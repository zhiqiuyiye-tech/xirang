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


class OpenAPIPutSmsGatewayInfoRequest(CTYunRequest):
    """
    1. status为false时，其他参数无效，可设置为空；
    """

    def __init__(self, request_param):
        super(OpenAPIPutSmsGatewayInfoRequest, self).__init__("/v4/message/sms/update", "POST", "ctmessage", "application/json")
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
        if self.parameters.service_provider is not None:
            body_param["serviceProvider"] = self.parameters.service_provider
        if self.parameters.endpoint is not None:
            body_param["endpoint"] = self.parameters.endpoint
        if self.parameters.access_key_id is not None:
            body_param["accessKeyID"] = self.parameters.access_key_id
        if self.parameters.access_key_secret is not None:
            body_param["accessKeySecret"] = self.parameters.access_key_secret
        if self.parameters.sms_sign is not None:
            body_param["smsSign"] = self.parameters.sms_sign
        if self.parameters.args is not None:
            body_param["args"] = self.parameters.args
        if self.parameters.script is not None:
            body_param["script"] = self.parameters.script
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


class OpenAPIPutSmsGatewayInfoRequestParam(object):

    def __init__(self, status, service_provider=None, endpoint=None, access_key_id=None, access_key_secret=None, sms_sign=None, args=None, script=None):
        """
        :param status: ture-开启，false-关闭
        :param service_provider: 短信服务提供商
        :param endpoint: serviceProvider为1,2时必传
        :param access_key_id: serviceProvider为1,2时必传
        :param access_key_secret: serviceProvider为1,2时必传
        :param sms_sign: 支持使用中文、英文字母、数字，不支持全数字
        :param args: serviceProvider为99时必传，搭配接入脚本使用
        :param script: serviceProvider为99时必传，搭配接入参数使用，对脚本内容进行base64编码后传入
        """
        self.status = status
        self.service_provider = service_provider
        self.endpoint = endpoint
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.sms_sign = sms_sign
        self.args = args
        self.script = script

    def set_service_provider(self, service_provider):
        """
        :param service_provider: 短信服务提供商
        """
        self.service_provider = service_provider

    def set_endpoint(self, endpoint):
        """
        :param endpoint: serviceProvider为1,2时必传
        """
        self.endpoint = endpoint

    def set_access_key_id(self, access_key_id):
        """
        :param access_key_id: serviceProvider为1,2时必传
        """
        self.access_key_id = access_key_id

    def set_access_key_secret(self, access_key_secret):
        """
        :param access_key_secret: serviceProvider为1,2时必传
        """
        self.access_key_secret = access_key_secret

    def set_sms_sign(self, sms_sign):
        """
        :param sms_sign: 支持使用中文、英文字母、数字，不支持全数字
        """
        self.sms_sign = sms_sign

    def set_args(self, args):
        """
        :param args: serviceProvider为99时必传，搭配接入脚本使用
        """
        self.args = args

    def set_script(self, script):
        """
        :param script: serviceProvider为99时必传，搭配接入参数使用，对脚本内容进行base64编码后传入
        """
        self.script = script

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")

