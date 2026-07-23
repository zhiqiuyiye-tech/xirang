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


class ListSnatsRequest(CTYunRequest):
    """
    获取SNAT规则列表
    """

    def __init__(self, request_param):
        super(ListSnatsRequest, self).__init__("/v4/vpc/list-snats", "GET", "ctvpc", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.nat_gateway_id is not None:
            query_param["natGatewayID"] = self.parameters.nat_gateway_id
        if self.parameters.s_nat_id is not None:
            query_param["sNatID"] = self.parameters.s_nat_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListSnatsRequestParam(object):

    def __init__(self, region_id, nat_gateway_id=None, s_nat_id=None, subnet_id=None, page_number=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param nat_gateway_id: 网关ID
        :param s_nat_id: SNAT规则ID
        :param subnet_id: 子网ID
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.s_nat_id = s_nat_id
        self.subnet_id = subnet_id
        self.page_number = page_number
        self.page_size = page_size

    def set_nat_gateway_id(self, nat_gateway_id):
        """
        :param nat_gateway_id: 网关ID
        """
        self.nat_gateway_id = nat_gateway_id

    def set_s_nat_id(self, s_nat_id):
        """
        :param s_nat_id: SNAT规则ID
        """
        self.s_nat_id = s_nat_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网ID
        """
        self.subnet_id = subnet_id

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

