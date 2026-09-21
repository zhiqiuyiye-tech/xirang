# coding=utf-8
import json
import sys
import os

# 将 api/ctyun-hybrid-python-sdk 加入到 Python 环境变量，以便直接引用 SDK
sys.path.append(os.path.join(os.path.dirname(__file__), "ctyun-hybrid-python-sdk"))

from ctyun_hybrid_sdk.services.ct.v4ecsflavorlist.request import V4EcsFlavorListRequestParam, V4EcsFlavorListRequest
from ctyun_hybrid_sdk.services.ct.client import CtClient
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP

def query_flavor():
    # 1. 设置访问凭证 (AK/SK)
    # 请替换为您的真实 AccessKey 和 SecretKey
    ak = "d99c7f600bee4234920c5d8ee148cb36"
    sk = "fd243425837a4c5496ffbc3791f7310b"
    credential = Credential(access_key=ak, secret_key=sk)

    # 2. 设置访问网关地址和协议
    # 根据混合云管 api 访问方式，通常需配置 host <云管ip> ct-global.ctapi.ctyun.local
    # 默认访问地址为 http://ct-global.ctapi.ctyun.local:12320
    # 接口路径 /v4/ecs/flavor/list 已封装在 V4EcsFlavorListRequest 内，无需在此指定
    config = Config(endpoint="ct-global.ctapi.ctyun.local:12320", scheme=SCHEME_HTTP, timeout=10)

    # 3. 创建云主机规格(CT)服务客户端
    # 按照网关签名说明，针对天翼混合云网关，指定 signer="hybrid"
    client = CtClient(credential, config, signer="hybrid")

    # 4. 初始化请求参数
    # 必填参数：region_id
    # 可选参数：az_name, flavor_type, flavor_name, flavor_cpu, flavor_ram, flavor_arch, flavor_series, flavor_id, nic_count, dec_id, instance_id
    # 注意：如果传了 flavor_id，则 az_name 为必填；只传 region_id 时 az_name 不必填
    # 注：az_name 在支持多 az 的资源池为必填；如不确定真实可用区名，先置 None 不传由网关判定
    request_param = V4EcsFlavorListRequestParam(
        region_id="cn-jx-jiu7-hybrid-industry",
az_name='cn-jx-jiu7-1a-hybrid-industry',       # 可用区（多az资源池必填）；置 None 则不发送该参数
        flavor_type="",     # 可填入规格类型，如 "CPU"、"CPU_S6"、"GPU_N_T4_V"；留空返回全部
    )
    # 可选筛选条件（按需取消注释设置）
    # request_param.set_flavor_name("ks1.medium.2")
    # request_param.set_flavor_cpu(4)
    # request_param.set_flavor_ram(8)
    # request_param.set_flavor_arch("x86")
    # request_param.set_flavor_series("s")
    # 查询指定规格ID时：az_name 必填
    # request_param.set_flavor_id("091de317-593a-9247-53b5-c981aa46e65b")

    # 5. 构造 Request 对象
    request = V4EcsFlavorListRequest(request_param)

    # 6. 设置自定义请求头 (根据 OpenAPI 规范，可按需补充)
    request.header["userId"] = "257230714868618"
    request.header["Accept-Language"] = "zh-CN"
    # request.header["x-ctyun-user-id"] = "实际的用户ID"

    # 7. 执行请求获取响应
    try:
        resp = client.v4_ecs_flavor_list(request)
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
            # 解析规格列表，表格化展示关键字段
            flavor_list = return_obj.get("flavorList", []) if isinstance(return_obj, dict) else []
            print("\n规格列表（共 %d 个）：" % len(flavor_list))
            print("%-28s%-22s%-18s%-6s%-8s%-8s%-8s%-6s%s" % ("规格名称", "系列", "类型", "CPU", "内存G", "架构", "可用", "可用数量", "规格ID"))
            print("-" * 140)
            for f in flavor_list:
                name = f.get("flavorName", "") or ""
                series = f.get("flavorSeriesName", "") or f.get("flavorSeries", "") or ""
                ftype = f.get("flavorType", "") or ""
                cpu = f.get("flavorCPU", "")
                ram = f.get("flavorRAM", "")
                arch = f.get("cpuInfo", "") or f.get("flavorArch", "") or ""
                available = f.get("available")
                avail_str = "是" if available is True else ("否" if available is False else "-")
                total = f.get("availableNum")
                fid = f.get("flavorID", "") or ""
                print("%-28s%-22s%-18s%-6s%-8s%-8s%-8s%-6s%s" % (str(name), str(series), str(ftype), str(cpu), str(ram), str(arch), avail_str, str(total), fid))

    except Exception as e:
        print("请求调用发生异常:", str(e))

if __name__ == '__main__':
    query_flavor()
