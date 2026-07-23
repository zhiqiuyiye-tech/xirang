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


class TransferCidrApiListRequest(CTYunRequest):
    """
    获取中转地址段
    """

    def __init__(self, request_param):
        super(TransferCidrApiListRequest, self).__init__("/v4/privatenat/list-cidrs", "GET", "ctnat", "")
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


class TransferCidrApiListRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, page_number=None, page_size=None):
        """
        :param region_id: 
        :param nat_gateway_id: 
        :param page_number: 列表的页码，默认值为1。
        :param page_size: 分页查询时每页的行数，最大值为100，超过按照100查询，默认值为10。
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.page_number = page_number
        self.page_size = page_size

    def set_page_number(self, page_number):
        """
        :param page_number: 列表的页码，默认值为1。
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页的行数，最大值为100，超过按照100查询，默认值为10。
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")

