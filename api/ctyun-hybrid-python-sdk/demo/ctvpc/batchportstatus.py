from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP
from ctyun_hybrid_sdk.core.hybrid_signer import HybridSigner
from ctyun_hybrid_sdk.services.ctvpc.batchcheckportstatus.request import BatchCheckPortStatusRequest, BatchCheckPortStatusRequestParam
from ctyun_hybrid_sdk.services.ctvpc.client import CtvpcClient
from ctyun_hybrid_sdk.core.logger import get_default_logger


if __name__ == '__main__':
    credential = Credential(access_key="xxxxx", secret_key="xxxxx")
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="ct-global.ctapi-internal.ctyun.local:31111", scheme=SCHEME_HTTP, timeout=10)
    logger = get_default_logger()
    vpc_client = CtvpcClient(credential, config,signer="hybrid")
    vpc_id = "vpc-tesfasdfasdf"
    sub_id = "sub-tesfasdfasdf"
    port_1_id = "ports-test123"
    port_2_id = "ports-test456"
    port_i_ds = port_1_id + ',' + port_2_id
    # todo:需要绑定云主机没搞
    requestParam = BatchCheckPortStatusRequestParam(region_id="nm8", port_ids=port_i_ds)
    request = BatchCheckPortStatusRequest(requestParam)
    request.header["ctUserId"] = '1'
    resp = vpc_client.send(request)
    resp = resp.__dict__
    print(resp)