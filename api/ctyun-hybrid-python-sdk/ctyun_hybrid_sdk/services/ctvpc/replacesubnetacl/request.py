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


class ReplaceSubnetAclRequest(CTYunRequest):
    """
    子网更换ACL
    """

    def __init__(self, request_param):
        super(ReplaceSubnetAclRequest, self).__init__("/v4/vpc/replace-subnet-acl", "POST", "ctvpc", "application/json")
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
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.acl_id is not None:
            body_param["aclID"] = self.parameters.acl_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class ReplaceSubnetAclRequestParam(object):

    def __init__(self, region_id, subnet_id, acl_id, client_token=None, az_name=None, project_id=None):
        """
        :param region_id: 资源池 ID
        :param subnet_id: 子网 的 ID
        :param acl_id: acl 的 ID
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param az_name: 可用区名称（2.0该参数无意义）
        :param project_id: 企业项目 ID
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.acl_id = acl_id
        self.client_token = client_token
        self.az_name = az_name
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（2.0该参数无意义）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.acl_id is None:
            raise Exception("acl_id can not None")

