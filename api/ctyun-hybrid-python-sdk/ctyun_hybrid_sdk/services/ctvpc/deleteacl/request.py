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


class DeleteAclRequest(CTYunRequest):
    """
    删除acl
    """

    def __init__(self, request_param):
        super(DeleteAclRequest, self).__init__("/v4/acl/delete", "POST", "ctvpc", "application/json")
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
        if self.parameters.acl_id is not None:
            body_param["aclID"] = self.parameters.acl_id
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


class DeleteAclRequestParam(object):

    def __init__(self, region_id, acl_id, client_token=None):
        """
        :param region_id: 资源池ID
        :param acl_id: ACL ID
        :param client_token: 对齐公有云参数，非必传
        """
        self.region_id = region_id
        self.acl_id = acl_id
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 对齐公有云参数，非必传
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.acl_id is None:
            raise Exception("acl_id can not None")

