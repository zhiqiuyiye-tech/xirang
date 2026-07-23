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


class RuleUpdateScheduledRequest(CTYunRequest):
    """
    修改一个定时任务的信息
    """

    def __init__(self, request_param):
        super(RuleUpdateScheduledRequest, self).__init__("/v4/scaling/rule/update-scheduled", "POST", "scaling", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.operate_unit is not None:
            body_param["operateUnit"] = self.parameters.operate_unit
        if self.parameters.operate_count is not None:
            body_param["operateCount"] = self.parameters.operate_count
        if self.parameters.execution_time is not None:
            body_param["executionTime"] = self.parameters.execution_time
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
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


class RuleUpdateScheduledRequestParam(object):

    def __init__(self, region_id, rule_id, name, operate_unit=None, operate_count=None, execution_time=None, action=None, group_id=None):
        """
        :param region_id: 区域id
        :param rule_id: 定时任务ID（规则ID）
        :param name: 定时任务名称,长度范围[2,50]
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2）(0值无效，视为不修改)
        :param operate_count: 操作数量(大于0，0值无效，视为不修改)
        :param execution_time: 执行时间  TZ格式
        :param action: 类型：int16；执行动作：增加（1），减少（2），设置为N（3）(0值无效，视为不修改)
        :param group_id: 伸缩组ID   （底层不需要该参数，公有云必选，故只做接收处理）
        """
        self.region_id = region_id
        self.rule_id = rule_id
        self.name = name
        self.operate_unit = operate_unit
        self.operate_count = operate_count
        self.execution_time = execution_time
        self.action = action
        self.group_id = group_id

    def set_operate_unit(self, operate_unit):
        """
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2）(0值无效，视为不修改)
        """
        self.operate_unit = operate_unit

    def set_operate_count(self, operate_count):
        """
        :param operate_count: 操作数量(大于0，0值无效，视为不修改)
        """
        self.operate_count = operate_count

    def set_execution_time(self, execution_time):
        """
        :param execution_time: 执行时间  TZ格式
        """
        self.execution_time = execution_time

    def set_action(self, action):
        """
        :param action: 类型：int16；执行动作：增加（1），减少（2），设置为N（3）(0值无效，视为不修改)
        """
        self.action = action

    def set_group_id(self, group_id):
        """
        :param group_id: 伸缩组ID   （底层不需要该参数，公有云必选，故只做接收处理）
        """
        self.group_id = group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.rule_id is None:
            raise Exception("rule_id can not None")
        if self.name is None:
            raise Exception("name can not None")

