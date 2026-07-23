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


class CheckTunnelOpenapiRequest(CTYunRequest):
    """
    校验tunnel（暂不使用）
    """

    def __init__(self, request_param):
        super(CheckTunnelOpenapiRequest, self).__init__("/v4/l2gw_connection/tunnel_check", "POST", "cda", "application/json")
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
        if self.parameters.l2gw_id is not None:
            body_param["l2gwID"] = self.parameters.l2gw_id
        if self.parameters.remote_tunnel_id is not None:
            body_param["remoteTunnelID"] = self.parameters.remote_tunnel_id
        if self.parameters.remote_tunnel_ip is not None:
            body_param["remoteTunnelIp"] = self.parameters.remote_tunnel_ip
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.l2gw_id is not None:
            query_param["l2gwID"] = self.parameters.l2gw_id
        if self.parameters.remote_tunnel_id is not None:
            query_param["remoteTunnelID"] = self.parameters.remote_tunnel_id
        if self.parameters.remote_tunnel_ip is not None:
            query_param["remoteTunnelIp"] = self.parameters.remote_tunnel_ip
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CheckTunnelOpenapiRequestParam(object):

    def __init__(self, region_id, l2gw_id, remote_tunnel_id, remote_tunnel_ip, ):
        """
        :param region_id: 资源池 ID
        :param l2gw_id: 企业交换机ID
        :param remote_tunnel_id: 隧道id
        :param remote_tunnel_ip: 隧道ip
        """
        self.region_id = region_id
        self.l2gw_id = l2gw_id
        self.remote_tunnel_id = remote_tunnel_id
        self.remote_tunnel_ip = remote_tunnel_ip

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.l2gw_id is None:
            raise Exception("l2gw_id can not None")
        if self.remote_tunnel_id is None:
            raise Exception("remote_tunnel_id can not None")
        if self.remote_tunnel_ip is None:
            raise Exception("remote_tunnel_ip can not None")

