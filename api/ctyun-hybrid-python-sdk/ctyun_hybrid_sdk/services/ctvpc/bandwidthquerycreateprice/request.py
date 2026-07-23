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


class BandwidthQueryCreatePriceRequest(CTYunRequest):
    """
    共享带宽创建询价
    """

    def __init__(self, request_param):
        super(BandwidthQueryCreatePriceRequest, self).__init__("/v4/bandwidth/query-create-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
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


class BandwidthQueryCreatePriceRequestParam(object):

    def __init__(self, region_id, bandwidth, cycle_type, client_token=None, cycle_count=None, name=None):
        """
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。
        :param region_id: 资源池id
        :param bandwidth: 共享带宽的带宽峰值，必须大于等于 5，且上限值定义为：默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        :param cycle_type: 订购类型：包年/包月订购，或按需订购。month / year / on_demand
        :param cycle_count: 包年/包月订购时为必传，按需时为非必传；订购时长, 当 cycleType = month, 支持询价1 - 11 个月; 当 cycleType = year, 支持询价 1 - 3 年
        :param name: 资源名称；长度为2-32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        """
        self.client_token = client_token
        self.region_id = region_id
        self.bandwidth = bandwidth
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.name = name

    def set_client_token(self, client_token):
        """
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。
        """
        self.client_token = client_token

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包年/包月订购时为必传，按需时为非必传；订购时长, 当 cycleType = month, 支持询价1 - 11 个月; 当 cycleType = year, 支持询价 1 - 3 年
        """
        self.cycle_count = cycle_count

    def set_name(self, name):
        """
        :param name: 资源名称；长度为2-32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        """
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

