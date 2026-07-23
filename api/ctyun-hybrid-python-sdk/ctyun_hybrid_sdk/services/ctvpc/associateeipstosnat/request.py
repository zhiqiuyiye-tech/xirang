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


class AssociateEipsToSnatRequest(CTYunRequest):
    """
    SNAT添加EIP
    """

    def __init__(self, request_param):
        super(AssociateEipsToSnatRequest, self).__init__("/v4/vpc/join-snat-for-eips", "POST", "ctvpc", "application/json")
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
        if self.parameters.s_nat_id is not None:
            body_param["sNatID"] = self.parameters.s_nat_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.ip_address_ids is not None:
            body_param["ipAddressIds"] = self.parameters.ip_address_ids
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
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


class AssociateEipsToSnatRequestParam(object):

    def __init__(self, s_nat_id, region_id, ip_address_ids, nat_gateway_id, client_token=None):
        """
        :param s_nat_id: snat id
        :param region_id: 资源池id
        :param ip_address_ids: 弹性ip id列表 注意:此参数为数组
        :param nat_gateway_id: NAT网关id
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.s_nat_id = s_nat_id
        self.region_id = region_id
        self.ip_address_ids = ip_address_ids
        self.nat_gateway_id = nat_gateway_id
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
        if self.s_nat_id is None:
            raise Exception("s_nat_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ip_address_ids is None:
            raise Exception("ip_address_ids can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")

