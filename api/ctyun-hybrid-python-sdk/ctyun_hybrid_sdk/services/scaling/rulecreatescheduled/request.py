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


class RuleCreateScheduledRequest(CTYunRequest):
    """
    创建一个定时任务
    """

    def __init__(self, request_param):
        super(RuleCreateScheduledRequest, self).__init__("/v4/scaling/rule/create-scheduled", "POST", "scaling", "application/json")
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
            body_param["groupId"] = self.parameters.group_id
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


class RuleCreateScheduledRequestParam(object):

    def __init__(self, region_id, group_id, name, operate_unit, operate_count, execution_time, action, ):
        """
        :param region_id: 区域id
        :param group_id: 伸缩组id
        :param name: 定时任务名称;2~50个字符
        :param operate_unit: 类型：int16；操作的单位：个数（1），百分比（2）
        :param operate_count: 操作数量;大于0
        :param execution_time: 执行时间  TZ格式
        :param action: 类型：int16；执行动作：增加（1），减少（2），设置为N（3）
        """
        self.region_id = region_id
        self.group_id = group_id
        self.name = name
        self.operate_unit = operate_unit
        self.operate_count = operate_count
        self.execution_time = execution_time
        self.action = action

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
        if self.operate_unit is None:
            raise Exception("operate_unit can not None")
        if self.operate_count is None:
            raise Exception("operate_count can not None")
        if self.execution_time is None:
            raise Exception("execution_time can not None")
        if self.action is None:
            raise Exception("action can not None")

