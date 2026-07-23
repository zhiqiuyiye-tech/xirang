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


class CtvpnGatewayNewRequest(CTYunRequest):
    """
    VPN网关订购
    """

    def __init__(self, request_param):
        super(CtvpnGatewayNewRequest, self).__init__("/v4/vpn/gateway/new", "POST", "ctvpn", "application/json")
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
        if self.parameters.vpc_id is not None:
            body_param["vpcId"] = self.parameters.vpc_id
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.connection_limit is not None:
            body_param["connectionLimit"] = self.parameters.connection_limit
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.local_subnet_ids is not None:
            body_param["localSubnetIDs"] = self.parameters.local_subnet_ids
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


class CtvpnGatewayNewRequestParam(object):

    def __init__(self, region_id, name, vpc_id, bandwidth, connection_limit, client_token=None, on_demand=None, cycle_type=None, cycle_count=None, description=None, local_subnet_ids=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性
        :param region_id: 资源池id
        :param name: VPN网关名称，长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param vpc_id: VPC ID
        :param bandwidth: 带宽大小
        :param connection_limit: VPN网关连接数限制
        :param on_demand: 是否按需下单。默认为False
        :param cycle_type: 包周期类型，YEAR/MONTH。onDemand为False时，必须指定
        :param cycle_count: 包周期数。onDemand为False时必须指定。周期最大长度不能超过36个月
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param local_subnet_ids: vpn网关本端子网列表，vpn底座高版本必传参数，低版本忽略 注意:此参数为数组
        """
        self.client_token = client_token
        self.region_id = region_id
        self.name = name
        self.vpc_id = vpc_id
        self.bandwidth = bandwidth
        self.connection_limit = connection_limit
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.description = description
        self.local_subnet_ids = local_subnet_ids

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性
        """
        self.client_token = client_token

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需下单。默认为False
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期类型，YEAR/MONTH。onDemand为False时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数。onDemand为False时必须指定。周期最大长度不能超过36个月
        """
        self.cycle_count = cycle_count

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_local_subnet_ids(self, local_subnet_ids):
        """
        :param local_subnet_ids: vpn网关本端子网列表，vpn底座高版本必传参数，低版本忽略
        """
        self.local_subnet_ids = local_subnet_ids

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
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.connection_limit is None:
            raise Exception("connection_limit can not None")

