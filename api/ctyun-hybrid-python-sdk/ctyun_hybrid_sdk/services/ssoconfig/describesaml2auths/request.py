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


class DescribeSAML2AuthsRequest(CTYunRequest):
    """
    查询OAuth 2.0  SSO 认证配置列表
    """

    def __init__(self, request_param):
        super(DescribeSAML2AuthsRequest, self).__init__("/v1/auth/saml2/list", "GET", "ssoconfig", "")
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
        if self.parameters.issuer is not None:
            query_param["issuer"] = self.parameters.issuer
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeSAML2AuthsRequestParam(object):

    def __init__(self, page=None, page_size=None, issuer=None, name=None):
        """
        :param page: 分页页码
        :param page_size: 分页每页数量最大100
        :param issuer: SAML2 认证签发人
        :param name: 平台名称
        """
        self.page = page
        self.page_size = page_size
        self.issuer = issuer
        self.name = name

    def set_page(self, page):
        """
        :param page: 分页页码
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 分页每页数量最大100
        """
        self.page_size = page_size

    def set_issuer(self, issuer):
        """
        :param issuer: SAML2 认证签发人
        """
        self.issuer = issuer

    def set_name(self, name):
        """
        :param name: 平台名称
        """
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        pass

