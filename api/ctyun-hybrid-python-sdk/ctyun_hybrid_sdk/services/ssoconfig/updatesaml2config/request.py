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


class UpdateSaml2ConfigRequest(CTYunRequest):
    """
    更新SAML2登录平台认证
    """

    def __init__(self, request_param):
        super(UpdateSaml2ConfigRequest, self).__init__("/v1/auth/saml2/update", "POST", "ssoconfig", "application/json")
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
        if self.parameters.issuer is not None:
            body_param["issuer"] = self.parameters.issuer
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.id is not None:
            body_param["id"] = self.parameters.id
        if self.parameters.sp_metadata is not None:
            body_param["spMetadata"] = self.parameters.sp_metadata
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


class UpdateSaml2ConfigRequestParam(object):

    def __init__(self, name, id, sp_metadata, issuer=None):
        """
        :param issuer: saml2 认证issuer  长度最长200,如果不填默认取spMetadata字段的entityID
        :param name: 平台名称 长度2到63
        :param id: 平台配置id
        :param sp_metadata: 客户端元数据配置文件
        """
        self.issuer = issuer
        self.name = name
        self.id = id
        self.sp_metadata = sp_metadata

    def set_issuer(self, issuer):
        """
        :param issuer: saml2 认证issuer  长度最长200,如果不填默认取spMetadata字段的entityID
        """
        self.issuer = issuer

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.sp_metadata is None:
            raise Exception("sp_metadata can not None")

