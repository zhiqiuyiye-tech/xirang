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


class CreateGatewayRouteTableRequest(CTYunRequest):
    """
    创建网关路由表   
    ## 公有云差别   
    * clientToken公有云必填字段，字段不影响接口功能，混合云不必填当作对齐。   此接口仅支持4.0
    """

    def __init__(self, request_param):
        super(CreateGatewayRouteTableRequest, self).__init__("/v4/vpc/route-table/create-gateway-routetable", "POST", "ctvpc", "application/json")
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


class CreateGatewayRouteTableRequestParam(object):

    def __init__(self, region_id, vpc_id, name, description=None, client_token=None):
        """
        :param region_id: 区域id
        :param vpc_id: vpc ID
        :param name: 路由表名称。长度为2-32个英文或中文字符。只能以中文或字母开头，仅支持中文、大小写字母、数字、-、_
        :param description: 路由表描述信息。支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param client_token: 可传但是不进行校验, 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.name = name
        self.description = description
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: 路由表描述信息。支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验, 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

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

