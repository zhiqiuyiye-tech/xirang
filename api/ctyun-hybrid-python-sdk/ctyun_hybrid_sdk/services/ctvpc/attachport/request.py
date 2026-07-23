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


class AttachPortRequest(CTYunRequest):
    """
    网卡绑定实例   
    ### 接口约束
    """

    def __init__(self, request_param):
        super(AttachPortRequest, self).__init__("/v4/ports/attach", "POST", "ctvpc", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.instance_type is not None:
            body_param["instanceType"] = self.parameters.instance_type
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class AttachPortRequestParam(object):

    def __init__(self, region_id, network_interface_id, instance_id, instance_type, az_name=None, client_token=None):
        """
        :param region_id: 
        :param network_interface_id: 网卡id
        :param instance_id: 云主机id
        :param instance_type: 实例类型：3-虚拟机 4-裸金属(2.2.4版本支持)
        :param az_name: 可用区名称（实际无作用，底层传参不需要可用区）
        :param client_token: 公有云需要暂无功能
        """
        self.region_id = region_id
        self.network_interface_id = network_interface_id
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.az_name = az_name
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（实际无作用，底层传参不需要可用区）
        """
        self.az_name = az_name

    def set_client_token(self, client_token):
        """
        :param client_token: 公有云需要暂无功能
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.instance_type is None:
            raise Exception("instance_type can not None")

