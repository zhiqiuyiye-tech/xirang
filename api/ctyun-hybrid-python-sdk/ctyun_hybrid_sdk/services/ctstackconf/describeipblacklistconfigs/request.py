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


class DescribeIPBlackListConfigsRequest(CTYunRequest):
    """
    查询登录黑名单配置列表
    """

    def __init__(self, request_param):
        super(DescribeIPBlackListConfigsRequest, self).__init__("/v1/login-secure-blacklist/list", "GET", "ctstackconf", "")
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
        if self.parameters.ip is not None:
            query_param["ip"] = self.parameters.ip
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


class DescribeIPBlackListConfigsRequestParam(object):

    def __init__(self, ip=None, page=None, page_size=None):
        """
        :param ip: 添加黑名单ip
        :param page: 页码，默认值1
        :param page_size: 每页数量，默认值10
        """
        self.ip = ip
        self.page = page
        self.page_size = page_size

    def set_ip(self, ip):
        """
        :param ip: 添加黑名单ip
        """
        self.ip = ip

    def set_page(self, page):
        """
        :param page: 页码，默认值1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页数量，默认值10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        pass

