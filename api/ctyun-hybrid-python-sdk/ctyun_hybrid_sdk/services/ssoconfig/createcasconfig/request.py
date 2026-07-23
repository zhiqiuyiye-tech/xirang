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


class CreateCasConfigRequest(CTYunRequest):
    """
    创建CAS平台认证配置
    """

    def __init__(self, request_param):
        super(CreateCasConfigRequest, self).__init__("/v1/auth/cas/create", "POST", "ssoconfig", "application/json")
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
        if self.parameters.cas_service_urls is not None:
            body_param["casServiceUrls"] = self.parameters.cas_service_urls
        if self.parameters.cas_service_logout_url is not None:
            body_param["casServiceLogoutURL"] = self.parameters.cas_service_logout_url
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


class CreateCasConfigRequestParam(object):

    def __init__(self, cas_service_urls, name, cas_service_logout_url=None):
        """
        :param cas_service_urls: 长度最大200
        :param cas_service_logout_url: 长度最大200
        :param name: 长度为2到63
        """
        self.cas_service_urls = cas_service_urls
        self.cas_service_logout_url = cas_service_logout_url
        self.name = name

    def set_cas_service_logout_url(self, cas_service_logout_url):
        """
        :param cas_service_logout_url: 长度最大200
        """
        self.cas_service_logout_url = cas_service_logout_url

    def check_param(self):
        """
        the param required check
        """
        if self.cas_service_urls is None:
            raise Exception("cas_service_urls can not None")
        if self.name is None:
            raise Exception("name can not None")

