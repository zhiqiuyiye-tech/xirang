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


class CreateEndpointServiceReverseRuleRequest(CTYunRequest):
    """
    创建终端节点服务中转规则(反向访问规则)   
    
    """

    def __init__(self, request_param):
        super(CreateEndpointServiceReverseRuleRequest, self).__init__("/v4/vpce/create-endpoint-service-reverse-rule", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_id is not None:
            body_param["endpointID"] = self.parameters.endpoint_id
        if self.parameters.transit_ip_address is not None:
            body_param["transitIPAddress"] = self.parameters.transit_ip_address
        if self.parameters.transit_port is not None:
            body_param["transitPort"] = self.parameters.transit_port
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.target_ip_address is not None:
            body_param["targetIPAddress"] = self.parameters.target_ip_address
        if self.parameters.target_port is not None:
            body_param["targetPort"] = self.parameters.target_port
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


class CreateEndpointServiceReverseRuleRequestParam(object):

    def __init__(self, region_id, endpoint_service_id, endpoint_id, transit_ip_address, transit_port, protocol, target_ip_address, target_port, client_token=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param endpoint_service_id: 终端节点关联的终端节点服务
        :param endpoint_id: 节点id
        :param transit_ip_address: 中转ip地址
        :param transit_port: 中转端口,1到65535
        :param protocol: TCP:TCP协议,UDP:UDP协议
        :param target_ip_address: 目标ip地址
        :param target_port: 目标端口,1到65535
        """
        self.client_token = client_token
        self.region_id = region_id
        self.endpoint_service_id = endpoint_service_id
        self.endpoint_id = endpoint_id
        self.transit_ip_address = transit_ip_address
        self.transit_port = transit_port
        self.protocol = protocol
        self.target_ip_address = target_ip_address
        self.target_port = target_port

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
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
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")
        if self.transit_ip_address is None:
            raise Exception("transit_ip_address can not None")
        if self.transit_port is None:
            raise Exception("transit_port can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.target_ip_address is None:
            raise Exception("target_ip_address can not None")
        if self.target_port is None:
            raise Exception("target_port can not None")

