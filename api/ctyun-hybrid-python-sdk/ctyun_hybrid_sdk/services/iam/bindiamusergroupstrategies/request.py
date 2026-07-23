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


class BindIAMUserGroupStrategiesRequest(CTYunRequest):
    """
    IAM认证-用户组绑定策略
    """

    def __init__(self, request_param):
        super(BindIAMUserGroupStrategiesRequest, self).__init__("/v1/userGroup/iam/bind-strategies", "POST", "iam", "application/json")
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
        if self.parameters.strategy_ids is not None:
            body_param["strategyIDs"] = self.parameters.strategy_ids
        if self.parameters.range is not None:
            body_param["range"] = self.parameters.range
        if self.parameters.auth_region_id is not None:
            body_param["authRegionID"] = self.parameters.auth_region_id
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


class BindIAMUserGroupStrategiesRequestParam(object):

    def __init__(self, strategy_ids, range, group_id, auth_region_id=None):
        """
        :param strategy_ids: 策略id 注意:此参数为数组
        :param range: 策略授权范围 范围 1-全局 2-资源池
        :param auth_region_id: 资源池id，策略为资源池时必填 注意:此参数为数组
        :param group_id: 用户组id
        """
        self.strategy_ids = strategy_ids
        self.range = range
        self.auth_region_id = auth_region_id
        self.group_id = group_id

    def set_auth_region_id(self, auth_region_id):
        """
        :param auth_region_id: 资源池id，策略为资源池时必填
        """
        self.auth_region_id = auth_region_id

    def check_param(self):
        """
        the param required check
        """
        if self.strategy_ids is None:
            raise Exception("strategy_ids can not None")
        if self.range is None:
            raise Exception("range can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

