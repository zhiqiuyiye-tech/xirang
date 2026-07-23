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


class BindHavipRequest(CTYunRequest):
    """
    v2绑定为同步操作，绑定成功为done的状态，若异常会直接报错
    """

    def __init__(self, request_param):
        super(BindHavipRequest, self).__init__("/v4/vpc/havip/bind", "POST", "ctvpc", "application/json")
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
        if self.parameters.ha_vip_id is not None:
            body_param["haVipID"] = self.parameters.ha_vip_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class BindHavipRequestParam(object):

    def __init__(self, region_id, ha_vip_id, resource_type, instance_id=None, az_name=None, project_id=None, network_interface_id=None, client_token=None, floating_id=None):
        """
        :param region_id: 资源池id
        :param ha_vip_id: VIP ID
        :param instance_id: ECS示例ID，当 resourceType 为 VM / PM 时，必填
        :param az_name: 可用区名称（v2该参数对齐公有云无意义）
        :param project_id: 企业项目id（非必填）
        :param resource_type: 绑定的实例类型，VM 表示虚拟机ECS, PM 表示裸金属, NETWORK 表示弹性 IP
        :param network_interface_id: 网卡ID，当绑定的实例类型为VM、PM时填写该参数生效，必填
        :param client_token: 客户端存根，可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        :param floating_id: 弹性IP ID，当 resourceType 为 NETWORK 时，必填
        """
        self.region_id = region_id
        self.ha_vip_id = ha_vip_id
        self.instance_id = instance_id
        self.az_name = az_name
        self.project_id = project_id
        self.resource_type = resource_type
        self.network_interface_id = network_interface_id
        self.client_token = client_token
        self.floating_id = floating_id

    def set_instance_id(self, instance_id):
        """
        :param instance_id: ECS示例ID，当 resourceType 为 VM / PM 时，必填
        """
        self.instance_id = instance_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（v2该参数对齐公有云无意义）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id（非必填）
        """
        self.project_id = project_id

    def set_network_interface_id(self, network_interface_id):
        """
        :param network_interface_id: 网卡ID，当绑定的实例类型为VM、PM时填写该参数生效，必填
        """
        self.network_interface_id = network_interface_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

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
        if self.ha_vip_id is None:
            raise Exception("ha_vip_id can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")

