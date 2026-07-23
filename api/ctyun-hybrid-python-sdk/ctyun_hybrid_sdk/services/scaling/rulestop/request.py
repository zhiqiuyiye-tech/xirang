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


class RuleStopRequest(CTYunRequest):
    """
    停用伸缩组中指定策略
    """

    def __init__(self, request_param):
        super(RuleStopRequest, self).__init__("/v4/scaling/rule/stop", "POST", "scaling", "application/json")
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


class RuleStopRequestParam(object):

    def __init__(self, region_id, rule_id, group_id=None):
        """
        :param region_id: 资源池ID
        :param rule_id: 报警任务ID（规则ID）
        :param group_id: 报警伸缩组ID 底层不支持groupID
        """
        self.region_id = region_id
        self.rule_id = rule_id
        self.group_id = group_id

    def set_group_id(self, group_id):
        """
        :param group_id: 报警伸缩组ID 底层不支持groupID
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

