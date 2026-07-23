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


class CreateDnatEntryRequest(CTYunRequest):
    """
    创建DNAT规则
    """

    def __init__(self, request_param):
        super(CreateDnatEntryRequest, self).__init__("/v4/vpc/create-dnat-entry", "POST", "ctvpc", "application/json")
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
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.external_port is not None:
            body_param["externalPort"] = self.parameters.external_port
        if self.parameters.internal_port is not None:
            body_param["internalPort"] = self.parameters.internal_port
        if self.parameters.virtual_machine_id is not None:
            body_param["virtualMachineID"] = self.parameters.virtual_machine_id
        if self.parameters.virtual_machine_type is not None:
            body_param["virtualMachineType"] = self.parameters.virtual_machine_type
        if self.parameters.internal_ip is not None:
            body_param["internalIp"] = self.parameters.internal_ip
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.external_id is not None:
            body_param["externalID"] = self.parameters.external_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.internal_port_range is not None:
            body_param["internalPortRange"] = self.parameters.internal_port_range
        if self.parameters.external_port_range is not None:
            body_param["externalPortRange"] = self.parameters.external_port_range
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


class CreateDnatEntryRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, protocol, external_port, internal_port, virtual_machine_type, external_id, virtual_machine_id=None, internal_ip=None, description=None, client_token=None, internal_port_range=None, external_port_range=None):
        """
        :param region_id: 资源池id
        :param nat_gateway_id: NAT网关id
        :param protocol: 支持协议：TCP/UDP/ANY，当为ANY时，externalPort和internalPort需传0
        :param external_port: 弹性IP公网端口 [1,65535]，当传端口段externalPortRange参数时，此参数为端口段起始端口
        :param internal_port: 主机内网端口 [1,65535]，当传端口段internalPortRange参数时，此参数为端口段起始端口
        :param virtual_machine_id: 云主机id virtualMachineType为1时必传
        :param virtual_machine_type: 云主机类型1-选择云主机，virtualMachineID字段必传 2-自定义，internalIp必传，默认1
        :param internal_ip: 云主机ip virtualMachineType为2时必传
        :param description: 描述信息  支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        :param external_id: 弹性公网id
        :param client_token: 客户端Token，用于保证请求的幂等性且不能超过64个字符(公有云要求必传字段,私有云不具有实际意义）)
        :param internal_port_range: 虚拟机或者裸机对外提供服务的协议端口号范围。功能说明:该端口范围与externalPortRange按顺序实现1:1映射。取值范围:1~65535。约束:只能以’-’字符连接端口范围。
        :param external_port_range: Floatingip对外提供服务的端口号范围。功能说明:该端口范围与internalPortRange按顺序实现1:1映射。取值范围:1~65535。约束:只能以’-’字符连接端口范围。
        """
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.protocol = protocol
        self.external_port = external_port
        self.internal_port = internal_port
        self.virtual_machine_id = virtual_machine_id
        self.virtual_machine_type = virtual_machine_type
        self.internal_ip = internal_ip
        self.description = description
        self.external_id = external_id
        self.client_token = client_token
        self.internal_port_range = internal_port_range
        self.external_port_range = external_port_range

    def set_virtual_machine_id(self, virtual_machine_id):
        """
        :param virtual_machine_id: 云主机id virtualMachineType为1时必传
        """
        self.virtual_machine_id = virtual_machine_id

    def set_internal_ip(self, internal_ip):
        """
        :param internal_ip: 云主机ip virtualMachineType为2时必传
        """
        self.internal_ip = internal_ip

    def set_description(self, description):
        """
        :param description: 描述信息  支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端Token，用于保证请求的幂等性且不能超过64个字符(公有云要求必传字段,私有云不具有实际意义）)
        """
        self.client_token = client_token

    def set_internal_port_range(self, internal_port_range):
        """
        :param internal_port_range: 虚拟机或者裸机对外提供服务的协议端口号范围。功能说明:该端口范围与externalPortRange按顺序实现1:1映射。取值范围:1~65535。约束:只能以’-’字符连接端口范围。
        """
        self.internal_port_range = internal_port_range

    def set_external_port_range(self, external_port_range):
        """
        :param external_port_range: Floatingip对外提供服务的端口号范围。功能说明:该端口范围与internalPortRange按顺序实现1:1映射。取值范围:1~65535。约束:只能以’-’字符连接端口范围。
        """
        self.external_port_range = external_port_range

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.external_port is None:
            raise Exception("external_port can not None")
        if self.internal_port is None:
            raise Exception("internal_port can not None")
        if self.virtual_machine_type is None:
            raise Exception("virtual_machine_type can not None")
        if self.external_id is None:
            raise Exception("external_id can not None")

