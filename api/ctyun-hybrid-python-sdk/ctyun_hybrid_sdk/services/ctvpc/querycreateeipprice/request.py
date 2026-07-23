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


class QueryCreateEipPriceRequest(CTYunRequest):
    """
    调用此接口可查询创建弹性公网IP的价格，可以直接使用创建参数询价，对非询价所需字段不做校验，只做透传，混合云目前入参缺失bandwidthID，这个字段。非必填，暂不做调整。支持3.0   
    价格单位：按带宽 元/小时，按流量 元/GB
    """

    def __init__(self, request_param):
        super(QueryCreateEipPriceRequest, self).__init__("/v4/eip/query-create-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.demand_billing_type is not None:
            body_param["demandBillingType"] = self.parameters.demand_billing_type
        if self.parameters.provider is not None:
            body_param["provider"] = self.parameters.provider
        if self.parameters.bandwidth_id is not None:
            body_param["bandwidthID"] = self.parameters.bandwidth_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class QueryCreateEipPriceRequestParam(object):

    def __init__(self, region_id, cycle_type, client_token=None, cycle_count=None, bandwidth=None, demand_billing_type=None, provider=None, bandwidth_id=None, name=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        :param region_id: 资源池 ID
        :param cycle_type: 订购类型：month / year / on_demand
        :param cycle_count: 订阅时长，当 cycleType = on_demand 时，可以不传；订购类型为month / year时询价支持1以上
        :param bandwidth: 弹性 IP 的带宽峰值，传0或者不传默认为 1 Mbps,，默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        :param demand_billing_type: 按需计费类型，当 cycleType 为 on_demand 时生效，支持 bandwidth（按带宽）/ upflowc（按流量），不传时默认为bandwidth
        :param provider: 网络类型 ，非询价所需字段 
        :param bandwidth_id: 共享带宽ID，非询价所需字段
        :param name:  弹性 IP 名称，非询价所需字段
        """
        self.client_token = client_token
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.bandwidth = bandwidth
        self.demand_billing_type = demand_billing_type
        self.provider = provider
        self.bandwidth_id = bandwidth_id
        self.name = name

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        """
        self.client_token = client_token

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订阅时长，当 cycleType = on_demand 时，可以不传；订购类型为month / year时询价支持1以上
        """
        self.cycle_count = cycle_count

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 弹性 IP 的带宽峰值，传0或者不传默认为 1 Mbps,，默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        """
        self.bandwidth = bandwidth

    def set_demand_billing_type(self, demand_billing_type):
        """
        :param demand_billing_type: 按需计费类型，当 cycleType 为 on_demand 时生效，支持 bandwidth（按带宽）/ upflowc（按流量），不传时默认为bandwidth
        """
        self.demand_billing_type = demand_billing_type

    def set_provider(self, provider):
        """
        :param provider: 网络类型 ，非询价所需字段 
        """
        self.provider = provider

    def set_bandwidth_id(self, bandwidth_id):
        """
        :param bandwidth_id: 共享带宽ID，非询价所需字段
        """
        self.bandwidth_id = bandwidth_id

    def set_name(self, name):
        """
        :param name:  弹性 IP 名称，非询价所需字段
        """
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

