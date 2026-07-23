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


class CreateIPv6GatewayRequest(CTYunRequest):
    """
    创建ipv6网关
    """

    def __init__(self, request_param):
        super(CreateIPv6GatewayRequest, self).__init__("/v4/vpc/create-ipv6-gateway", "POST", "ctvpc", "application/json")
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


class CreateIPv6GatewayRequestParam(object):

    def __init__(self, region_id, vpc_id, client_token, description=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param vpc_id: VPC ID
        :param description: 描述信息，长度不超过50，支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头
        :param client_token: 客户端存根，公有云参数，对于私有云无意义，可随意填写
        :param project_id: 企业项目 ID，默认为"0"
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.description = description
        self.client_token = client_token
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述信息，长度不超过50，支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头
        """
        self.description = description

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为"0"
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

