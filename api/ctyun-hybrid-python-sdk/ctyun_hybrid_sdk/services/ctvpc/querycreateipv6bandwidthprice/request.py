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


class QueryCreateIpv6BandwidthPriceRequest(CTYunRequest):
    """
    非必需询价字段不做校验，只透传
    """

    def __init__(self, request_param):
        super(QueryCreateIpv6BandwidthPriceRequest, self).__init__("/v4/ipv6_bandwidth/query-create-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class QueryCreateIpv6BandwidthPriceRequestParam(object):

    def __init__(self, region_id, cycle_type, bandwidth, client_token=None, cycle_count=None, name=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        :param region_id: 创建共享带宽的区域id。
        :param cycle_type: 订购类型：包年/包月订购 month / year，或按需订购/on_demand。
        :param bandwidth: IPV6带宽的带宽峰值，最小值1，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准。
        :param cycle_count: 订购类型为包年/包月订购 month / year时，必填。当 cycleType = month, 支持 1 - 11 个月; 当 cycleType = year, 支持 1 - 5年
        :param name: 非必需询价字段 共享带宽名称
        """
        self.client_token = client_token
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.bandwidth = bandwidth
        self.cycle_count = cycle_count
        self.name = name

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        """
        self.client_token = client_token

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购类型为包年/包月订购 month / year时，必填。当 cycleType = month, 支持 1 - 11 个月; 当 cycleType = year, 支持 1 - 5年
        """
        self.cycle_count = cycle_count

    def set_name(self, name):
        """
        :param name: 非必需询价字段 共享带宽名称
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
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")

