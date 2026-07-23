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


class UnbindHavipRequest(CTYunRequest):
    """
    v2绑定为同步操作，若异常会直接报错   
       
    ### 接口约束   
    此接口只能在port绑定了havip并且port绑定了实例时使用，否则解绑时会返回失败。   
    当resourceType 为VM、PM时 instanceID不能为空，当类型为NETWORK 时floatingID 值不允许为空。
    """

    def __init__(self, request_param):
        super(UnbindHavipRequest, self).__init__("/v4/vpc/havip/unbind", "POST", "ctvpc", "application/json")
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
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.ha_vip_id is not None:
            body_param["haVipID"] = self.parameters.ha_vip_id
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.floating_id is not None:
            body_param["floatingID"] = self.parameters.floating_id
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


class UnbindHavipRequestParam(object):

    def __init__(self, region_id, resource_type, ha_vip_id, client_token=None, network_interface_id=None, instance_id=None, floating_id=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param resource_type: 绑定的实例类型，VM 表示虚拟机ECS, PM 表示裸金属, NETWORK 表示弹性 IP
        :param ha_vip_id: 高可用虚IP的ID
        :param network_interface_id: 虚拟网卡ID，当resourceType 为 VM / PM 时必传
        :param instance_id: ECS示例ID，当 resourceType 为 VM / PM 时，必填
        :param floating_id: 弹性IP ID，当 resourceType 为 NETWORK 时，必填
        """
        self.client_token = client_token
        self.region_id = region_id
        self.resource_type = resource_type
        self.ha_vip_id = ha_vip_id
        self.network_interface_id = network_interface_id
        self.instance_id = instance_id
        self.floating_id = floating_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_network_interface_id(self, network_interface_id):
        """
        :param network_interface_id: 虚拟网卡ID，当resourceType 为 VM / PM 时必传
        """
        self.network_interface_id = network_interface_id

    def set_instance_id(self, instance_id):
        """
        :param instance_id: ECS示例ID，当 resourceType 为 VM / PM 时，必填
        """
        self.instance_id = instance_id

    def set_floating_id(self, floating_id):
        """
        :param floating_id: 弹性IP ID，当 resourceType 为 NETWORK 时，必填
        """
        self.floating_id = floating_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.ha_vip_id is None:
            raise Exception("ha_vip_id can not None")

