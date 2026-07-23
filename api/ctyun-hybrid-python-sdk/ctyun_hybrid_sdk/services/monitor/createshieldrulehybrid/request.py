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


class CreateShieldRuleHybridRequest(CTYunRequest):
    """
    创建告警屏蔽规则
    """

    def __init__(self, request_param):
        super(CreateShieldRuleHybridRequest, self).__init__("/v4/monitor/create-shield-rule", "POST", "monitor", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.alarm_rule_id is not None:
            body_param["alarmRuleID"] = self.parameters.alarm_rule_id
        if self.parameters.work_start_time is not None:
            body_param["workStartTime"] = self.parameters.work_start_time
        if self.parameters.work_end_time is not None:
            body_param["workEndTime"] = self.parameters.work_end_time
        if self.parameters.week_days is not None:
            body_param["weekDays"] = self.parameters.week_days
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.process_policy is not None:
            body_param["processPolicy"] = self.parameters.process_policy
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


class CreateShieldRuleHybridRequestParam(object):

    def __init__(self, region_id, name, alarm_rule_id, work_start_time, work_end_time, week_days, start_time, end_time, process_policy, description=None):
        """
        :param region_id: 资源池ID
        :param name: 长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param description: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!），不支持连续字符--
        :param alarm_rule_id: 告警规则ID
        :param work_start_time: 格式：2025-04-13 00:00:00
        :param work_end_time: 格式：2025-04-13 00:00:00
        :param week_days: 1、2、3、4、5、6、0（星期一、星期二、星期三、星期四、星期五、星期六、星期天） 注意:此参数为数组
        :param start_time: 格式：00:00:00
        :param end_time: 格式：00:00:00
        :param process_policy: shield：显示在“被屏蔽告警”中，discard：丢弃
        """
        self.region_id = region_id
        self.name = name
        self.description = description
        self.alarm_rule_id = alarm_rule_id
        self.work_start_time = work_start_time
        self.work_end_time = work_end_time
        self.week_days = week_days
        self.start_time = start_time
        self.end_time = end_time
        self.process_policy = process_policy

    def set_description(self, description):
        """
        :param description: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!），不支持连续字符--
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.alarm_rule_id is None:
            raise Exception("alarm_rule_id can not None")
        if self.work_start_time is None:
            raise Exception("work_start_time can not None")
        if self.work_end_time is None:
            raise Exception("work_end_time can not None")
        if self.week_days is None:
            raise Exception("week_days can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")
        if self.process_policy is None:
            raise Exception("process_policy can not None")

