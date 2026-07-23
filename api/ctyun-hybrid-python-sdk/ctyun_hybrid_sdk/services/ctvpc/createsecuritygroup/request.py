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


class CreateSecurityGroupRequest(CTYunRequest):
    """
    创建安全组。   
    安全组名称不允许重复   
    3.0vpcID无用
    """

    def __init__(self, request_param):
        super(CreateSecurityGroupRequest, self).__init__("/v4/vpc/create-security-group", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class CreateSecurityGroupRequestParam(object):

    def __init__(self, name, region_id, vpc_id=None, description=None, client_token=None, project_id=None):
        """
        :param name: 安全组名称 支持拉丁字母、中文、数字，下划线，连字符，中文 / 英文字母开头，长度 2 - 32
        :param region_id: 资源池ID
        :param vpc_id: VPC ID 4.0必传 3.0不传
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 企业项目ID
        """
        self.name = name
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.description = description
        self.client_token = client_token
        self.project_id = project_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: VPC ID 4.0必传 3.0不传
        """
        self.vpc_id = vpc_id

    def set_description(self, description):
        """
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

