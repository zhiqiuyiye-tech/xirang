# coding=utf8

# Copyright 2023 CTYUN.CN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ctyun_hybrid_sdk.core.request import CTYunRequest


class UpdateAlarmRuleConditionsHybridRequest(CTYunRequest):
    """
    告警规则：修改告警规则条件
    """

    def __init__(self, request_param):
        super(UpdateAlarmRuleConditionsHybridRequest, self).__init__("/v4/monitor/update-alarm-rule-conditions", "POST", "monitor", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.alarm_rule_id is not None:
            body_param["alarmRuleID"] = self.parameters.alarm_rule_id
        if self.parameters.rules is not None:
            rules = []
            if isinstance(self.parameters.rules, list):
                for item in self.parameters.rules:
                    if type(item) is dict:
                        rules.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        rules.append(item_dict_value)
            else:
                rules.append(self.parameters.rules.get_dic())
            body_param["rules"] = rules
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class Rule(object):

    def __init__(self, fun, operator, evaluation_count, value, period, metric, ):
        """
        :param fun: 本参数表示告警采用算法。取值范围：   
         last：原始值算法。   
         avg：平均值算法。   
         max：最大值算法。   
         min：最小值算法。   
         根据以上范围取值。
        :param operator: 本参数表示比较符。默认值le。取值范围：   
         eq：等于。   
         gt：大于。   
         ge：大于等于。   
         lt：小于。   
         le：小于等于。   
         根据以上范围取值。
        :param evaluation_count: 持续次数，当规则执行结果持续多久符合条件时报警（防抖）。（云管支持1-5次）
        :param value: 告警阈值，大于0整数。若指标单位为%，不能大于100
        :param period: 本参数表示算法统计周期。（混合云管支持：1m, 5m, 20m, 1h, 4h, 12h, 24h）
        :param metric: 监控指标
        """
        self.fun = fun
        self.operator = operator
        self.evaluation_count = evaluation_count
        self.value = value
        self.period = period
        self.metric = metric
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.fun is not None:
            obj_dict["fun"] = self.fun
        if self.operator is not None:
            obj_dict["operator"] = self.operator
        if self.evaluation_count is not None:
            obj_dict["evaluationCount"] = self.evaluation_count
        if self.value is not None:
            obj_dict["value"] = self.value
        if self.period is not None:
            obj_dict["period"] = self.period
        if self.metric is not None:
            obj_dict["metric"] = self.metric
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.fun is None:
            raise Exception("fun can not None")
        if self.operator is None:
            raise Exception("operator can not None")
        if self.evaluation_count is None:
            raise Exception("evaluation_count can not None")
        if self.value is None:
            raise Exception("value can not None")
        if self.period is None:
            raise Exception("period can not None")
        if self.metric is None:
            raise Exception("metric can not None")


class UpdateAlarmRuleConditionsHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id, rules, ):
        """
        :param region_id: 
        :param alarm_rule_id: 
        :param rules:  注意:此参数为数组
        """
        self.region_id = region_id
        self.alarm_rule_id = alarm_rule_id
        self.rules = rules

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")
        if self.rules is None:
            raise Exception("rules can not None")

