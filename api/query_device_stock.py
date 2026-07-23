# coding=utf-8
import json
import sys
import os

# 将 api/ctyun-hybrid-python-sdk 加入到 Python 环境变量，以便直接引用 SDK
sys.path.append(os.path.join(os.path.dirname(__file__), "ctyun-hybrid-python-sdk"))

from ctyun_hybrid_sdk.services.ebm.querydevicesstock.request import QueryDevicesStockRequestParam, QueryDevicesStockRequest
from ctyun_hybrid_sdk.services.ebm.client import EbmClient
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP

def query_device_stock():
    # 1. 设置访问凭证 (AK/SK)
    # 请替换为您的真实 AccessKey 和 SecretKey
    ak = "d99c7f600bee4234920c5d8ee148cb36"
    sk = "fd243425837a4c5496ffbc3791f7310b"
    credential = Credential(access_key=ak, secret_key=sk)
    
    # 2. 设置访问网关地址和协议
    # 根据混合云管 api 访问方式，通常需配置 host <云管ip> ct-global.ctapi.ctyun.local
    # 默认访问地址为 http://ct-global.ctapi.ctyun.local:12320
    # 接口路径 /v4/ebm/device-stock-list 已封装在 QueryDevicesStockRequest 内，无需在此指定
    config = Config(endpoint="ct-global.ctapi.ctyun.local:12320", scheme=SCHEME_HTTP, timeout=10)
    
    # 3. 创建裸金属(EBM)服务客户端
    # 按照网关签名说明，针对天翼混合云网关，指定 signer="hybrid"
    client = EbmClient(credential, config, signer="hybrid")
    
    # 4. 初始化请求参数
    # 必填参数：region_id
    # 可选参数：device_type, az_name
    # 注：count 为公有云字段，混合云暂不支持，故不传
    # 注：az_name 在 4.0 资源池为必填，3.0 资源池可不传；如不确定真实可用区名，先置 None 不传由网关判定
    request_param = QueryDevicesStockRequestParam(
        region_id="cn-jx-jiu7-hybrid-industry",
        device_type="",     # 可填入具体的设备类型，如 "physical.t1.large"；留空返回全部
        az_name='cn-jx-jiu7-1a-hybrid-industry',       # 可用区（4.0 必填）；置 None 则不发送该参数
    )
    
    # 5. 构造 Request 对象
    request = QueryDevicesStockRequest(request_param)
    
    # 6. 设置自定义请求头 (根据 OpenAPI 规范，可按需补充)
    request.header["userId"] = "257230714868618"
    request.header["Accept-Language"] = "zh-CN"
    # request.header["x-ctyun-user-id"] = "实际的用户ID"
    
    # 7. 执行请求获取响应
    try:
        resp = client.query_devices_stock(request)
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

    except Exception as e:
        print("请求调用发生异常:", str(e))

if __name__ == '__main__':
    query_device_stock()
