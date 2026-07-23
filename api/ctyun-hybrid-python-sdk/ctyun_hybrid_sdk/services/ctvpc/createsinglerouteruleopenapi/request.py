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


class CreateSingleRouteRuleOpenapiRequest(CTYunRequest):
    """
    创建单条路由表规则   
    
    """

    def __init__(self, request_param):
        super(CreateSingleRouteRuleOpenapiRequest, self).__init__("/v4/vpc/route-table/create-rule", "POST", "ctvpc", "application/json")
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
        if self.parameters.route_table_id is not None:
            body_param["routeTableID"] = self.parameters.route_table_id
        if self.parameters.next_hop_id is not None:
            body_param["nextHopID"] = self.parameters.next_hop_id
        if self.parameters.next_hop_type is not None:
            body_param["nextHopType"] = self.parameters.next_hop_type
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.destination is not None:
            body_param["destination"] = self.parameters.destination
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class CreateSingleRouteRuleOpenapiRequestParam(object):

    def __init__(self, region_id, route_table_id, next_hop_id, next_hop_type, ip_version, destination, description=None):
        """
        :param region_id: 区域 id
        :param route_table_id: 路由表 id
        :param next_hop_id: 下一跳设备 id（3.0资源池下一跳类型为natgw时，该字段填写所在的vpcID）
        :param next_hop_type: vpcpeering（对等连接） / havip（虚拟IP） / bm（弹性裸金属服务器）/ vm（云主机） / natgw（NAT网关）/ igw6（IPv6网关） / dc（专线网关） / ticc（云间高速） / vpngw（VPN网关） / enic（弹性网卡）目前只支持云主机、虚拟ip、vpn网关、Nat网关、对等连接、裸金属     3.0ipv4只支持云主机、nat网关、虚拟IP、对等连接、专线网关，3.0 ipv6只支持云主机、虚拟IP
        :param ip_version: 4 标识 ipv4, 6 标识 ipv6
        :param destination: 无类别域间路由 ipv4Cidr 或 ipv6Cidr格式
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128	
        """
        self.region_id = region_id
        self.route_table_id = route_table_id
        self.next_hop_id = next_hop_id
        self.next_hop_type = next_hop_type
        self.ip_version = ip_version
        self.destination = destination
        self.description = description

    def set_description(self, description):
        """
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128	
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.route_table_id is None:
            raise Exception("route_table_id can not None")
        if self.next_hop_id is None:
            raise Exception("next_hop_id can not None")
        if self.next_hop_type is None:
            raise Exception("next_hop_type can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.destination is None:
            raise Exception("destination can not None")

