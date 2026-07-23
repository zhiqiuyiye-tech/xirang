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


class ApiOrderResizeNatRequest(CTYunRequest):
    """
    变配NAT网关走订单
    """

    def __init__(self, request_param):
        super(ApiOrderResizeNatRequest, self).__init__("/v4/vpc/modify-nat-gateway-spec", "POST", "ctvpc", "application/json")
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
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
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


class ApiOrderResizeNatRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, spec, client_token=None):
        """
        :param region_id: 资源池ID
        :param nat_gateway_id: NAT网关ID
        :param spec: 规格(可传值：1-SMALL,2-MEDIUM,3-LARGE,4-XLARGE)。变配接口只支持资源升级操作
        :param client_token: 
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.spec = spec
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")
        if self.spec is None:
            raise Exception("spec can not None")

