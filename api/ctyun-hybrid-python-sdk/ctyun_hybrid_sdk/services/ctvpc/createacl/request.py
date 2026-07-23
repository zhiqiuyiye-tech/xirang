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


class CreateAclRequest(CTYunRequest):
    """
    创建acl，ACL的名称不能重名
    """

    def __init__(self, request_param):
        super(CreateAclRequest, self).__init__("/v4/acl/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
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


class CreateAclRequestParam(object):

    def __init__(self, region_id, name, vpc_id, client_token, description=None, subnet_id=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param name: 长度为2-32位，支持英文字母、中文、数字、特殊符号_(下划线) -(中划线) /(斜杠) ，中文/英文字母开头
        :param vpc_id: vpc ID
        :param description: 描述，长度为0-50字符   
         支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        :param client_token: 与公有云对齐，对于云管无意义，可以随意填写
        :param subnet_id: 子网ID，3.0及轻量云资源池必填
        :param project_id: 企业项目id
        """
        self.region_id = region_id
        self.name = name
        self.vpc_id = vpc_id
        self.description = description
        self.client_token = client_token
        self.subnet_id = subnet_id
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述，长度为0-50字符   
         支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        """
        self.description = description

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网ID，3.0及轻量云资源池必填
        """
        self.subnet_id = subnet_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

