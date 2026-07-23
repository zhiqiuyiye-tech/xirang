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


class CloneVdcStrategyRequest(CTYunRequest):
    """
    克隆策略-VDC
    """

    def __init__(self, request_param):
        super(CloneVdcStrategyRequest, self).__init__("/v1/policy/vdc/cloneStrategy", "POST", "iam", "application/json")
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
        if self.parameters.strategy_name is not None:
            body_param["strategyName"] = self.parameters.strategy_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.strategy_id is not None:
            body_param["strategyID"] = self.parameters.strategy_id
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


class CloneVdcStrategyRequestParam(object):

    def __init__(self, strategy_name, strategy_id, description=None):
        """
        :param strategy_name: 策略名称
        :param description: 策略描述，0-100
        :param strategy_id: 克隆的原始策略id
        """
        self.strategy_name = strategy_name
        self.description = description
        self.strategy_id = strategy_id

    def set_description(self, description):
        """
        :param description: 策略描述，0-100
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.strategy_name is None:
            raise Exception("strategy_name can not None")
        if self.strategy_id is None:
            raise Exception("strategy_id can not None")

