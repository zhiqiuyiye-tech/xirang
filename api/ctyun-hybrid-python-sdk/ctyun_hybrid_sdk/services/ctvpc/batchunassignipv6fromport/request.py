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


class BatchUnassignIPv6FromPortRequest(CTYunRequest):
    """
    多个网卡解绑IPv6地址
    """

    def __init__(self, request_param):
        super(BatchUnassignIPv6FromPortRequest, self).__init__("/v4/ports/batch-unassign-ipv6", "POST", "ctvpc", "application/json")
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

    def __init__(self, network_interface_id, ipv6_addresses, ):
        """
        :param network_interface_id: 网卡ID
        :param ipv6_addresses: IPv6地址列表
        """
        self.network_interface_id = network_interface_id
        self.ipv6_addresses = ipv6_addresses
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.network_interface_id is not None:
            obj_dict["networkInterfaceID"] = self.network_interface_id
        if self.ipv6_addresses is not None:
            obj_dict["ipv6Addresses"] = self.ipv6_addresses
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")
        if self.ipv6_addresses is None:
            raise Exception("ipv6_addresses can not None")


class BatchUnassignIPv6FromPortRequestParam(object):

    def __init__(self, client_token, region_id, data, ):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求当个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param data: 网卡设置IPv6信息的列表 注意:此参数为数组
        """
        self.client_token = client_token
        self.region_id = region_id
        self.data = data

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.data is None:
            raise Exception("data can not None")

