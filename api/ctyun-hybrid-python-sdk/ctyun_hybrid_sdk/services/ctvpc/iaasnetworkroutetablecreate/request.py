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


class IaasNetworkRouteTableCreateRequest(CTYunRequest):
    """
    创建路由表
    """

    def __init__(self, request_param):
        super(IaasNetworkRouteTableCreateRequest, self).__init__("/v4/vpc/route-table/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class IaasNetworkRouteTableCreateRequestParam(object):

    def __init__(self, region_id, vpc_id, name, description=None, client_token=None, project_id=None):
        """
        :param region_id: 区域id
        :param vpc_id: vpc（虚拟私有云） ID
        :param name: 路由表名称。长度为2-32个英文或中文字符。只能以中文或字母开头，仅支持中文、大小写字母、数字、-、_
        :param description: 路由表描述信息。长度为0-128个英文或中文字符，不能以http:或者https:开头，支持~!@#$%^&*()_+{}|:<>?-=[];,./~！@#￥%……&*（）——+{}：“《》？默认值：空
        :param client_token: 客户端存根,可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 企业项目id
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.name = name
        self.description = description
        self.client_token = client_token
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 路由表描述信息。长度为0-128个英文或中文字符，不能以http:或者https:开头，支持~!@#$%^&*()_+{}|:<>?-=[];,./~！@#￥%……&*（）——+{}：“《》？默认值：空
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根,可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

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
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.name is None:
            raise Exception("name can not None")

