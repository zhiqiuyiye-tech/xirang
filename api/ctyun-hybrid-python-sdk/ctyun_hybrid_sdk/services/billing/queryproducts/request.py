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


class QueryProductsRequest(CTYunRequest):
    """
    产品列表
    """

    def __init__(self, request_param):
        super(QueryProductsRequest, self).__init__("/v1/billing/queryProducts", "GET", "billing", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryProductsRequestParam(object):

    def __init__(self, name=None, status=None, page=None, page_size=None):
        """
        :param name: 产品名称（模糊搜索）
        :param status: 状态（1-上架；2-下架）
        :param page: 开始页(不传默认1)
        :param page_size: 分页大小(不传默认10)
        """
        self.name = name
        self.status = status
        self.page = page
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 产品名称（模糊搜索）
        """
        self.name = name

    def set_status(self, status):
        """
        :param status: 状态（1-上架；2-下架）
        """
        self.status = status

    def set_page(self, page):
        """
        :param page: 开始页(不传默认1)
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小(不传默认10)
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        pass

