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


class UpdateShieldRuleStatusHybridRequest(CTYunRequest):
    """
    修改告警屏蔽规则状态
    """

    def __init__(self, request_param):
        super(UpdateShieldRuleStatusHybridRequest, self).__init__("/v4/monitor/update-shield-rule-status", "POST", "monitor", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
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


class UpdateShieldRuleStatusHybridRequestParam(object):

    def __init__(self, id, status, ):
        """
        :param id: 告警屏蔽规则ID
        :param status: 0 停用；1启用
        """
        self.id = id
        self.status = status

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.status is None:
            raise Exception("status can not None")

