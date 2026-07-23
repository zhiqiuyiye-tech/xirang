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


class Ipv4GwBindRouteTableRequest(CTYunRequest):
    """
    IPv4网关绑定网关路由表 只支持4.0   
       
    ### 接口约束   
       
    1 个 ipv4 网关只能绑定一个路由表，每次调用该接口的效果是进行 update 操作。
    """

    def __init__(self, request_param):
        super(Ipv4GwBindRouteTableRequest, self).__init__("/v4/vpc/ipv4-gw/add-route-table-binding", "POST", "ctvpc", "application/json")
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
        if self.parameters.ipv4_gw_id is not None:
            body_param["ipv4GwID"] = self.parameters.ipv4_gw_id
        if self.parameters.route_table_id is not None:
            body_param["routeTableID"] = self.parameters.route_table_id
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


class Ipv4GwBindRouteTableRequestParam(object):

    def __init__(self, region_id, ipv4_gw_id, route_table_id, client_token=None):
        """
        :param client_token: 可传但是不进行校验, 客户端存根
        :param region_id: 区域ID
        :param ipv4_gw_id: IPv4网关的ID
        :param route_table_id: 网关路由表ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.ipv4_gw_id = ipv4_gw_id
        self.route_table_id = route_table_id

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验, 客户端存根
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ipv4_gw_id is None:
            raise Exception("ipv4_gw_id can not None")
        if self.route_table_id is None:
            raise Exception("route_table_id can not None")

