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


class RuleUpdateAlarmRequest(CTYunRequest):
    """
    修改一个报警策略
    """

    def __init__(self, request_param):
        super(RuleUpdateAlarmRequest, self).__init__("/v4/scaling/rule/update-alarm", "POST", "scaling", "application/json")
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
        if self.parameters.rule_id is not None:
            body_param["ruleID"] = self.parameters.rule_id
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.operate_unit is not None:
            body_param["operateUnit"] = self.parameters.operate_unit
        if self.parameters.operate_count is not None:
            body_param["operateCount"] = self.parameters.operate_count
        if self.parameters.cooldown is not None:
            body_param["cooldown"] = self.parameters.cooldown
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


class RuleUpdateAlarmRequestParam(object):

    def __init__(self, region_id, rule_id, group_id, name=None, action=None, operate_unit=None, operate_count=None, cooldown=None):
        """
        :param region_id: 资源池ID
        :param rule_id: 报警任务ID（规则ID）
        :param group_id: 报警伸缩组ID
        :param name: 伸缩策略名称；长度限制2～50（空串无效，视为不修改）
        :param action: 类型：int16;执行动作：增加（1），减少（2），设置为N（3）（0值无效，视为不修改）
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2） （0值无效，视为不修改）
        :param operate_count: 操作数量;大于0（0值无效，视为不修改）
        :param cooldown: 冷却时间，单位：秒 （0值无效，视为不修改）
        """
        self.region_id = region_id
        self.rule_id = rule_id
        self.group_id = group_id
        self.name = name
        self.action = action
        self.operate_unit = operate_unit
        self.operate_count = operate_count
        self.cooldown = cooldown

    def set_name(self, name):
        """
        :param name: 伸缩策略名称；长度限制2～50（空串无效，视为不修改）
        """
        self.name = name

    def set_action(self, action):
        """
        :param action: 类型：int16;执行动作：增加（1），减少（2），设置为N（3）（0值无效，视为不修改）
        """
        self.action = action

    def set_operate_unit(self, operate_unit):
        """
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2） （0值无效，视为不修改）
        """
        self.operate_unit = operate_unit

    def set_operate_count(self, operate_count):
        """
        :param operate_count: 操作数量;大于0（0值无效，视为不修改）
        """
        self.operate_count = operate_count

    def set_cooldown(self, cooldown):
        """
        :param cooldown: 冷却时间，单位：秒 （0值无效，视为不修改）
        """
        self.cooldown = cooldown

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.rule_id is None:
            raise Exception("rule_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

