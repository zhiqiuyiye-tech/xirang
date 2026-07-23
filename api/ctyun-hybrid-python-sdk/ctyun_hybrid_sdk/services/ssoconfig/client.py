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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class SsoconfigClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ssoconfig-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(SsoconfigClient, self).__init__(credential, config, 'ssoconfig', '0.1.0', logger, signer)

    def update_saml2_config(self, update_saml2_config_request_param):
        """
        /v1/auth/saml2/update
        更新SAML2登录平台认证
        """
        return self.send(update_saml2_config_request_param)

    def describe_cas_auths(self, describe_cas_auths_request_param):
        """
        /v1/auth/cas/list
        查询Cas认证服务配置列表
        """
        return self.send(describe_cas_auths_request_param)

    def delete_cas_config(self, delete_cas_config_request_param):
        """
        /v1/auth/cas/delete
        删除CAS登录平台配置
        """
        return self.send(delete_cas_config_request_param)

    def update_oauth_config(self, update_oauth_config_request_param):
        """
        /v1/auth/oauth/update
        更新OAuth登录平台认证
        """
        return self.send(update_oauth_config_request_param)

    def update_cas_config(self, update_cas_config_request_param):
        """
        /v1/auth/cas/update
        更新CAS登录平台认证
        """
        return self.send(update_cas_config_request_param)

    def create_cas_config(self, create_cas_config_request_param):
        """
        /v1/auth/cas/create
        创建CAS平台认证配置
        """
        return self.send(create_cas_config_request_param)

    def delete_s_a_m_l2_config(self, delete_s_a_m_l2_config_request_param):
        """
        /v1/auth/saml2/delete
        删除SAML2登录平台配置
        """
        return self.send(delete_s_a_m_l2_config_request_param)

    def create_oauth_config(self, create_oauth_config_request_param):
        """
        /v1/auth/oauth/create
        创建OAuth认证配置
        """
        return self.send(create_oauth_config_request_param)

    def describe_oauth_auths(self, describe_oauth_auths_request_param):
        """
        /v1/auth/oauth/list
        查询OAuth 2.0  SSO 认证配置列表
        """
        return self.send(describe_oauth_auths_request_param)

    def delete_oauth_config(self, delete_oauth_config_request_param):
        """
        /v1/auth/oauth/delete
        删除oauth 2.0 平台认证配置
        """
        return self.send(delete_oauth_config_request_param)

    def describe_s_a_m_l2_auths(self, describe_s_a_m_l2_auths_request_param):
        """
        /v1/auth/saml2/list
        查询OAuth 2.0  SSO 认证配置列表
        """
        return self.send(describe_s_a_m_l2_auths_request_param)

    def create_saml2_config(self, create_saml2_config_request_param):
        """
        /v1/auth/saml2/create
        创建SAML2.0 认证配置
        """
        return self.send(create_saml2_config_request_param)
