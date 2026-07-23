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


class CdaStaticRouteAddRequest(CTYunRequest):
    """
    专线网关需要先绑定物理专线且没有绑定动态路由
    """

    def __init__(self, request_param):
        super(CdaStaticRouteAddRequest, self).__init__("/v4/cda/static-route/add", "POST", "cda", "application/json")
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
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.dst_cidr is not None:
            body_param["dstCidr"] = self.parameters.dst_cidr
        if self.parameters.dst_cidr_v6 is not None:
            body_param["dstCidrV6"] = self.parameters.dst_cidr_v6
        if self.parameters.next_hop is not None:
            next_hop = []
            if isinstance(self.parameters.next_hop, list):
                for item in self.parameters.next_hop:
                    if type(item) is dict:
                        next_hop.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        next_hop.append(item_dict_value)
            else:
                next_hop.append(self.parameters.next_hop.get_dic())
            body_param["nextHop"] = next_hop
        if self.parameters.next_hop_v6 is not None:
            next_hop_v6 = []
            if isinstance(self.parameters.next_hop_v6, list):
                for item in self.parameters.next_hop_v6:
                    if type(item) is dict:
                        next_hop_v6.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        next_hop_v6.append(item_dict_value)
            else:
                next_hop_v6.append(self.parameters.next_hop_v6.get_dic())
            body_param["nextHopV6"] = next_hop_v6
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


class NextHop(object):

    def __init__(self, remote_gateway_ip, priority, track=None):
        """
        :param remote_gateway_ip: 下一跳，即物理专线的远端互联ip
        :param priority: 优先级
        :param track: 0为关闭，1为开启
        """
        self.remote_gateway_ip = remote_gateway_ip
        self.priority = priority
        self.track = track
        self.check_param()

    def set_track(self, track):
        """
        :param track: 0为关闭，1为开启
        """
        self.track = track

    def get_dic(self):
        obj_dict = dict()
        if self.remote_gateway_ip is not None:
            obj_dict["remoteGatewayIp"] = self.remote_gateway_ip
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.track is not None:
            obj_dict["track"] = self.track
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.remote_gateway_ip is None:
            raise Exception("remote_gateway_ip can not None")
        if self.priority is None:
            raise Exception("priority can not None")


class NextHopV6(object):

    def __init__(self, remote_gateway_ip, priority, track=None):
        """
        :param remote_gateway_ip: 下一跳，即物理专线的远端互联ip
        :param priority: 优先级
        :param track: 0为关闭，1为开启
        """
        self.remote_gateway_ip = remote_gateway_ip
        self.priority = priority
        self.track = track
        self.check_param()

    def set_track(self, track):
        """
        :param track: 0为关闭，1为开启
        """
        self.track = track

    def get_dic(self):
        obj_dict = dict()
        if self.remote_gateway_ip is not None:
            obj_dict["remoteGatewayIp"] = self.remote_gateway_ip
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.track is not None:
            obj_dict["track"] = self.track
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.remote_gateway_ip is None:
            raise Exception("remote_gateway_ip can not None")
        if self.priority is None:
            raise Exception("priority can not None")


class CdaStaticRouteAddRequestParam(object):

    def __init__(self, region_id, gateway_name, ip_version, dst_cidr=None, dst_cidr_v6=None, next_hop=None, next_hop_v6=None):
        """
        :param region_id: 资源池id
        :param gateway_name: 专线网关名称（唯一）（只能是字母和数字）
        :param ip_version: 0,IPV4 （默认） 1,DUALSTACK 2，IPV6
        :param dst_cidr: 目的地址列表 注意:此参数为数组
        :param dst_cidr_v6: 目的地址列表 注意:此参数为数组
        :param next_hop: 下一跳和优先级 注意:此参数为数组
        :param next_hop_v6: 下一跳和优先级 注意:此参数为数组
        """
        self.region_id = region_id
        self.gateway_name = gateway_name
        self.ip_version = ip_version
        self.dst_cidr = dst_cidr
        self.dst_cidr_v6 = dst_cidr_v6
        self.next_hop = next_hop
        self.next_hop_v6 = next_hop_v6

    def set_dst_cidr(self, dst_cidr):
        """
        :param dst_cidr: 目的地址列表
        """
        self.dst_cidr = dst_cidr

    def set_dst_cidr_v6(self, dst_cidr_v6):
        """
        :param dst_cidr_v6: 目的地址列表
        """
        self.dst_cidr_v6 = dst_cidr_v6

    def set_next_hop(self, next_hop):
        """
        :param next_hop: 下一跳和优先级
        """
        self.next_hop = next_hop

    def set_next_hop_v6(self, next_hop_v6):
        """
        :param next_hop_v6: 下一跳和优先级
        """
        self.next_hop_v6 = next_hop_v6

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")

