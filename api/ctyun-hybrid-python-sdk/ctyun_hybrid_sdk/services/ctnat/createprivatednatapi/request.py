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


class CreatePrivateDnatApiRequest(CTYunRequest):
    """
    创建私网DNAT
    """

    def __init__(self, request_param):
        super(CreatePrivateDnatApiRequest, self).__init__("/v4/privatenat/create-dnat", "POST", "ctnat", "application/json")
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
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
        if self.parameters.external_ip is not None:
            body_param["externalIP"] = self.parameters.external_ip
        if self.parameters.external_port is not None:
            body_param["externalPort"] = self.parameters.external_port
        if self.parameters.internal_port is not None:
            body_param["internalPort"] = self.parameters.internal_port
        if self.parameters.internal_ip is not None:
            body_param["internalIP"] = self.parameters.internal_ip
        if self.parameters.port_id is not None:
            body_param["portID"] = self.parameters.port_id
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
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


class CreatePrivateDnatApiRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, external_ip, external_port, internal_port, protocol, internal_ip=None, port_id=None, description=None):
        """
        :param region_id: 资源池ID
        :param nat_gateway_id: 私网NAT的ID
        :param external_ip: 中转IP的地址
        :param external_port: 对外的端口（1-65535）
        :param internal_port: 内部端口
        :param internal_ip: 内部IP，和portID二选其一
        :param port_id: 网卡ID，和internalIP二选其一，网卡的优先级最高
        :param protocol: 协议：tcp/udp
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.external_ip = external_ip
        self.external_port = external_port
        self.internal_port = internal_port
        self.internal_ip = internal_ip
        self.port_id = port_id
        self.protocol = protocol
        self.description = description

    def set_internal_ip(self, internal_ip):
        """
        :param internal_ip: 内部IP，和portID二选其一
        """
        self.internal_ip = internal_ip

    def set_port_id(self, port_id):
        """
        :param port_id: 网卡ID，和internalIP二选其一，网卡的优先级最高
        """
        self.port_id = port_id

    def set_description(self, description):
        """
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")
        if self.external_ip is None:
            raise Exception("external_ip can not None")
        if self.external_port is None:
            raise Exception("external_port can not None")
        if self.internal_port is None:
            raise Exception("internal_port can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")

