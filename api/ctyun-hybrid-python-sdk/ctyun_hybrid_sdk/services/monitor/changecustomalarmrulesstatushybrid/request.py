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


class ChangeCustomAlarmRulesStatusHybridRequest(CTYunRequest):
    """
    批量更新告警规则状态为禁用或启用
    """

    def __init__(self, request_param):
        super(ChangeCustomAlarmRulesStatusHybridRequest, self).__init__("/v4/monitor/change-custom-alarm-rules-status", "POST", "monitor", "application/json")
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
        if self.parameters.alarm_rule_id_list is not None:
            body_param["alarmRuleIDList"] = self.parameters.alarm_rule_id_list
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
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


class ChangeCustomAlarmRulesStatusHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id_list, status, ):
        """
        :param region_id: 资源池ID
        :param alarm_rule_id_list: 告警规则ID列表 注意:此参数为数组
        :param status: 本参数表示规则状态。取值范围：0：启用。1：停用。根据以上范围取值。
        """
        self.region_id = region_id
        self.alarm_rule_id_list = alarm_rule_id_list
        self.status = status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id_list is None:
            raise Exception("alarm_rule_id_list can not None")
        if self.status is None:
            raise Exception("status can not None")

