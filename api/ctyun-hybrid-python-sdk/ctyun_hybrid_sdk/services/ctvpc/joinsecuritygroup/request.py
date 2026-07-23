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


class JoinSecurityGroupRequest(CTYunRequest):
    """
    绑定安全组。主机和安全组需要在同一个VPC下才能够进行绑定（4.0）
    """

    def __init__(self, request_param):
        super(JoinSecurityGroupRequest, self).__init__("/v4/vpc/join-security-group", "POST", "ctvpc", "application/json")
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
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
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


class JoinSecurityGroupRequestParam(object):

    def __init__(self, region_id, security_group_id, instance_id, action=None, network_interface_id=None):
        """
        :param region_id: 资源池ID
        :param security_group_id: 安全组ID
        :param instance_id: 主机ID /UUID
        :param action: 系统规定参数：joinSecurityGroup 兼容旧文档，不做校验
        :param network_interface_id: 弹性网卡ID，归属于instanceID实例,指定后仅给该网卡绑定安全组
        """
        self.region_id = region_id
        self.security_group_id = security_group_id
        self.instance_id = instance_id
        self.action = action
        self.network_interface_id = network_interface_id

    def set_action(self, action):
        """
        :param action: 系统规定参数：joinSecurityGroup 兼容旧文档，不做校验
        """
        self.action = action

    def set_network_interface_id(self, network_interface_id):
        """
        :param network_interface_id: 弹性网卡ID，归属于instanceID实例,指定后仅给该网卡绑定安全组
        """
        self.network_interface_id = network_interface_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.security_group_id is None:
            raise Exception("security_group_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")

