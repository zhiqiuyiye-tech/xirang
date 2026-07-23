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


class DescribeCasAuthsRequest(CTYunRequest):
    """
    查询Cas认证服务配置列表
    """

    def __init__(self, request_param):
        super(DescribeCasAuthsRequest, self).__init__("/v1/auth/cas/list", "GET", "ssoconfig", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.cas_service_urls is not None:
            query_param["casServiceUrls"] = self.parameters.cas_service_urls
        if self.parameters.cas_service_logout_url is not None:
            query_param["casServiceLogoutURL"] = self.parameters.cas_service_logout_url
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeCasAuthsRequestParam(object):

    def __init__(self, page=None, page_size=None, name=None, cas_service_urls=None, cas_service_logout_url=None):
        """
        :param page: 页码
        :param page_size: 分页大小，最大100
        :param name: 平台名称
        :param cas_service_urls: cas 认证服务地址
        :param cas_service_logout_url: cas服务登出url
        """
        self.page = page
        self.page_size = page_size
        self.name = name
        self.cas_service_urls = cas_service_urls
        self.cas_service_logout_url = cas_service_logout_url

    def set_page(self, page):
        """
        :param page: 页码
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小，最大100
        """
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 平台名称
        """
        self.name = name

    def set_cas_service_urls(self, cas_service_urls):
        """
        :param cas_service_urls: cas 认证服务地址
        """
        self.cas_service_urls = cas_service_urls

    def set_cas_service_logout_url(self, cas_service_logout_url):
        """
        :param cas_service_logout_url: cas服务登出url
        """
        self.cas_service_logout_url = cas_service_logout_url

    def check_param(self):
        """
        the param required check
        """
        pass

