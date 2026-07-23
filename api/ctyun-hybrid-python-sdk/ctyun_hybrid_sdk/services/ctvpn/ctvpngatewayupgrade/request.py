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


class CtvpnGatewayUpgradeRequest(CTYunRequest):
    """
    VPN网关升配
    """

    def __init__(self, request_param):
        super(CtvpnGatewayUpgradeRequest, self).__init__("/v4/vpn/gateway/upgrade", "POST", "ctvpn", "application/json")
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
        if self.parameters.connection_limit is not None:
            body_param["connectionLimit"] = self.parameters.connection_limit
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.link_resource_id is not None:
            body_param["linkResourceID"] = self.parameters.link_resource_id
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


class CtvpnGatewayUpgradeRequestParam(object):

    def __init__(self, region_id, connection_limit, bandwidth, resource_id, client_token=None, link_resource_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。
        :param region_id: 资源池id
        :param connection_limit: VPN网关连接数限制
        :param bandwidth: 带宽大小
        :param resource_id: 资源id
        :param link_resource_id: vpn连接id
        """
        self.client_token = client_token
        self.region_id = region_id
        self.connection_limit = connection_limit
        self.bandwidth = bandwidth
        self.resource_id = resource_id
        self.link_resource_id = link_resource_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。
        """
        self.client_token = client_token

    def set_link_resource_id(self, link_resource_id):
        """
        :param link_resource_id: vpn连接id
        """
        self.link_resource_id = link_resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.connection_limit is None:
            raise Exception("connection_limit can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.resource_id is None:
            raise Exception("resource_id can not None")

