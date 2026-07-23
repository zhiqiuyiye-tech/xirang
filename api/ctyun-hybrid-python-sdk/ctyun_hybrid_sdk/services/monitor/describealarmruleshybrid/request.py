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


class DescribeAlarmRulesHybridRequest(CTYunRequest):
    """
    查看告警规则的详情信息。   
    因与公有云底层逻辑区别，返回格式与公有云不同。
    """

    def __init__(self, request_param):
        super(DescribeAlarmRulesHybridRequest, self).__init__("/v4/monitor/describe-alarm-rule", "GET", "monitor", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.alarm_rule_id is not None:
            query_param["alarmRuleID"] = self.parameters.alarm_rule_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeAlarmRulesHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id, ):
        """
        :param region_id: 资源池ID
        :param alarm_rule_id: 告警规则ID
        """
        self.region_id = region_id
        self.alarm_rule_id = alarm_rule_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")

