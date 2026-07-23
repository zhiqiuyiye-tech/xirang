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


class QueryEbmMemTopHybridRequest(CTYunRequest):
    """
    调用此接口可查询用户在指定资源池裸金属监控中内存使用率Top-N。
    """

    def __init__(self, request_param):
        super(QueryEbmMemTopHybridRequest, self).__init__("/v4/monitor/query-baremetal-mem-top", "POST", "monitor", "application/json")
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
        if self.parameters.number is not None:
            body_param["number"] = self.parameters.number
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


class QueryEbmMemTopHybridRequestParam(object):

    def __init__(self, region_id, number=None):
        """
        :param region_id: 资源池ID	
        :param number: 选取TOP值的数量，不传默认为3，最大值为20，当传入值或默认值超过用户实际拥有的资源数量，以用户的实际资源数量为准	
        """
        self.region_id = region_id
        self.number = number

    def set_number(self, number):
        """
        :param number: 选取TOP值的数量，不传默认为3，最大值为20，当传入值或默认值超过用户实际拥有的资源数量，以用户的实际资源数量为准	
        """
        self.number = number

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

