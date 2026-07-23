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


class ChangeVdcUserPasswordRequest(CTYunRequest):
    """
    VDC用户修改密码 
    """

    def __init__(self, request_param):
        super(ChangeVdcUserPasswordRequest, self).__init__("/v1/vdc/user/change-password", "POST", "iam", "application/json")
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


class ChangeVdcUserPasswordRequestParam(object):

    def __init__(self, password, user_id, ):
        """
        :param password: 长度为8-20字符，必须包含4项：大写字母+小写字母+数字+特殊字符，特殊字符仅支持~!@#$%&*()-_.
        :param user_id: 用户id
        """
        self.password = password
        self.user_id = user_id

    def check_param(self):
        """
        the param required check
        """
        if self.password is None:
            raise Exception("password can not None")
        if self.user_id is None:
            raise Exception("user_id can not None")

