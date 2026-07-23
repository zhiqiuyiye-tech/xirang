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


class ChangeUserPasswordHubRequest(CTYunRequest):
    """
    密码使用SM4-CBC算法加密,pcks5填充   
    key是登录名做sha256
    """

    def __init__(self, request_param):
        super(ChangeUserPasswordHubRequest, self).__init__("/v4/user/hub/change-password", "POST", "user", "application/json")
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
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.password_confirm is not None:
            body_param["passwordConfirm"] = self.parameters.password_confirm
        if self.parameters.user_id is not None:
            body_param["userID"] = self.parameters.user_id
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


class ChangeUserPasswordHubRequestParam(object):

    def __init__(self, password, password_confirm, user_id, ):
        """
        :param password: 密码
        :param password_confirm: 密码确认
        :param user_id: 用户id
        """
        self.password = password
        self.password_confirm = password_confirm
        self.user_id = user_id

    def check_param(self):
        """
        the param required check
        """
        if self.password is None:
            raise Exception("password can not None")
        if self.password_confirm is None:
            raise Exception("password_confirm can not None")
        if self.user_id is None:
            raise Exception("user_id can not None")

