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


class PortReplaceVPCRequest(CTYunRequest):
    """
    网卡更换网络和IP地址
    """

    def __init__(self, request_param):
        super(PortReplaceVPCRequest, self).__init__("/v4/ports/change-vpc", "POST", "ctvpc", "application/json")
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
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
        if self.parameters.ip_address is not None:
            body_param["ipAddress"] = self.parameters.ip_address
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.security_group_ids is not None:
            body_param["securityGroupIDs"] = self.parameters.security_group_ids
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


class PortReplaceVPCRequestParam(object):

    def __init__(self, region_id, network_interface_id, subnet_id, instance_id, security_group_ids, ip_address=None):
        """
        :param region_id: 资源池Id
        :param network_interface_id: 网卡ID(仅主网卡允许更换网络)
        :param ip_address: 内网 IP 地址，如果不传或传""为自动分配（仅支持ipv4地址）
        :param subnet_id: 子网 ID
        :param instance_id: 弹性云主机 ID
        :param security_group_ids: 安全组 id 列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.network_interface_id = network_interface_id
        self.ip_address = ip_address
        self.subnet_id = subnet_id
        self.instance_id = instance_id
        self.security_group_ids = security_group_ids

    def set_ip_address(self, ip_address):
        """
        :param ip_address: 内网 IP 地址，如果不传或传""为自动分配（仅支持ipv4地址）
        """
        self.ip_address = ip_address

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.security_group_ids is None:
            raise Exception("security_group_ids can not None")

