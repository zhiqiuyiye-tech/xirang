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


class DeleteIPv6GatewayRequest(CTYunRequest):
    """
    删除ipv6网关
    """

    def __init__(self, request_param):
        super(DeleteIPv6GatewayRequest, self).__init__("/v4/vpc/delete-ipv6-gateway", "POST", "ctvpc", "application/json")
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
        if self.parameters.ipv6_gateway_id is not None:
            body_param["ipv6GatewayID"] = self.parameters.ipv6_gateway_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class DeleteIPv6GatewayRequestParam(object):

    def __init__(self, region_id, ipv6_gateway_id, client_token, project_id=None):
        """
        :param region_id: 资源池ID
        :param ipv6_gateway_id: IPv6网关ID
        :param client_token: 客户端存根，用于保证订单幂等性（私有云接口无效，不做校验）
        :param project_id: 企业项目 ID，默认为"0"
        """
        self.region_id = region_id
        self.ipv6_gateway_id = ipv6_gateway_id
        self.client_token = client_token
        self.project_id = project_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为"0"
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ipv6_gateway_id is None:
            raise Exception("ipv6_gateway_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

