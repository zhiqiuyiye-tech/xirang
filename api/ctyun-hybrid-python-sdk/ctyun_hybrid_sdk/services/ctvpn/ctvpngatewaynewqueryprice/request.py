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


class CtvpnGatewayNewQueryPriceRequest(CTYunRequest):
    """
    VPN网关订购询价
    """

    def __init__(self, request_param):
        super(CtvpnGatewayNewQueryPriceRequest, self).__init__("/v4/vpn/gateway/query-price-new", "POST", "ctvpn", "application/json")
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
        if self.parameters.count is not None:
            body_param["count"] = self.parameters.count
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


class CtvpnGatewayNewQueryPriceRequestParam(object):

    def __init__(self, region_id, bandwidth, connection_limit, cycle_type, cycle_count, count, client_token=None, on_demand=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性
        :param region_id: 资源池id
        :param bandwidth: 带宽大小
        :param connection_limit: VPN网关连接数限制
        :param on_demand: 是否按需下单。默认为False
        :param cycle_type: 包周期类型，YEAR/MONTH。onDemand为False时，必须指定
        :param cycle_count: 包周期数。onDemand为False时必须指定。周期最大长度不能超过36个月
        :param count: 批量下单数量，最大值10
        """
        self.client_token = client_token
        self.region_id = region_id
        self.bandwidth = bandwidth
        self.connection_limit = connection_limit
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.count = count

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

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.connection_limit is None:
            raise Exception("connection_limit can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")
        if self.count is None:
            raise Exception("count can not None")

