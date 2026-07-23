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


class SetAlarmRuleNotifyStrategyHybridRequest(CTYunRequest):
    """
    调用此接口可设置指定告警规则的通知策略（重复通知，静默时间，告警恢复是否通知）。
    """

    def __init__(self, request_param):
        super(SetAlarmRuleNotifyStrategyHybridRequest, self).__init__("/v4/monitor/set-alarm-rule-notify-strategy", "POST", "monitor", "application/json")
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
        if self.parameters.repeat_times is not None:
            body_param["repeatTimes"] = self.parameters.repeat_times
        if self.parameters.silence_time is not None:
            body_param["silenceTime"] = self.parameters.silence_time
        if self.parameters.recover_notify is not None:
            body_param["recoverNotify"] = self.parameters.recover_notify
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


class SetAlarmRuleNotifyStrategyHybridRequestParam(object):

    def __init__(self, region_id, alarm_rule_id, repeat_times=None, silence_time=None, recover_notify=None):
        """
        :param region_id: 资源池ID
        :param alarm_rule_id: 告警规则ID
        :param repeat_times: 重复告警通知次数（云管只支持0-3次）
        :param silence_time: 静默时间，多久重复通知一次，单位为秒（混合云支持：300, 600, 900, 1800, 3600, 10800, 21600, 43200, 86400）
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        """
        self.region_id = region_id
        self.alarm_rule_id = alarm_rule_id
        self.repeat_times = repeat_times
        self.silence_time = silence_time
        self.recover_notify = recover_notify

    def set_repeat_times(self, repeat_times):
        """
        :param repeat_times: 重复告警通知次数（云管只支持0-3次）
        """
        self.repeat_times = repeat_times

    def set_silence_time(self, silence_time):
        """
        :param silence_time: 静默时间，多久重复通知一次，单位为秒（混合云支持：300, 600, 900, 1800, 3600, 10800, 21600, 43200, 86400）
        """
        self.silence_time = silence_time

    def set_recover_notify(self, recover_notify):
        """
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        """
        self.recover_notify = recover_notify

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")

