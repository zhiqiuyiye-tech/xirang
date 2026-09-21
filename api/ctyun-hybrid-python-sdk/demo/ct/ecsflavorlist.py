# -*- coding: utf-8 -*-
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS
from ctyun_hybrid_sdk.services.ct.v4ecsflavorlist.request import V4EcsFlavorListRequest, V4EcsFlavorListRequestParam
from ctyun_hybrid_sdk.services.ct.client import CtClient
from ctyun_hybrid_sdk.core.logger import get_default_logger

if __name__ == '__main__':
    credential = Credential(access_key="xxxx", secret_key="xxxxx")
    # 设置访问网关地址、协议、超时时间
    config = Config(endpoint="ct-global.ctapi-internal.ctyun.local:40117", scheme=SCHEME_HTTPS, timeout=180, cert_verify='../test.crt')
    logger = get_default_logger()
    ct_client = CtClient(credential, config)

    # 示例1：只传 regionID，查询该资源池下所有可用规格
    request_param = V4EcsFlavorListRequestParam(region_id="2022guizhou_syj")
    # 可选筛选条件（按需设置）
    # request_param.set_flavor_type("CPU")
    # request_param.set_flavor_cpu(4)
    # request_param.set_flavor_ram(8)
    # request_param.set_flavor_arch("x86")
    # request_param.set_flavor_series("s")

    # 示例2：查询指定规格ID（传 flavorID 时 azName 必填）
    # request_param = V4EcsFlavorListRequestParam(region_id="2022guizhou_syj", az_name="cn-xinan1-1A", flavor_id="091de317-593a-9247-53b5-c981aa46e65b")

    request = V4EcsFlavorListRequest(request_param)
    resp = ct_client.v4_ecs_flavor_list(request)
    print(resp.__dict__)
