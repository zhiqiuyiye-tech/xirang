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


class CtvpnGatewayUpdateRequest(CTYunRequest):
    """
    VPN网关修改
    """

    def __init__(self, request_param):
        super(CtvpnGatewayUpdateRequest, self).__init__("/v4/vpn/gateway/update", "POST", "ctvpn", "application/json")
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
        if self.parameters.customer_id is not None:
            body_param["customerID"] = self.parameters.customer_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.local_subnet_ids is not None:
            body_param["localSubnetIDs"] = self.parameters.local_subnet_ids
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


class CtvpnGatewayUpdateRequestParam(object):

    def __init__(self, region_id, name, id, customer_id=None, local_subnet_ids=None):
        """
        :param region_id: 资源池id
        :param customer_id: 此接口中无实际作用
        :param name: 名称，长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param id: vpn网关id
        :param local_subnet_ids: vpn网关本端子网列表，vpn底座高版本必传参数，低版本忽略 注意:此参数为数组
        """
        self.region_id = region_id
        self.customer_id = customer_id
        self.name = name
        self.id = id
        self.local_subnet_ids = local_subnet_ids

    def set_customer_id(self, customer_id):
        """
        :param customer_id: 此接口中无实际作用
        """
        self.customer_id = customer_id

    def set_local_subnet_ids(self, local_subnet_ids):
        """
        :param local_subnet_ids: vpn网关本端子网列表，vpn底座高版本必传参数，低版本忽略
        """
        self.local_subnet_ids = local_subnet_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.id is None:
            raise Exception("id can not None")

