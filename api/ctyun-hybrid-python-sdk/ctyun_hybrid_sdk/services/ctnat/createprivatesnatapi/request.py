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


class CreatePrivateSnatApiRequest(CTYunRequest):
    """
    创建私网SNAT规则。snatIps需填入中转IP的地址。sourceSubnetID和sourceCIDR必须传一个，都传以子网ID为准。
    """

    def __init__(self, request_param):
        super(CreatePrivateSnatApiRequest, self).__init__("/v4/privatenat/create-snat", "POST", "ctnat", "application/json")
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
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
        if self.parameters.source_subnet_id is not None:
            body_param["sourceSubnetID"] = self.parameters.source_subnet_id
        if self.parameters.source_cidr is not None:
            body_param["sourceCIDR"] = self.parameters.source_cidr
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.snat_ips is not None:
            body_param["snatIps"] = self.parameters.snat_ips
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


class CreatePrivateSnatApiRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, snat_ips, source_subnet_id=None, source_cidr=None, description=None, client_token=None):
        """
        :param region_id: 资源池id
        :param nat_gateway_id: NAT网关ID
        :param source_subnet_id: 子网id sourceCIDR和sourceSubnetID二选一必传
        :param source_cidr: 自定义输入VPC、交换机或ECS实例的网段，还可以输入任意网段 sourceCIDR和sourceSubnetID二选一必传
        :param description: 描述
        :param snat_ips: 中转IP的地址列表 注意:此参数为数组
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.source_subnet_id = source_subnet_id
        self.source_cidr = source_cidr
        self.description = description
        self.snat_ips = snat_ips
        self.client_token = client_token

    def set_source_subnet_id(self, source_subnet_id):
        """
        :param source_subnet_id: 子网id sourceCIDR和sourceSubnetID二选一必传
        """
        self.source_subnet_id = source_subnet_id

    def set_source_cidr(self, source_cidr):
        """
        :param source_cidr: 自定义输入VPC、交换机或ECS实例的网段，还可以输入任意网段 sourceCIDR和sourceSubnetID二选一必传
        """
        self.source_cidr = source_cidr

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")
        if self.snat_ips is None:
            raise Exception("snat_ips can not None")

