# coding=utf-8
import json
import sys
import os

# Windows 控制台默认 GBK 编码会导致中文输出乱码，重置 stdout/stderr 为 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 将 api/ctyun-hybrid-python-sdk 加入到 Python 环境变量，以便直接引用 SDK
sys.path.append(os.path.join(os.path.dirname(__file__), "ctyun-hybrid-python-sdk"))

from ctyun_hybrid_sdk.services.common.getregiontotalremainmetric.request import (
    GetRegionTotalRemainMetricRequest,
    GetRegionTotalRemainMetricRequestParam,
)
from ctyun_hybrid_sdk.services.common.client import CommonClient
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP


def query_region_total_remain():
    # 1. 设置访问凭证 (AK/SK)
    # 请替换为您的真实 AccessKey 和 SecretKey
    ak = "d99c7f600bee4234920c5d8ee148cb36"
    sk = "fd243425837a4c5496ffbc3791f7310b"
    credential = Credential(access_key=ak, secret_key=sk)

    # 2. 设置访问网关地址和协议
    # 根据混合云管 api 访问方式，通常需配置 host <云管ip> ct-global.ctapi.ctyun.local
    # 默认访问地址为 http://ct-global.ctapi.ctyun.local:12320
    # 接口路径 /v4/region/get-total-remain-metric 已封装在 GetRegionTotalRemainMetricRequest 内，无需在此指定
    config = Config(endpoint="ct-global.ctapi.ctyun.local:12320", scheme=SCHEME_HTTP, timeout=10)

    # 3. 创建通用服务客户端
    # 按照网关签名说明，针对天翼混合云网关，指定 signer="hybrid"
    client = CommonClient(credential, config, signer="hybrid")

    # 4. 初始化请求参数
    # 必填参数：region_id (资源池ID)
    # 可选参数：pool_type (查询全部资源池类型，暂只支持 maz，openapi 只支持 4.0 的 maz，其他忽略；该参数暂不支持)
    request_param = GetRegionTotalRemainMetricRequestParam(
        region_id="cn-jx-jiu7-hybrid-industry",
        pool_type=None,     # 暂不支持，置 None 不发送该参数
    )

    # 5. 构造 Request 对象
    request = GetRegionTotalRemainMetricRequest(request_param)

    # 6. 设置自定义请求头 (根据 OpenAPI 规范，可按需补充)
    request.header["userId"] = "257230714868618"
    request.header["Accept-Language"] = "zh-CN"
    # request.header["x-ctyun-user-id"] = "实际的用户ID"

    # 7. 执行请求获取响应
    try:
        resp = client.get_region_total_remain_metric(request)
        # 打印返回的解析内容
        # 注：resp 属性由 SDK 的 load_hook 设置；若网关返回空 body 则属性可能缺失，用 getattr 兜底
        print("请求成功，返回内容：")
        print("statusCode:", getattr(resp, "statusCode", None))
        print("errorCode:", getattr(resp, "errorCode", None))
        print("message:", getattr(resp, "message", None))
        print("description:", getattr(resp, "description", None))
        return_obj = getattr(resp, "returnObj", None)
        print("returnObj:", json.dumps(return_obj, indent=4, ensure_ascii=False))
        # 若 returnObj 为空或 statusCode 非 800，通常为网关签名/连通性问题（见 docs/网关签名说明.md 错误码表）
        if getattr(resp, "statusCode", None) != 800 or return_obj is None:
            print("提示：网关未返回业务数据，请检查 host 解析、网关连通性及 AK/SK 是否有效。")
        else:
            # 提取关键总量/已用量指标便于快速查看
            capacity = return_obj.get("capacity", {}) if isinstance(return_obj, dict) else {}
            print("\n关键指标摘要:")
            print("资源池名称:", return_obj.get("poolName") if isinstance(return_obj, dict) else None)
            print("VCPU:   总量 %s / 已分配 %s" % (capacity.get("totalCpu"), capacity.get("cpuUse")))
            print("内存:   总量 %s %s / 已分配 %s %s" % (
                capacity.get("totalMemory"), capacity.get("memUnits"),
                capacity.get("memUse"), capacity.get("memUseUnits")))
            print("块存储: 总量 %s %s / 已分配 %s %s" % (
                capacity.get("totalDisk"), capacity.get("diskUnits"),
                capacity.get("allocatedDisk"), capacity.get("diskAllocatedUnits")))
            print("对象存储:总量 %s %s / 已用 %s %s" % (
                capacity.get("totalOss"), capacity.get("ossUnits"),
                capacity.get("ossUse"), capacity.get("ossUseUnits")))
            print("文件存储:总量 %s %s / 已分配 %s %s" % (
                capacity.get("totalSfs"), capacity.get("sfsUnits"),
                capacity.get("sfsUse"), capacity.get("sfsUseUnits")))
            print("IP:     总量 %s / 已分配 %s / 剩余 %s" % (
                capacity.get("ipTotal"), capacity.get("ipAllocated"), capacity.get("ipRemainingTotal")))
            print("宿主机总量:", capacity.get("totalHost"), "| 裸金属总量:", capacity.get("totalBms"), "| 虚机使用总量:", capacity.get("totalEcs"))

    except Exception as e:
        print("请求调用发生异常:", str(e))


if __name__ == '__main__':
    query_region_total_remain()
