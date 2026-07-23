from ctyun_hybrid_sdk.services.scaling.rulecreate.request import RuleCreateRequest, RuleCreateRequestParam, TriggerObj
from ctyun_hybrid_sdk.services.scaling.client import ScalingClient
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP


if __name__ == '__main__':
    # 先创建伸缩组
    group_id = 'test-lsj'
    # 创建一条伸缩策略
    data = {
        "statistics": "max",
        "name": "test-lsj",
        "period": "5m",
        "threshold": 50,
        "evaluationCount": 1,
        "comparisonOperator": "ge",
        "metricName": "cpu_util"
    }
    trigger_obj = TriggerObj(name=data['name'], metric_name=data['name'], statistics=data['statistics'],
                             comparison_operator=data['comparisonOperator'], threshold=data['threshold'],
                             period=data['period'], evaluation_count=data['evaluationCount'])
    params = {
        'operate_unit': 1,
        'operate_count': 1,
        'action': 1,
        'type': 1,
        'name': "test-lsj-rl"
    }
    request_param = RuleCreateRequestParam(region_id="nm8", operate_unit=params['operate_unit'],
                                           operate_count=params['operate_count'], action=params['action'],
                                           type=params['type'], group_id=group_id, name=params['name'],
                                           trigger_obj=trigger_obj)
    scaling_request = RuleCreateRequest(request_param)
    scaling_request.header["ctUserId"] = "1"
    credential = Credential(access_key="test123", secret_key="test456")
    config = Config(endpoint="ct-global.ctapi.ctyun.local:31152", scheme=SCHEME_HTTP, timeout=10)
    client = ScalingClient(credential, config)
    resp = client.group_update(scaling_request)

    rule_id = resp.__dict__['returnObj']['ruleID']
    # 验证创建成功
    print(rule_id)