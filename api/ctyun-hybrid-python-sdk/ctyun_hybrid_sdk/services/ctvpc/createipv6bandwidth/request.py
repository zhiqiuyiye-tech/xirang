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


class CreateIPv6BandwidthRequest(CTYunRequest):
    """
    创建IPV6带宽
    """

    def __init__(self, request_param):
        super(CreateIPv6BandwidthRequest, self).__init__("/v4/ipv6_bandwidth/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
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


class CreateIPv6BandwidthRequestParam(object):

    def __init__(self, region_id, name, cycle_type, client_token=None, cycle_count=None, bandwidth=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性（传值则会校验））
        :param region_id: 创建IPV6带宽的区域id。
        :param name: 长度为2～32字符   
         支持使用字母、数字、中划线（-）、下划线（_)，只能以字母开头、以数字或字母结尾。不允许重名
        :param cycle_type: 订购类型：包年/包月订购 month / year，或按需订购on_demand
        :param cycle_count: 订购类型为包年/包月订购 month / year时，必填。当 cycleType = month, 支持 1 - 11 个月; 当 cycleType = year, 支持 1 - 5年
        :param bandwidth: IPV6带宽的带宽峰值，如果不传默认是 1，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准。
        """
        self.client_token = client_token
        self.region_id = region_id
        self.name = name
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.bandwidth = bandwidth

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性（传值则会校验））
        """
        self.client_token = client_token

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购类型为包年/包月订购 month / year时，必填。当 cycleType = month, 支持 1 - 11 个月; 当 cycleType = year, 支持 1 - 5年
        """
        self.cycle_count = cycle_count

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: IPV6带宽的带宽峰值，如果不传默认是 1，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准。
        """
        self.bandwidth = bandwidth

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

