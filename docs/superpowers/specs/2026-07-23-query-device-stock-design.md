# 查询物理机库存 (query_device_stock.py) 修改设计

## 背景

[api/query_device_stock.py](../../../api/query_device_stock.py) 通过天翼混合云 Python SDK 调用 `/v4/ebm/device-stock-list` 接口查询物理机库存。当前脚本运行即崩溃。

## 目标

按 [docs/查询物理机库存.md](../../../api/docs/查询物理机库存.md) 与 [docs/使用说明.md](../../../api/docs/使用说明.md) 修正并对齐脚本，使其能在混合云环境下正确查询物理机库存。

## 根因

[query_device_stock.py:25](../../../api/query_device_stock.py#L25) 调用 `Config(path="/v4/ebm/device-stock-list", ...)`，但 `Config.__init__` 签名仅为 `(endpoint, scheme, timeout, cert_verify)`，不存在 `path` 形参，直接抛 `TypeError`。

接口路径 `/v4/ebm/device-stock-list` 已硬编码在 [SDK 的 QueryDevicesStockRequest](../../../api/ctyun-hybrid-python-sdk/ctyun_hybrid_sdk/services/ebm/querydevicesstock/request.py#L26) 中，`path` 形参既非法又冗余。

## 修改内容（仅 query_device_stock.py）

1. **移除非法 `path` 参数**：`Config(...)` 仅保留 `endpoint="ct-global.ctapi.ctyun.local:12320"`、`scheme=SCHEME_HTTP`、`timeout=10`。endpoint 与 使用说明.md 的混合云访问方式一致。
2. **移除 `count` 参数**：文档标注 `count` 为公有云字段，混合云暂不支持、忽略。构造 `QueryDevicesStockRequestParam` 时不传 `count`，避免在签名 query 中发送无意义的 `count=`。
3. **保留必填/关键参数**：`region_id="nm8"`（必填）、`az_name="az1"`（文档 4.0 必填）、`device_type=""`（可选，留空返回全部设备类型）。
4. **补充 `Accept-Language: zh-CN` 请求头**：对齐文档 header 示例。保留现有 `userId` 头。`x-ctyun-user-id` 保持注释（可选）。
5. **保留签名方式**：`EbmClient(..., signer="hybrid")`，AK/SK/userId 维持原值（按用户选择不外置凭证）。
6. **改进响应输出**：响应 `returnObj` 经 `load_hook` 设置，`json.dumps(resp.__dict__)` 不能可靠展示库存数据。改为显式打印 `statusCode`、`errorCode`、`message`、`returnObj`，便于查看 `totalCount` 与 `results[]`（含 `az`/`available`/`success`/`deviceType`）。

## 不在范围内

- 不外置 AK/SK/userId/endpoint/region_id 到环境变量或配置文件。
- 不修改 SDK 源码。
- 不引入新依赖。
- 不删除 `debug_request.py`（独立的 requests 手动签名调试脚本，与本次 SDK 调用无关）。

## 验证

运行 `python api/query_device_stock.py`：
- 成功：`statusCode == 800`，`returnObj.results` 列出各可用区物理机可用数。
- 签名/连通失败：返回 `auth.gateway.4xx`（详见 网关签名说明.md 错误码表），指向环境（host 不可解析 / AK-SK 失效），非代码问题。
