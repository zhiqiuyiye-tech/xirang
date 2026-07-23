from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP
from ctyun_hybrid_sdk.services.ctvpn.ctvpnusergatewaylist.request import CtvpnUserGatewayListRequest, CtvpnUserGatewayListRequestParam
from ctyun_hybrid_sdk.services.ctvpn.client import CtvpnClient


if __name__ == '__main__':
    credential = Credential(access_key="xxxx", secret_key="xxxxx")
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="ct-global.ctapi.ctyun.local:31152", scheme=SCHEME_HTTP, timeout=10)
    vpn_client = CtvpnClient(credential, config)
    request_param = CtvpnUserGatewayListRequestParam(customer_id='aba3e26d-a9d5-4993-b68a-4bc42797842c',
                                                     ct_user_id='aba3e26d-a9d5-4993-b68a-4bc42797842c',region_id='nm8',
                                                     id='07e933cb-712d-4eac-ac45-b4f74889288d',
                                                     name='User-Gateway-9zvtlwb6')
    request = CtvpnUserGatewayListRequest(request_param)
    resp = vpn_client.ctvpn_user_gateway_list(request)
    print(resp)