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


class CreateOAuthConfigRequest(CTYunRequest):
    """
    创建OAuth认证配置
    """

    def __init__(self, request_param):
        super(CreateOAuthConfigRequest, self).__init__("/v1/auth/oauth/create", "POST", "ssoconfig", "application/json")
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
        if self.parameters.domain is not None:
            body_param["domain"] = self.parameters.domain
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


class CreateOAuthConfigRequestParam(object):

    def __init__(self, domain, name, ):
        """
        :param domain:  长度最大200
        :param name: 长度为2到63
        """
        self.domain = domain
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.domain is None:
            raise Exception("domain can not None")
        if self.name is None:
            raise Exception("name can not None")

