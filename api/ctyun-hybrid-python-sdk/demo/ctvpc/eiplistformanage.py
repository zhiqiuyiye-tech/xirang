# -*- coding: utf-8 -*-
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP
from ctyun_hybrid_sdk.core.hybrid_signer import HybridSigner
from ctyun_hybrid_sdk.services.ctvpc.eiplistformanage.request import EipListForManageRequest, EipListForManageRequestParam
from ctyun_hybrid_sdk.services.ctvpc.client import CtvpcClient
from ctyun_hybrid_sdk.core.logger import get_default_logger
import os

if __name__ == '__main__':
    credential = Credential(access_key="xxxx", secret_key="xxxxx")
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间

    config = Config(endpoint="ct-global.ctapi-internal.ctyun.local:40117", scheme=SCHEME_HTTPS, timeout=180,cert_verify='../test.crt')
    logger = get_default_logger()
    vpc_client = CtvpcClient(credential, config)
    requestParam = EipListForManageRequestParam(region_id="2022_guizhou_siyouyun2",ids=["test123","test456"],
                                         client_token="test123#")
    request = EipListForManageRequest(requestParam)
    request.header["ctUserId"] = "1"
    resp = vpc_client.send(request)
    resp = resp.__dict__
    print(resp)