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


class DeleteSecurityGroupRequest(CTYunRequest):
    """
    删除安全组。删除安全组之前，请确保安全组内不存在实例。
    """

    def __init__(self, request_param):
        super(DeleteSecurityGroupRequest, self).__init__("/v4/vpc/delete-security-group", "POST", "ctvpc", "application/json")
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
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
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


class DeleteSecurityGroupRequestParam(object):

    def __init__(self, security_group_id, region_id, client_token=None):
        """
        :param security_group_id: 安全组 ID
        :param region_id: 资源池 ID
        :param client_token: 内容不进行校验，客户端存根（此字段在私有云不具有实际意义）
        """
        self.security_group_id = security_group_id
        self.region_id = region_id
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 内容不进行校验，客户端存根（此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.security_group_id is None:
            raise Exception("security_group_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

