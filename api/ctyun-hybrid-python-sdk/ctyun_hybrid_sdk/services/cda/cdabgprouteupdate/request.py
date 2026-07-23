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


class CdaBgpRouteUpdateRequest(CTYunRequest):
    """
    底层不支持修改ipVersion
    """

    def __init__(self, request_param):
        super(CdaBgpRouteUpdateRequest, self).__init__("/v4/cda/bgp-route/update", "POST", "cda", "application/json")
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
        if self.parameters.bgp_id is not None:
            body_param["BGPId"] = self.parameters.bgp_id
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.network_cidr is not None:
            body_param["networkCidr"] = self.parameters.network_cidr
        if self.parameters.network_cidr_v6 is not None:
            body_param["networkCidrV6"] = self.parameters.network_cidr_v6
        if self.parameters.bgp_list is not None:
            bgp_list = []
            if isinstance(self.parameters.bgp_list, list):
                for item in self.parameters.bgp_list:
                    if type(item) is dict:
                        bgp_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        bgp_list.append(item_dict_value)
            else:
                bgp_list.append(self.parameters.bgp_list.get_dic())
            body_param["BGPList"] = bgp_list
        if self.parameters.bgp_ipv6_list is not None:
            bgp_ipv6_list = []
            if isinstance(self.parameters.bgp_ipv6_list, list):
                for item in self.parameters.bgp_ipv6_list:
                    if type(item) is dict:
                        bgp_ipv6_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        bgp_ipv6_list.append(item_dict_value)
            else:
                bgp_ipv6_list.append(self.parameters.bgp_ipv6_list.get_dic())
            body_param["BGPIpv6List"] = bgp_ipv6_list
        if self.parameters.multi_path is not None:
            body_param["multiPath"] = self.parameters.multi_path
        if self.parameters.multi_path_ipv6 is not None:
            body_param["multiPathIpv6"] = self.parameters.multi_path_ipv6
        if self.parameters.multi_path_type is not None:
            body_param["multiPathType"] = self.parameters.multi_path_type
        if self.parameters.multi_path_number is not None:
            body_param["multiPathNumber"] = self.parameters.multi_path_number
        if self.parameters.multi_path_num_ipv6 is not None:
            body_param["multiPathNumIpv6"] = self.parameters.multi_path_num_ipv6
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


class BGP(object):

    def __init__(self, line_name, bgp_ip, bfd, peer_as, bgp_neighbor, bgp_key=None):
        """
        :param line_name: 物理专线名称
        :param bgp_ip: BGP邻居 IP
        :param bfd: 是否打开bfd功能
        :param peer_as: Peer AS号
        :param bgp_neighbor: BGP邻居名称
        :param bgp_key: BGP密钥
        """
        self.line_name = line_name
        self.bgp_ip = bgp_ip
        self.bfd = bfd
        self.peer_as = peer_as
        self.bgp_neighbor = bgp_neighbor
        self.bgp_key = bgp_key
        self.check_param()

    def set_bgp_key(self, bgp_key):
        """
        :param bgp_key: BGP密钥
        """
        self.bgp_key = bgp_key

    def get_dic(self):
        obj_dict = dict()
        if self.line_name is not None:
            obj_dict["lineName"] = self.line_name
        if self.bgp_ip is not None:
            obj_dict["BGPIP"] = self.bgp_ip
        if self.bfd is not None:
            obj_dict["bfd"] = self.bfd
        if self.peer_as is not None:
            obj_dict["peerAS"] = self.peer_as
        if self.bgp_neighbor is not None:
            obj_dict["BGPNeighbor"] = self.bgp_neighbor
        if self.bgp_key is not None:
            obj_dict["BGPKey"] = self.bgp_key
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.line_name is None:
            raise Exception("line_name can not None")
        if self.bgp_ip is None:
            raise Exception("bgp_ip can not None")
        if self.bfd is None:
            raise Exception("bfd can not None")
        if self.peer_as is None:
            raise Exception("peer_as can not None")
        if self.bgp_neighbor is None:
            raise Exception("bgp_neighbor can not None")


class BGPIpv6(object):

    def __init__(self, line_name, bgp_ipv6, bfd, peer_as, bgp_neighbor_ipv6, bgp_key=None):
        """
        :param line_name: 物理专线名称
        :param bgp_ipv6: BGP邻居V6 IP
        :param bfd: 是否打开bfd功能
        :param peer_as: Peer AS号
        :param bgp_neighbor_ipv6: BGP邻居V6名称
        :param bgp_key: BGP密钥
        """
        self.line_name = line_name
        self.bgp_ipv6 = bgp_ipv6
        self.bfd = bfd
        self.peer_as = peer_as
        self.bgp_neighbor_ipv6 = bgp_neighbor_ipv6
        self.bgp_key = bgp_key
        self.check_param()

    def set_bgp_key(self, bgp_key):
        """
        :param bgp_key: BGP密钥
        """
        self.bgp_key = bgp_key

    def get_dic(self):
        obj_dict = dict()
        if self.line_name is not None:
            obj_dict["lineName"] = self.line_name
        if self.bgp_ipv6 is not None:
            obj_dict["BGPIPv6"] = self.bgp_ipv6
        if self.bfd is not None:
            obj_dict["bfd"] = self.bfd
        if self.peer_as is not None:
            obj_dict["peerAS"] = self.peer_as
        if self.bgp_neighbor_ipv6 is not None:
            obj_dict["BGPNeighborIpv6"] = self.bgp_neighbor_ipv6
        if self.bgp_key is not None:
            obj_dict["BGPKey"] = self.bgp_key
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.line_name is None:
            raise Exception("line_name can not None")
        if self.bgp_ipv6 is None:
            raise Exception("bgp_ipv6 can not None")
        if self.bfd is None:
            raise Exception("bfd can not None")
        if self.peer_as is None:
            raise Exception("peer_as can not None")
        if self.bgp_neighbor_ipv6 is None:
            raise Exception("bgp_neighbor_ipv6 can not None")


class CdaBgpRouteUpdateRequestParam(object):

    def __init__(self, region_id, bgp_id, ip_version, network_cidr, network_cidr_v6, bgp_list, bgp_ipv6_list, multi_path=None, multi_path_ipv6=None, multi_path_type=None, multi_path_number=None, multi_path_num_ipv6=None):
        """
        :param region_id: 资源池id
        :param bgp_id: 动态路由id（唯一）
        :param ip_version: IPV4 （默认)/DUALSTACK/IPV6 
        :param network_cidr: 客户侧子网列表(IPv4) 注意:此参数为数组
        :param network_cidr_v6: 客户侧子网列表(IPv6) 注意:此参数为数组
        :param bgp_list: Ipv4类型的bgp 注意:此参数为数组
        :param bgp_ipv6_list: Ipv6类型的bgp 注意:此参数为数组
        :param multi_path: 是否打开多路功能
        :param multi_path_ipv6: 是否开启Bgp-ipv6多路功能
        :param multi_path_type:  Bgp多路功能类型(IBGP/EBGP) 
        :param multi_path_number: Bgp多路功能序号(负载线路数)
        :param multi_path_num_ipv6: BGP-IPv6多路功能序号(负载线路数)
        """
        self.region_id = region_id
        self.bgp_id = bgp_id
        self.ip_version = ip_version
        self.network_cidr = network_cidr
        self.network_cidr_v6 = network_cidr_v6
        self.bgp_list = bgp_list
        self.bgp_ipv6_list = bgp_ipv6_list
        self.multi_path = multi_path
        self.multi_path_ipv6 = multi_path_ipv6
        self.multi_path_type = multi_path_type
        self.multi_path_number = multi_path_number
        self.multi_path_num_ipv6 = multi_path_num_ipv6

    def set_multi_path(self, multi_path):
        """
        :param multi_path: 是否打开多路功能
        """
        self.multi_path = multi_path

    def set_multi_path_ipv6(self, multi_path_ipv6):
        """
        :param multi_path_ipv6: 是否开启Bgp-ipv6多路功能
        """
        self.multi_path_ipv6 = multi_path_ipv6

    def set_multi_path_type(self, multi_path_type):
        """
        :param multi_path_type:  Bgp多路功能类型(IBGP/EBGP) 
        """
        self.multi_path_type = multi_path_type

    def set_multi_path_number(self, multi_path_number):
        """
        :param multi_path_number: Bgp多路功能序号(负载线路数)
        """
        self.multi_path_number = multi_path_number

    def set_multi_path_num_ipv6(self, multi_path_num_ipv6):
        """
        :param multi_path_num_ipv6: BGP-IPv6多路功能序号(负载线路数)
        """
        self.multi_path_num_ipv6 = multi_path_num_ipv6

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bgp_id is None:
            raise Exception("bgp_id can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.network_cidr is None:
            raise Exception("network_cidr can not None")
        if self.network_cidr_v6 is None:
            raise Exception("network_cidr_v6 can not None")
        if self.bgp_list is None:
            raise Exception("bgp_list can not None")
        if self.bgp_ipv6_list is None:
            raise Exception("bgp_ipv6_list can not None")

