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


class RefuseEndpointApplyRequest(CTYunRequest):
    """
    拒绝终端节点连接申请
    """

    def __init__(self, request_param):
        super(RefuseEndpointApplyRequest, self).__init__("/v4/vpce/reject-endpoint-apply", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
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


class RefuseEndpointApplyRequestParam(object):

    def __init__(self, region_id, endpoint_id, endpoint_service_id, client_token, ):
        """
        :param region_id: 资源池id
        :param endpoint_id: 终端节点ID
        :param endpoint_service_id: 终端节点服务ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.region_id = region_id
        self.endpoint_id = endpoint_id
        self.endpoint_service_id = endpoint_service_id
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

