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


class RuleCreateCycleRequest(CTYunRequest):
    """
    创建一个周期策略   
    **注意**：cycle=2时，day取值范围为0~6，0代表周天(底层设计如此)
    """

    def __init__(self, request_param):
        super(RuleCreateCycleRequest, self).__init__("/v4/scaling/rule/create-cycle", "POST", "scaling", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.cycle is not None:
            body_param["cycle"] = self.parameters.cycle
        if self.parameters.operate_count is not None:
            body_param["operateCount"] = self.parameters.operate_count
        if self.parameters.operate_unit is not None:
            body_param["operateUnit"] = self.parameters.operate_unit
        if self.parameters.execution_time is not None:
            body_param["executionTime"] = self.parameters.execution_time
        if self.parameters.effective_from is not None:
            body_param["effectiveFrom"] = self.parameters.effective_from
        if self.parameters.effective_till is not None:
            body_param["effectiveTill"] = self.parameters.effective_till
        if self.parameters.day is not None:
            body_param["day"] = self.parameters.day
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


class RuleCreateCycleRequestParam(object):

    def __init__(self, region_id, group_id, name, action, cycle, operate_count, operate_unit, execution_time, effective_from, effective_till, day, ):
        """
        :param region_id: 资源池ID
        :param group_id: 伸缩组ID
        :param name: 规则名称，请注意不能与当前伸缩组内的其他规则冲突;长度2～50;
        :param action: 类型：int16;执行动作：增加（1），减少（2），设置为N（3）
        :param cycle: 类型：int16;循环方式，取值范围1-3（包含边界）。说明：1：按月循环，2：按周循环，3：按天循环
        :param operate_count: 执行次数
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2）
        :param execution_time: 周期规则执行时间（只取小时和分钟，年月日无效，但必须符合effectiveFrom/TIill统一格式）
        :param effective_from: 周期规则执行有效期起始时间
        :param effective_till: 周期规则执行有效期截止时间
        :param day: 当cycle为1时必填，且list元素限制为1-31（包含边界）中的整数且不重复；当cycle为2时必填，且list元素限制为1-7（包含边界）中的整数且不重复；当cycle为3时非必填； 注意:此参数为数组
        """
        self.region_id = region_id
        self.group_id = group_id
        self.name = name
        self.action = action
        self.cycle = cycle
        self.operate_count = operate_count
        self.operate_unit = operate_unit
        self.execution_time = execution_time
        self.effective_from = effective_from
        self.effective_till = effective_till
        self.day = day

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.cycle is None:
            raise Exception("cycle can not None")
        if self.operate_count is None:
            raise Exception("operate_count can not None")
        if self.operate_unit is None:
            raise Exception("operate_unit can not None")
        if self.execution_time is None:
            raise Exception("execution_time can not None")
        if self.effective_from is None:
            raise Exception("effective_from can not None")
        if self.effective_till is None:
            raise Exception("effective_till can not None")
        if self.day is None:
            raise Exception("day can not None")

