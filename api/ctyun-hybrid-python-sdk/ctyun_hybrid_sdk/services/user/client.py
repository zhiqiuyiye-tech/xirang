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


class UserClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('user-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(UserClient, self).__init__(credential, config, 'user', '0.1.0', logger, signer)

    def list_vdc_hybrid(self, list_vdc_hybrid_request_param):
        """
        /v4/vdc/list-vdc
        查询所有VDC组织列表
        """
        return self.send(list_vdc_hybrid_request_param)

    def create_vdc_hybrid_hub(self, create_vdc_hybrid_hub_request_param):
        """
        /v4/vdc/hub/create-vdc
        创建VDC组织-hub
        """
        return self.send(create_vdc_hybrid_hub_request_param)

    def create_user_hub(self, create_user_hub_request_param):
        """
        /v4/user/hub/create
        密码使用SM4-CBC算法加密,pcks5填充   
    key是登录名做sha256
        """
        return self.send(create_user_hub_request_param)

    def user_page_list_hybrid(self, user_page_list_hybrid_request_param):
        """
        /v4/user/page-user-list
        分页查询用户信息，需要注意v2 的openapi 子账号和主账号获取的资源是重复的，主账号有当前vdc下所有资源的权限，如果使用用户id获取资源只需要是用主账号即可，主子账号及企业账号使用请求返回值 userType 判断即可
        """
        return self.send(user_page_list_hybrid_request_param)

    def change_user_password_hub(self, change_user_password_hub_request_param):
        """
        /v4/user/hub/change-password
        密码使用SM4-CBC算法加密,pcks5填充   
    key是登录名做sha256
        """
        return self.send(change_user_password_hub_request_param)
