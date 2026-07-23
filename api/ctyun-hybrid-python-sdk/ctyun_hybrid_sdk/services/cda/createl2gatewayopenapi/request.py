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


class CreateL2GatewayOpenapiRequest(CTYunRequest):
    """
    创建企业交换机
    """

    def __init__(self, request_param):
        super(CreateL2GatewayOpenapiRequest, self).__init__("/v4/l2gw/create", "POST", "cda", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.link_gw_type is not None:
            body_param["linkGwType"] = self.parameters.link_gw_type
        if self.parameters.link_gw_id is not None:
            body_param["linkGwID"] = self.parameters.link_gw_id
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.ip is not None:
            body_param["ip"] = self.parameters.ip
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.auto_renew is not None:
            body_param["autoRenew"] = self.parameters.auto_renew
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


class CreateL2GatewayOpenapiRequestParam(object):

    def __init__(self, region_id, name, vpc_id, link_gw_type, link_gw_id, subnet_id, cycle_type, spec, client_token=None, description=None, ip=None, cycle_count=None, auto_renew=None):
        """
        :param client_token: 客户端存根
        :param region_id: 资源池 ID
        :param name: 二层网关名称，由数字、字母、中文、-、_组成，不能以数字、_和-开头，长度限制2-32个字符
        :param description: 描述
        :param vpc_id: vpc id
        :param link_gw_type: 隧道连接方式 linegw：云专线 vpn：VPN
        :param link_gw_id: 关联网关
        :param subnet_id: 本端隧道子网
        :param ip: 本端隧道IP
        :param cycle_type: 订购类型：month（包月） / year（包年） / on_demand（按需）
        :param cycle_count: 订购时长，包年和包月时必填
        :param spec: 规格 STANDARD：标准版 ENHANCED：增强版 BASIC: 基础版
        :param auto_renew: 是否自动续订（公有云参数，混合云无实际意义）
        """
        self.client_token = client_token
        self.region_id = region_id
        self.name = name
        self.description = description
        self.vpc_id = vpc_id
        self.link_gw_type = link_gw_type
        self.link_gw_id = link_gw_id
        self.subnet_id = subnet_id
        self.ip = ip
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.spec = spec
        self.auto_renew = auto_renew

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_ip(self, ip):
        """
        :param ip: 本端隧道IP
        """
        self.ip = ip

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，包年和包月时必填
        """
        self.cycle_count = cycle_count

    def set_auto_renew(self, auto_renew):
        """
        :param auto_renew: 是否自动续订（公有云参数，混合云无实际意义）
        """
        self.auto_renew = auto_renew

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
        if self.link_gw_type is None:
            raise Exception("link_gw_type can not None")
        if self.link_gw_id is None:
            raise Exception("link_gw_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.spec is None:
            raise Exception("spec can not None")

