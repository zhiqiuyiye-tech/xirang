from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP
from ctyun_hybrid_sdk.services.ctvpc.listhavip.request import ListHavipRequest, ListHavipRequestParam,Filters
from ctyun_hybrid_sdk.services.ctvpc.client import CtvpcClient


if __name__ == '__main__':
    credential = Credential(access_key="xxxxx", secret_key="xxxxx")
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="ct-global.ctapi-internal.ctyun.local:31167", scheme=SCHEME_HTTP, timeout=10)
    vpc_client = CtvpcClient(credential, config)
    filters = Filters(key='haVipID', value="aa-test123")
    requestParam = ListHavipRequestParam(region_id="2022_guizhou_siyouyun2", filters=filters,
                                         client_token="test123&")


    request = ListHavipRequest(requestParam)
    request.header["ctUserId"] = "1"
    resp = vpc_client.send(request)
    resp = resp.__dict__
    print(resp)