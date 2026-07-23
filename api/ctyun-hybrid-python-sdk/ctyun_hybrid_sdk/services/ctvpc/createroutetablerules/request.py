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


class CreateRouteTableRulesRequest(CTYunRequest):
    """
    批量创建路由表规则   3.0底层不支持批量，由云管侧处理兼容，所以尽量数量控制在5个以内   
    
    """

    def __init__(self, request_param):
        super(CreateRouteTableRulesRequest, self).__init__("/v4/vpc/route-table/create-rules", "POST", "ctvpc", "application/json")
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
        if self.parameters.route_rules is not None:
            route_rules = []
            if isinstance(self.parameters.route_rules, list):
                for item in self.parameters.route_rules:
                    if type(item) is dict:
                        route_rules.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        route_rules.append(item_dict_value)
            else:
                route_rules.append(self.parameters.route_rules.get_dic())
            body_param["routeRules"] = route_rules
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


class RouteRule(object):

    def __init__(self, next_hop_id, next_hop_type, ip_version, destination, description=None):
        """
        :param next_hop_id: 下一跳设备 id（3.0资源池下一跳类型为natgw时，该字段填写所在的vpcID）
        :param next_hop_type: vpcpeering（对等连接） / havip（虚拟IP） / bm（弹性裸金属服务器）/ vm（云主机） / natgw（NAT网关）/ igw6（IPv6网关） / dc（专线网关） / ticc（云间高速） / vpngw（VPN网关） / enic（弹性网卡）目前只支持云主机、虚拟ip、vpn网关、Nat网关、对等连接、裸金属     3.0ipv4只支持云主机、nat网关、虚拟IP、对等连接、专线网关，3.0 ipv6只支持云主机、虚拟IP
        :param ip_version: 4 标识 ipv4, 6 标识 ipv6
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128	
        :param destination: 无类别域间路由 ipv4Cidr 或 ipv6Cidr格式
        """
        self.next_hop_id = next_hop_id
        self.next_hop_type = next_hop_type
        self.ip_version = ip_version
        self.description = description
        self.destination = destination
        self.check_param()

    def set_description(self, description):
        """
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128	
        """
        self.description = description

    def get_dic(self):
        obj_dict = dict()
        if self.next_hop_id is not None:
            obj_dict["nextHopID"] = self.next_hop_id
        if self.next_hop_type is not None:
            obj_dict["nextHopType"] = self.next_hop_type
        if self.ip_version is not None:
            obj_dict["ipVersion"] = self.ip_version
        if self.description is not None:
            obj_dict["description"] = self.description
        if self.destination is not None:
            obj_dict["destination"] = self.destination
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.next_hop_id is None:
            raise Exception("next_hop_id can not None")
        if self.next_hop_type is None:
            raise Exception("next_hop_type can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.destination is None:
            raise Exception("destination can not None")


class CreateRouteTableRulesRequestParam(object):

    def __init__(self, region_id, route_table_id, route_rules, client_token=None):
        """
        :param region_id: 区域 id
        :param route_table_id: 路由表 id
        :param route_rules: 路由表规则列表 注意:此参数为数组
        :param client_token: 客户端存根，可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.route_table_id = route_table_id
        self.route_rules = route_rules
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.route_table_id is None:
            raise Exception("route_table_id can not None")
        if self.route_rules is None:
            raise Exception("route_rules can not None")

