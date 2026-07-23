from ctyun_hybrid_sdk.services.ctvpc.createsgingressrule.request import CreateSgIngressRuleRequest, CreateSgIngressRuleRequestParam, SecurityGroupRule
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP
from ctyun_hybrid_sdk.services.ctvpc.client import CtvpcClient

if __name__ == '__main__':
    vpc_id = 'test-123'

    # 创建安全组

    sg_id = "sg-test123-lsj"
    # 创建入向规则
    ingress_rule = SecurityGroupRule(direction="egress", ethertype="IPv4", action="accept",
                                     dest_cidr_ip="0.0.0.0/0", range="22-33", protocol="TCP")
    requestParam = CreateSgIngressRuleRequestParam(region_id="nm8", security_group_id=sg_id,
                                                   security_group_rules=ingress_rule,
                                                   client_token="test123")
    request = CreateSgIngressRuleRequest(requestParam)
    request.header["ctUserId"] = "1"
    credential = Credential(access_key="test123", secret_key="test456")
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="ct-global.ctapi.ctyun.local:31152", scheme=SCHEME_HTTP, timeout=10)
    vpc_client = CtvpcClient(credential, config)
    resp = vpc_client.create_sg_ingress_rule(request)


