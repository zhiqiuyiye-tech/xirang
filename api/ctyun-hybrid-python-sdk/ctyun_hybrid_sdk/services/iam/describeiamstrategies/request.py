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


class DescribeIamStrategiesRequest(CTYunRequest):
    """
    获取策略列表-IAM
    """

    def __init__(self, request_param):
        super(DescribeIamStrategiesRequest, self).__init__("/v1/policy/iam/queryStrategy", "POST", "iam", "application/json")
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
        if self.parameters.strategy_name is not None:
            body_param["strategyName"] = self.parameters.strategy_name
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.range is not None:
            body_param["range"] = self.parameters.range
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.region_type is not None:
            body_param["regionType"] = self.parameters.region_type
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


class DescribeIamStrategiesRequestParam(object):

    def __init__(self, page, page_size, strategy_name=None, range=None, type=None, region_type=None):
        """
        :param strategy_name: 策略名称
        :param page: 页码，最小1
        :param page_size: 页面大小 ，最小1，超过100默认为100
        :param range: 策略范围 1-全局 2-资源池
        :param type: 策略类型 1-系统 2-自定义
        :param region_type: 资源池类型，资源池类型可从接口/v1/regions/region-type获取
        """
        self.strategy_name = strategy_name
        self.page = page
        self.page_size = page_size
        self.range = range
        self.type = type
        self.region_type = region_type

    def set_strategy_name(self, strategy_name):
        """
        :param strategy_name: 策略名称
        """
        self.strategy_name = strategy_name

    def set_range(self, range):
        """
        :param range: 策略范围 1-全局 2-资源池
        """
        self.range = range

    def set_type(self, type):
        """
        :param type: 策略类型 1-系统 2-自定义
        """
        self.type = type

    def set_region_type(self, region_type):
        """
        :param region_type: 资源池类型，资源池类型可从接口/v1/regions/region-type获取
        """
        self.region_type = region_type

    def check_param(self):
        """
        the param required check
        """
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

