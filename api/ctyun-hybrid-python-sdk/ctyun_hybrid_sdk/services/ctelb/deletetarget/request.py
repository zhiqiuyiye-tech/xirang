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


class DeleteTargetRequest(CTYunRequest):
    """
    删除后端服务
    """

    def __init__(self, request_param):
        super(DeleteTargetRequest, self).__init__("/v4/elb/delete-target", "POST", "ctelb", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.target_id is not None:
            body_param["targetID"] = self.parameters.target_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class DeleteTargetRequestParam(object):

    def __init__(self, region_id, id=None, target_id=None, client_token=None):
        """
        :param region_id: 区域ID
        :param id: 后端服务ID, 该字段后续废弃
        :param target_id: 后端服务ID, 推荐使用该字段, 当同时使用 ID 和 targetID 时，优先使用 targetID
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.id = id
        self.target_id = target_id
        self.client_token = client_token

    def set_id(self, id):
        """
        :param id: 后端服务ID, 该字段后续废弃
        """
        self.id = id

    def set_target_id(self, target_id):
        """
        :param target_id: 后端服务ID, 推荐使用该字段, 当同时使用 ID 和 targetID 时，优先使用 targetID
        """
        self.target_id = target_id

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

