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


class QueryModifyNatPriceRequest(CTYunRequest):
    """
    变配nat网关 询价 
    """

    def __init__(self, request_param):
        super(QueryModifyNatPriceRequest, self).__init__("/v4/nat/query-modify-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
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


class QueryModifyNatPriceRequestParam(object):

    def __init__(self, region_id, spec, nat_gateway_id, client_token=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        :param region_id: 资源池 ID
        :param spec: 规格，规格 1~4, 1表示小型, 2表示中型, 3表示大型, 4表示超大型
        :param nat_gateway_id: nat网关ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.spec = spec
        self.nat_gateway_id = nat_gateway_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.spec is None:
            raise Exception("spec can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")

