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


class UnassignIPv6FromPortRequest(CTYunRequest):
    """
    单个网卡解绑多个 IPv6 地址
    """

    def __init__(self, request_param):
        super(UnassignIPv6FromPortRequest, self).__init__("/v4/ecs/ports/unassign-ipv6", "POST", "ctecs", "application/json")
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
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
        if self.parameters.ipv6_addresses is not None:
            body_param["ipv6Addresses"] = self.parameters.ipv6_addresses
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class UnassignIPv6FromPortRequestParam(object):

    def __init__(self, region_id, network_interface_id, ipv6_addresses, client_token=None):
        """
        :param region_id: 资源池id
        :param network_interface_id: 网卡id
        :param ipv6_addresses: 要解绑的IPV6地址 注意:此参数为数组
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.network_interface_id = network_interface_id
        self.ipv6_addresses = ipv6_addresses
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")
        if self.ipv6_addresses is None:
            raise Exception("ipv6_addresses can not None")

