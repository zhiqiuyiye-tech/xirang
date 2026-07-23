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


class CreateTargetRequest(CTYunRequest):
    """
    创建后端服务   
    **注意**：   InstanceType参数在私有云是直接根据instanceId即可判断主机类型，默认云主机/裸金属不用传，但是当IP时必须要指定的。取值范围：VM、BM、ENIC（ENIC暂不支持）、IP   
    更新支持IP，开发中
    """

    def __init__(self, request_param):
        super(CreateTargetRequest, self).__init__("/v4/elb/create-target", "POST", "ctelb", "application/json")
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
        if self.parameters.target_group_id is not None:
            body_param["targetGroupID"] = self.parameters.target_group_id
        if self.parameters.weight is not None:
            body_param["weight"] = self.parameters.weight
        if self.parameters.protocol_port is not None:
            body_param["protocolPort"] = self.parameters.protocol_port
        if self.parameters.instance_type is not None:
            body_param["instanceType"] = self.parameters.instance_type
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.instance_ip is not None:
            body_param["instanceIP"] = self.parameters.instance_ip
        if self.parameters.instance_v_p_c is not None:
            body_param["instanceVPC"] = self.parameters.instance_v_p_c
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


class CreateTargetRequestParam(object):

    def __init__(self, region_id, target_group_id, instance_id, weight=None, protocol_port=None, instance_type=None, description=None, client_token=None, instance_ip=None, instance_v_p_c=None):
        """
        :param region_id: 区域ID
        :param target_group_id: 后端服务组ID
        :param weight: 权重。取值范围：1-256，默认为100
        :param protocol_port: 协议端口。取值范围：1-65535（后端服务组开启全端口后，该参数不填或传0，否则必填）
        :param instance_type: 默认云主机/裸金属不用传，IP时必须要指定的 InstanceType，私有云直接根据主机id即可判断主机类型，没有实际用途实例类型。取值范围：VM、BM、ENIC（ENIC暂不支持）、IP、IDC；acs/3.0资源池仅支持VM BM IP(本端IP)
        :param instance_id: 实例ID，若instanceType为IP，则为对应网卡的ID,其他类型均为实例ID
        :param description: 描述
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param instance_ip: 后端服务 ip
        :param instance_v_p_c: 当 instanceType 为 IDC 时，必须传
        """
        self.region_id = region_id
        self.target_group_id = target_group_id
        self.weight = weight
        self.protocol_port = protocol_port
        self.instance_type = instance_type
        self.instance_id = instance_id
        self.description = description
        self.client_token = client_token
        self.instance_ip = instance_ip
        self.instance_v_p_c = instance_v_p_c

    def set_weight(self, weight):
        """
        :param weight: 权重。取值范围：1-256，默认为100
        """
        self.weight = weight

    def set_protocol_port(self, protocol_port):
        """
        :param protocol_port: 协议端口。取值范围：1-65535（后端服务组开启全端口后，该参数不填或传0，否则必填）
        """
        self.protocol_port = protocol_port

    def set_instance_type(self, instance_type):
        """
        :param instance_type: 默认云主机/裸金属不用传，IP时必须要指定的 InstanceType，私有云直接根据主机id即可判断主机类型，没有实际用途实例类型。取值范围：VM、BM、ENIC（ENIC暂不支持）、IP、IDC；acs/3.0资源池仅支持VM BM IP(本端IP)
        """
        self.instance_type = instance_type

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_instance_ip(self, instance_ip):
        """
        :param instance_ip: 后端服务 ip
        """
        self.instance_ip = instance_ip

    def set_instance_v_p_c(self, instance_v_p_c):
        """
        :param instance_v_p_c: 当 instanceType 为 IDC 时，必须传
        """
        self.instance_v_p_c = instance_v_p_c

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.target_group_id is None:
            raise Exception("target_group_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")

