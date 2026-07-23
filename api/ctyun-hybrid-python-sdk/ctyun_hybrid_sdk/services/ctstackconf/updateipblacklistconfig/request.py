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


class UpdateIPBlackListConfigRequest(CTYunRequest):
    """
    登录IP黑名单修改
    """

    def __init__(self, request_param):
        super(UpdateIPBlackListConfigRequest, self).__init__("/v1/login-secure-blacklist/update", "POST", "ctstackconf", "application/json")
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
        if self.parameters.id is not None:
            body_param["id"] = self.parameters.id
        if self.parameters.ip is not None:
            body_param["ip"] = self.parameters.ip
        if self.parameters.desc is not None:
            body_param["desc"] = self.parameters.desc
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


class UpdateIPBlackListConfigRequestParam(object):

    def __init__(self, id, ip, desc=None):
        """
        :param id: ID 编号
        :param ip: 登录ip
        :param desc: 描述信息字符串最长128
        """
        self.id = id
        self.ip = ip
        self.desc = desc

    def set_desc(self, desc):
        """
        :param desc: 描述信息字符串最长128
        """
        self.desc = desc

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.ip is None:
            raise Exception("ip can not None")

