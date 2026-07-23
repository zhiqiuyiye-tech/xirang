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


class SetAlarmRuleContactHybridRequest(CTYunRequest):
    """
    调用此接口可设置指定告警规则的告警联系人及通知方式。
    """

    def __init__(self, request_param):
        super(SetAlarmRuleContactHybridRequest, self).__init__("/v4/monitor/set-alarm-rule-contact", "POST", "monitor", "application/json")
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
        if self.parameters.contact_group_list is not None:
            body_param["contactGroupList"] = self.parameters.contact_group_list
        if self.parameters.notify_type is not None:
            body_param["notifyType"] = self.parameters.notify_type
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


class SetAlarmRuleContactHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id, contact_group_list, notify_type, ):
        """
        :param region_id: 
        :param alarm_rule_id: 
        :param contact_group_list: 告警接收策略通知人ID列表告警联系人组（云管只支持1个） 注意:此参数为数组
        :param notify_type: 取值范围：internal:站内信通知。sms：短信通知。email：邮件通知。internal、email根据云管要求必填 注意:此参数为数组
        """
        self.region_id = region_id
        self.alarm_rule_id = alarm_rule_id
        self.contact_group_list = contact_group_list
        self.notify_type = notify_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")
        if self.contact_group_list is None:
            raise Exception("contact_group_list can not None")
        if self.notify_type is None:
            raise Exception("notify_type can not None")

