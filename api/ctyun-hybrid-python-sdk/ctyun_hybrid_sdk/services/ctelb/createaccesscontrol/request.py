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


class CreateAccessControlRequest(CTYunRequest):
    """
    创建策略地址组，策略地址组为被访问控制的黑白名单调用的地址组。
    """

    def __init__(self, request_param):
        super(CreateAccessControlRequest, self).__init__("/v4/elb/create-access-control", "POST", "ctelb", "application/json")
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
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.source_ips is not None:
            body_param["sourceIps"] = self.parameters.source_ips
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


class CreateAccessControlRequestParam(object):

    def __init__(self, name, region_id, source_ips, description=None, client_token=None, project_id=None):
        """
        :param name: 访问控制名称,只能由数字，字母，-组成不能以数字和-开头，最大长度32
        :param description: 描述，长度为0-128字符，支持使用中文、字母、数字、特殊符号~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，，
        :param region_id: 区域ID
        :param source_ips: IP地址的集合或者CIDR 注意:此参数为数组
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。可传但是不进行校验。（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 企业项目ID
        """
        self.name = name
        self.description = description
        self.region_id = region_id
        self.source_ips = source_ips
        self.client_token = client_token
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述，长度为0-128字符，支持使用中文、字母、数字、特殊符号~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，，
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。可传但是不进行校验。（非必填，并且此字段在私有云不具有实际意义）
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
        if self.source_ips is None:
            raise Exception("source_ips can not None")

