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


class DeleteEndpointServiceRuleRequest(CTYunRequest):
    """
    终端节点服务规则删除接口
    """

    def __init__(self, request_param):
        super(DeleteEndpointServiceRuleRequest, self).__init__("/v4/vpce/delete-endpoint-service-rule", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.server_port is not None:
            body_param["serverPort"] = self.parameters.server_port
        if self.parameters.endpoint_port is not None:
            body_param["endpointPort"] = self.parameters.endpoint_port
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


class DeleteEndpointServiceRuleRequestParam(object):

    def __init__(self, region_id, endpoint_service_id, protocol, server_port, endpoint_port, client_token=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param endpoint_service_id: 终端节点关联的终端节点服务
        :param protocol: TCP:TCP协议,UDP:UDP协议
        :param server_port: 服务端口
        :param endpoint_port: 节点端口
        """
        self.client_token = client_token
        self.region_id = region_id
        self.endpoint_service_id = endpoint_service_id
        self.protocol = protocol
        self.server_port = server_port
        self.endpoint_port = endpoint_port

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.server_port is None:
            raise Exception("server_port can not None")
        if self.endpoint_port is None:
            raise Exception("endpoint_port can not None")

