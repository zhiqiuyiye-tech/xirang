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


class GetL2ConnectionListOpenapiRequest(CTYunRequest):
    """
    查询二层连接列表
    """

    def __init__(self, request_param):
        super(GetL2ConnectionListOpenapiRequest, self).__init__("/v4/l2gw_connection/query", "GET", "cda", "")
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
        if self.parameters.l2gw_id is not None:
            query_param["l2gwID"] = self.parameters.l2gw_id
        if self.parameters.l2_connection_id is not None:
            query_param["l2ConnectionID"] = self.parameters.l2_connection_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetL2ConnectionListOpenapiRequestParam(object):

    def __init__(self, region_id, l2gw_id=None, l2_connection_id=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param l2gw_id: 企业交换机ID
        :param l2_connection_id: 二层连接ID
        :param page_no: 列表的页码，默认值为 1，传参小于0时默认1
        :param page_size: 分页查询时每页的行数，最大值为 50，默认值为 10。传参小于0时默认10
        """
        self.region_id = region_id
        self.l2gw_id = l2gw_id
        self.l2_connection_id = l2_connection_id
        self.page_no = page_no
        self.page_size = page_size

    def set_l2gw_id(self, l2gw_id):
        """
        :param l2gw_id: 企业交换机ID
        """
        self.l2gw_id = l2gw_id

    def set_l2_connection_id(self, l2_connection_id):
        """
        :param l2_connection_id: 二层连接ID
        """
        self.l2_connection_id = l2_connection_id

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的页码，默认值为 1，传参小于0时默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页的行数，最大值为 50，默认值为 10。传参小于0时默认10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

