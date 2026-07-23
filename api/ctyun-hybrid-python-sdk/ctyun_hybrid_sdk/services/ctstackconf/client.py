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


class CtstackconfClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctstackconf-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtstackconfClient, self).__init__(credential, config, 'ctstackconf', '0.1.0', logger, signer)

    def delete_ip_black_list_config(self, delete_ip_black_list_config_request_param):
        """
        /v1/login-secure-blacklist/delete
        登录IP黑名单删除
        """
        return self.send(delete_ip_black_list_config_request_param)

    def add_ip_white_list_config(self, add_ip_white_list_config_request_param):
        """
        /v1/login-secure-whitelist/add
        登录IP白名单添加
        """
        return self.send(add_ip_white_list_config_request_param)

    def describe_ip_white_list_configs(self, describe_ip_white_list_configs_request_param):
        """
        /v1/login-secure-whitelist/list
        查询登录IP白名单配置列表
        """
        return self.send(describe_ip_white_list_configs_request_param)

    def reset_login_theme(self, reset_login_theme_request_param):
        """
        /v1/login-theme/reset
        重置登录页面主题配置，包括图片，系统图标
        """
        return self.send(reset_login_theme_request_param)

    def describe_ip_black_list_configs(self, describe_ip_black_list_configs_request_param):
        """
        /v1/login-secure-blacklist/list
        查询登录黑名单配置列表
        """
        return self.send(describe_ip_black_list_configs_request_param)

    def add_ip_black_list_config(self, add_ip_black_list_config_request_param):
        """
        /v1/login-secure-blacklist/add
        向IP黑名单中添加IP
        """
        return self.send(add_ip_black_list_config_request_param)

    def delete_ip_white_list_config(self, delete_ip_white_list_config_request_param):
        """
        /v1/login-secure-whitelist/delete
        登录IP白名单删除
        """
        return self.send(delete_ip_white_list_config_request_param)

    def update_ip_white_list_config(self, update_ip_white_list_config_request_param):
        """
        /v1/login-secure-whitelist/update
        登录IP白名单修改
        """
        return self.send(update_ip_white_list_config_request_param)

    def update_ip_black_list_config(self, update_ip_black_list_config_request_param):
        """
        /v1/login-secure-blacklist/update
        登录IP黑名单修改
        """
        return self.send(update_ip_black_list_config_request_param)
