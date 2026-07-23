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


class UpdateHealthCheckNewRequest(CTYunRequest):
    """
    更新健康检查
    """

    def __init__(self, request_param):
        super(UpdateHealthCheckNewRequest, self).__init__("/v4/elb/update-health-check-new", "POST", "ctelb", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.timeout is not None:
            body_param["timeout"] = self.parameters.timeout
        if self.parameters.max_retry is not None:
            body_param["maxRetry"] = self.parameters.max_retry
        if self.parameters.http_method is not None:
            body_param["httpMethod"] = self.parameters.http_method
        if self.parameters.http_url_path is not None:
            body_param["httpUrlPath"] = self.parameters.http_url_path
        if self.parameters.http_expected_codes is not None:
            body_param["httpExpectedCodes"] = self.parameters.http_expected_codes
        if self.parameters.protocol_port is not None:
            body_param["protocolPort"] = self.parameters.protocol_port
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


class UpdateHealthCheckNewRequestParam(object):

    def __init__(self, region_id, id, client_token=None, name=None, description=None, timeout=None, max_retry=None, http_method=None, http_url_path=None, http_expected_codes=None, protocol_port=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一, 公共参数不支持修改（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param id: 健康检查ID
        :param name: 健康检查名称, 只能由数字，字母，-组成不能以数字和-开头，最大长度32
        :param description: 描述,内容限制：1、长度限制128 2、支持汉字，大小写字母，数字 3、支持英文特殊字符：~!@#$%^&*()_-+=<>?:"{}
        :param timeout: 健康检查响应的最大超时时间，取值范围：2-60秒，默认为2秒
        :param max_retry: 最大重试次数，取值范围：1-10次，默认为2次
        :param http_method: 仅当健康检查协议（protocol）为HTTP时必填且生效,HTTP请求的方法默认GET，{GET/HEAD/POST/PUT/DELETE/TRACE/OPTIONS/CONNECT/PATCH}
        :param http_url_path: 仅当健康检查协议（protocol）为HTTP时必填且生效,默认为'/',支持的最大字符长度：80
        :param http_expected_codes: 仅当健康检查协议（protocol）为HTTP时必填且生效,支持{http_2xx/http_3xx/http_4xx/http_5xx} 注意:此参数为数组
        :param protocol_port: 绑定全端口监听的主机组时必须指定，范围1-65535
        """
        self.client_token = client_token
        self.region_id = region_id
        self.id = id
        self.name = name
        self.description = description
        self.timeout = timeout
        self.max_retry = max_retry
        self.http_method = http_method
        self.http_url_path = http_url_path
        self.http_expected_codes = http_expected_codes
        self.protocol_port = protocol_port

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一, 公共参数不支持修改（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 健康检查名称, 只能由数字，字母，-组成不能以数字和-开头，最大长度32
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述,内容限制：1、长度限制128 2、支持汉字，大小写字母，数字 3、支持英文特殊字符：~!@#$%^&*()_-+=<>?:"{}
        """
        self.description = description

    def set_timeout(self, timeout):
        """
        :param timeout: 健康检查响应的最大超时时间，取值范围：2-60秒，默认为2秒
        """
        self.timeout = timeout

    def set_max_retry(self, max_retry):
        """
        :param max_retry: 最大重试次数，取值范围：1-10次，默认为2次
        """
        self.max_retry = max_retry

    def set_http_method(self, http_method):
        """
        :param http_method: 仅当健康检查协议（protocol）为HTTP时必填且生效,HTTP请求的方法默认GET，{GET/HEAD/POST/PUT/DELETE/TRACE/OPTIONS/CONNECT/PATCH}
        """
        self.http_method = http_method

    def set_http_url_path(self, http_url_path):
        """
        :param http_url_path: 仅当健康检查协议（protocol）为HTTP时必填且生效,默认为'/',支持的最大字符长度：80
        """
        self.http_url_path = http_url_path

    def set_http_expected_codes(self, http_expected_codes):
        """
        :param http_expected_codes: 仅当健康检查协议（protocol）为HTTP时必填且生效,支持{http_2xx/http_3xx/http_4xx/http_5xx}
        """
        self.http_expected_codes = http_expected_codes

    def set_protocol_port(self, protocol_port):
        """
        :param protocol_port: 绑定全端口监听的主机组时必须指定，范围1-65535
        """
        self.protocol_port = protocol_port

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

