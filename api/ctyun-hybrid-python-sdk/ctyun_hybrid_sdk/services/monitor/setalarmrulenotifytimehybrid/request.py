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


class SetAlarmRuleNotifyTimeHybridRequest(CTYunRequest):
    """
    调用此接口可设置指定告警规则的通知周期。
    """

    def __init__(self, request_param):
        super(SetAlarmRuleNotifyTimeHybridRequest, self).__init__("/v4/monitor/set-alarm-rule-notify-time", "POST", "monitor", "application/json")
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
        if self.parameters.notify_weekdays is not None:
            body_param["notifyWeekdays"] = self.parameters.notify_weekdays
        if self.parameters.notify_start is not None:
            body_param["notifyStart"] = self.parameters.notify_start
        if self.parameters.notify_end is not None:
            body_param["notifyEnd"] = self.parameters.notify_end
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


class SetAlarmRuleNotifyTimeHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id, notify_weekdays=None, notify_start=None, notify_end=None):
        """
        :param region_id: 资源池ID
        :param alarm_rule_id: 告警规则ID
        :param notify_weekdays: 本参数表示通知周期。默认值[0,1,2,3,4,5,6]。取值范围：0：周日。1：周一。2：周二。3：周三。4：周四。5：周五。6：周六。根据以上范围取值。 注意:此参数为数组
        :param notify_start: 通知起始时段，默认值为全时段"00:00:00"
        :param notify_end: 通知结束时段，默认值为全时段"23:59:59"
        """
        self.region_id = region_id
        self.alarm_rule_id = alarm_rule_id
        self.notify_weekdays = notify_weekdays
        self.notify_start = notify_start
        self.notify_end = notify_end

    def set_notify_weekdays(self, notify_weekdays):
        """
        :param notify_weekdays: 本参数表示通知周期。默认值[0,1,2,3,4,5,6]。取值范围：0：周日。1：周一。2：周二。3：周三。4：周四。5：周五。6：周六。根据以上范围取值。
        """
        self.notify_weekdays = notify_weekdays

    def set_notify_start(self, notify_start):
        """
        :param notify_start: 通知起始时段，默认值为全时段"00:00:00"
        """
        self.notify_start = notify_start

    def set_notify_end(self, notify_end):
        """
        :param notify_end: 通知结束时段，默认值为全时段"23:59:59"
        """
        self.notify_end = notify_end

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")

