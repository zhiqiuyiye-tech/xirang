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


class OpenAPISendTestEmailRequest(CTYunRequest):
    """
    发送测试邮件
    """

    def __init__(self, request_param):
        super(OpenAPISendTestEmailRequest, self).__init__("/v4/message/email/test", "POST", "ctmessage", "application/json")
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
        if self.parameters.to_addr is not None:
            body_param["toAddr"] = self.parameters.to_addr
        if self.parameters.host is not None:
            body_param["host"] = self.parameters.host
        if self.parameters.port is not None:
            body_param["port"] = self.parameters.port
        if self.parameters.tls is not None:
            body_param["tls"] = self.parameters.tls
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.sender_addr is not None:
            body_param["senderAddr"] = self.parameters.sender_addr
        if self.parameters.sender_display_name is not None:
            body_param["senderDisplayName"] = self.parameters.sender_display_name
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


class OpenAPISendTestEmailRequestParam(object):

    def __init__(self, to_addr, host, port, tls, account, password, sender_addr, sender_display_name, ):
        """
        :param to_addr: 目标邮箱地址
        :param host: 邮件服务器Host
        :param port: 邮件服务器端口
        :param tls: 根据邮件服务器实际端口协议填写，一般建议设置为true
        :param account: email格式，用于SMTP认证
        :param password: 发件邮箱密码
        :param sender_addr: email格式，一般与发件邮箱账号相同
        :param sender_display_name: 发送人展示名称
        """
        self.to_addr = to_addr
        self.host = host
        self.port = port
        self.tls = tls
        self.account = account
        self.password = password
        self.sender_addr = sender_addr
        self.sender_display_name = sender_display_name

    def check_param(self):
        """
        the param required check
        """
        if self.to_addr is None:
            raise Exception("to_addr can not None")
        if self.host is None:
            raise Exception("host can not None")
        if self.port is None:
            raise Exception("port can not None")
        if self.tls is None:
            raise Exception("tls can not None")
        if self.account is None:
            raise Exception("account can not None")
        if self.password is None:
            raise Exception("password can not None")
        if self.sender_addr is None:
            raise Exception("sender_addr can not None")
        if self.sender_display_name is None:
            raise Exception("sender_display_name can not None")

