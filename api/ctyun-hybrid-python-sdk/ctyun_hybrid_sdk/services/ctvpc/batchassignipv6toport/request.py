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


class BatchAssignIPv6ToPortRequest(CTYunRequest):
    """
    1、该接口无法保证原子性，可能会出现部分网卡更新成功，部分网卡更新失败的情况，这种情况需要调用方进行处理。   
    2、返回结果是多条任务的job id，再分别通过job id查询每条任务的执行结果。
    """

    def __init__(self, request_param):
        super(BatchAssignIPv6ToPortRequest, self).__init__("/v4/ports/batch-assign-ipv6", "POST", "ctvpc", "application/json")
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
        if self.parameters.data is not None:
            data = []
            if isinstance(self.parameters.data, list):
                for item in self.parameters.data:
                    if type(item) is dict:
                        data.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        data.append(item_dict_value)
            else:
                data.append(self.parameters.data.get_dic())
            body_param["data"] = data
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


class Data(object):

    def __init__(self, network_interface_id, ipv6_addresses_count=None, ipv6_addresses=None):
        """
        :param network_interface_id: 网卡ID（多个数组中的网卡id不允许重复）
        :param ipv6_addresses_count: Ipv6地址数量(ipv6AddressesCount和ipv6Addresses只能传一个)
        :param ipv6_addresses: IPv6地址列表(ipv6AddressesCount和ipv6Addresses只能传一个)
        """
        self.network_interface_id = network_interface_id
        self.ipv6_addresses_count = ipv6_addresses_count
        self.ipv6_addresses = ipv6_addresses
        self.check_param()

    def set_ipv6_addresses_count(self, ipv6_addresses_count):
        """
        :param ipv6_addresses_count: Ipv6地址数量(ipv6AddressesCount和ipv6Addresses只能传一个)
        """
        self.ipv6_addresses_count = ipv6_addresses_count

    def set_ipv6_addresses(self, ipv6_addresses):
        """
        :param ipv6_addresses: IPv6地址列表(ipv6AddressesCount和ipv6Addresses只能传一个)
        """
        self.ipv6_addresses = ipv6_addresses

    def get_dic(self):
        obj_dict = dict()
        if self.network_interface_id is not None:
            obj_dict["networkInterfaceID"] = self.network_interface_id
        if self.ipv6_addresses_count is not None:
            obj_dict["ipv6AddressesCount"] = self.ipv6_addresses_count
        if self.ipv6_addresses is not None:
            obj_dict["ipv6Addresses"] = self.ipv6_addresses
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")


class BatchAssignIPv6ToPortRequestParam(object):

    def __init__(self, region_id, data, client_token, ):
        """
        :param region_id: 资源池ID
        :param data: 网卡设置IPv6信息的列表 注意:此参数为数组
        :param client_token: 用于保证订单幂等性
        """
        self.region_id = region_id
        self.data = data
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.data is None:
            raise Exception("data can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

