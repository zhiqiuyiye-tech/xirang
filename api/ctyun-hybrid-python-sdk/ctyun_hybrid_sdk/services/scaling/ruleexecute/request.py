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


class RuleExecuteRequest(CTYunRequest):
    """
    请求示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"regionID"</span><span class="colour" style="color:rgb(0, 0, 0)">:</span><span class="colour" style="color:rgb(4, 81, 165)">"nm8"</span><span class="colour" style="color:rgb(0, 0, 0)">,</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"ruleID"</span><span class="colour" style="color:rgb(0, 0, 0)">:</span><span class="colour" style="color:rgb(4, 81, 165)">"8e6883a0-5b63-11ed-a71c-0242ac130010"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>   
       
    返回示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    </span><span class="colour" style="color:rgb(163, 21, 21)">"returnObj"</span><span class="colour" style="color:rgb(0, 0, 0)">: {</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">        </span><span class="colour" style="color:rgb(163, 21, 21)">"ruleID"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"8e6883a0-5b63-11ed-a71c-0242ac130010"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    },</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    </span><span class="colour" style="color:rgb(163, 21, 21)">"statusCode"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(9, 134, 88)">800</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>
    """

    def __init__(self, request_param):
        super(RuleExecuteRequest, self).__init__("/v4/scaling/rule/execute", "POST", "scaling", "application/json")
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
        if self.parameters.execution_mode is not None:
            body_param["executionMode"] = self.parameters.execution_mode
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


class RuleExecuteRequestParam(object):

    def __init__(self, region_id, rule_id, execution_mode=None, group_id=None):
        """
        :param region_id: 资源id
        :param rule_id: 规则id
        :param execution_mode: 执行方式（自动执行策略（1）/手动执行策略（2）/手动移入实例（3）/手动移出实例（4）/新建伸缩组满足最小数（5）/修改伸缩组满足最大最小限制（6）/健康检查移入（7）/健康检查移出（8））--暂未提供  先不传
        :param group_id: 伸缩组ID --暂未提供 可不传
        """
        self.region_id = region_id
        self.rule_id = rule_id
        self.execution_mode = execution_mode
        self.group_id = group_id

    def set_execution_mode(self, execution_mode):
        """
        :param execution_mode: 执行方式（自动执行策略（1）/手动执行策略（2）/手动移入实例（3）/手动移出实例（4）/新建伸缩组满足最小数（5）/修改伸缩组满足最大最小限制（6）/健康检查移入（7）/健康检查移出（8））--暂未提供  先不传
        """
        self.execution_mode = execution_mode

    def set_group_id(self, group_id):
        """
        :param group_id: 伸缩组ID --暂未提供 可不传
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

