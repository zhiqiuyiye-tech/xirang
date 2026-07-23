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


class AssignIPv6ToPortRequest(CTYunRequest):
    """
    单个网卡关联多个IPv6地址
    """

    def __init__(self, request_param):
        super(AssignIPv6ToPortRequest, self).__init__("/v4/ports/assign-ipv6", "POST", "ctvpc", "application/json")
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
        if self.parameters.ipv6_addresses_count is not None:
            body_param["ipv6AddressesCount"] = self.parameters.ipv6_addresses_count
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


class AssignIPv6ToPortRequestParam(object):

    def __init__(self, region_id, network_interface_id, client_token, ipv6_addresses_count=None, ipv6_addresses=None):
        """
        :param region_id: 资源池id
        :param network_interface_id: 网卡id
        :param ipv6_addresses_count: 要分配的ipv6地址数量（注：ipv6AddressesCount和ipv6Addresses必传一个，且不能同时指定，建议不超过10个）
        :param ipv6_addresses: 要分配的IPV6地址（注：ipv6AddressesCount和ipv6Addresses必传一个，且不能同时指定，建议不超过10个） 注意:此参数为数组
        :param client_token: 用于保证订单幂等性
        """
        self.region_id = region_id
        self.network_interface_id = network_interface_id
        self.ipv6_addresses_count = ipv6_addresses_count
        self.ipv6_addresses = ipv6_addresses
        self.client_token = client_token

    def set_ipv6_addresses_count(self, ipv6_addresses_count):
        """
        :param ipv6_addresses_count: 要分配的ipv6地址数量（注：ipv6AddressesCount和ipv6Addresses必传一个，且不能同时指定，建议不超过10个）
        """
        self.ipv6_addresses_count = ipv6_addresses_count

    def set_ipv6_addresses(self, ipv6_addresses):
        """
        :param ipv6_addresses: 要分配的IPV6地址（注：ipv6AddressesCount和ipv6Addresses必传一个，且不能同时指定，建议不超过10个）
        """
        self.ipv6_addresses = ipv6_addresses

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

