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


class CreateVpcPeeringRouteHybridRequest(CTYunRequest):
    """
    1.16.01版本以后支持该接口
    """

    def __init__(self, request_param):
        super(CreateVpcPeeringRouteHybridRequest, self).__init__("/v4/vpc/vpcpeer/create-peering-route", "POST", "ctvpc", "application/json")
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
        if self.parameters.peering_id is not None:
            body_param["peeringId"] = self.parameters.peering_id
        if self.parameters.network_id is not None:
            body_param["networkId"] = self.parameters.network_id
        if self.parameters.routes is not None:
            routes = []
            if isinstance(self.parameters.routes, list):
                for item in self.parameters.routes:
                    if type(item) is dict:
                        routes.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        routes.append(item_dict_value)
            else:
                routes.append(self.parameters.routes.get_dic())
            body_param["routes"] = routes
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


class Route(object):

    def __init__(self, destination, next_hop, ):
        """
        :param destination: 目的地址：子网掩码格式：192.168.1.0/24
        :param next_hop: 下一跳，对等连接的id
        """
        self.destination = destination
        self.next_hop = next_hop
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.destination is not None:
            obj_dict["destination"] = self.destination
        if self.next_hop is not None:
            obj_dict["nextHop"] = self.next_hop
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.destination is None:
            raise Exception("destination can not None")
        if self.next_hop is None:
            raise Exception("next_hop can not None")


class CreateVpcPeeringRouteHybridRequestParam(object):

    def __init__(self, region_id, peering_id, network_id, routes, ):
        """
        :param region_id: 资源池id
        :param peering_id: 对等连接id
        :param network_id: vpc的id
        :param routes: 路由列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.peering_id = peering_id
        self.network_id = network_id
        self.routes = routes

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.peering_id is None:
            raise Exception("peering_id can not None")
        if self.network_id is None:
            raise Exception("network_id can not None")
        if self.routes is None:
            raise Exception("routes can not None")

