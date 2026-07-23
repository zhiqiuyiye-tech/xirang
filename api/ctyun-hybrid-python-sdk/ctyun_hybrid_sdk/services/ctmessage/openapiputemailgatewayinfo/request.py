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


class OpenAPIPutEmailGatewayInfoRequest(CTYunRequest):
    """
    1. 仅支持SMTP协议邮件服务器;   
    2. status字段为true时，tls默认值为false，其他所有配置字段为必传字段；
    """

    def __init__(self, request_param):
        super(OpenAPIPutEmailGatewayInfoRequest, self).__init__("/v4/message/email/update", "POST", "ctmessage", "application/json")
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
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
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


class OpenAPIPutEmailGatewayInfoRequestParam(object):

    def __init__(self, status, host=None, port=None, tls=None, account=None, password=None, sender_addr=None, sender_display_name=None):
        """
        :param status: true-开启，false-关闭
        :param host: 长度为1 ~ 63 字符, 支持使用英文字母、数字、点号（.）、@、下划线（_）
        :param port: 1~65535, 例如25、465、587.
        :param tls: 根据邮件服务器实际端口协议填写，一般建议设置为true
        :param account: email格式，用于SMTP认证
        :param password: 长度为1 ~ 63字符，支持ASCII字符，不支持中文
        :param sender_addr: email格式,一般与发件邮箱账号相同
        :param sender_display_name: 长度为1 ~ 63字符
        """
        self.status = status
        self.host = host
        self.port = port
        self.tls = tls
        self.account = account
        self.password = password
        self.sender_addr = sender_addr
        self.sender_display_name = sender_display_name

    def set_host(self, host):
        """
        :param host: 长度为1 ~ 63 字符, 支持使用英文字母、数字、点号（.）、@、下划线（_）
        """
        self.host = host

    def set_port(self, port):
        """
        :param port: 1~65535, 例如25、465、587.
        """
        self.port = port

    def set_tls(self, tls):
        """
        :param tls: 根据邮件服务器实际端口协议填写，一般建议设置为true
        """
        self.tls = tls

    def set_account(self, account):
        """
        :param account: email格式，用于SMTP认证
        """
        self.account = account

    def set_password(self, password):
        """
        :param password: 长度为1 ~ 63字符，支持ASCII字符，不支持中文
        """
        self.password = password

    def set_sender_addr(self, sender_addr):
        """
        :param sender_addr: email格式,一般与发件邮箱账号相同
        """
        self.sender_addr = sender_addr

    def set_sender_display_name(self, sender_display_name):
        """
        :param sender_display_name: 长度为1 ~ 63字符
        """
        self.sender_display_name = sender_display_name

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")

