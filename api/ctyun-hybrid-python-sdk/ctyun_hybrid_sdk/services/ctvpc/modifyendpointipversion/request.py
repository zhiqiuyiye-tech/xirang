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


class ModifyEndpointIPVersionRequest(CTYunRequest):
    """
    修改终端节点IP地址类型
    """

    def __init__(self, request_param):
        super(ModifyEndpointIPVersionRequest, self).__init__("/v4/vpce/modify-endpoint-ip-version", "POST", "ctvpc", "application/json")
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
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.endpoint_id is not None:
            body_param["endpointID"] = self.parameters.endpoint_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.ip_address is not None:
            body_param["ipAddress"] = self.parameters.ip_address
        if self.parameters.ipv6_address is not None:
            body_param["ipv6Address"] = self.parameters.ipv6_address
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


class ModifyEndpointIPVersionRequestParam(object):

    def __init__(self, region_id, endpoint_id, client_token=None, ip_version=None, ip_address=None, ipv6_address=None):
        """
        :param region_id: 资源池id
        :param endpoint_id: 终端节点ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈
        :param ip_address: 终端节点ipv4地址
        :param ipv6_address: 终端节点ipv6地址
        """
        self.region_id = region_id
        self.endpoint_id = endpoint_id
        self.client_token = client_token
        self.ip_version = ip_version
        self.ip_address = ip_address
        self.ipv6_address = ipv6_address

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        """
        self.client_token = client_token

    def set_ip_version(self, ip_version):
        """
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈
        """
        self.ip_version = ip_version

    def set_ip_address(self, ip_address):
        """
        :param ip_address: 终端节点ipv4地址
        """
        self.ip_address = ip_address

    def set_ipv6_address(self, ipv6_address):
        """
        :param ipv6_address: 终端节点ipv6地址
        """
        self.ipv6_address = ipv6_address

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")

