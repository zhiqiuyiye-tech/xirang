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


class CreateHavipRequest(CTYunRequest):
    """
    创建高可用虚IP   
    混合云入参多projectID字段，非必填，传入正确的uuid形式的projectID会校验企业项目；clientToken字段不影响业务混合云补充为非必填。
    """

    def __init__(self, request_param):
        super(CreateHavipRequest, self).__init__("/v4/vpc/havip/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.ip_address is not None:
            body_param["ipAddress"] = self.parameters.ip_address
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.vip_type is not None:
            body_param["vipType"] = self.parameters.vip_type
        if self.parameters.network_id is not None:
            body_param["networkID"] = self.parameters.network_id
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreateHavipRequestParam(object):

    def __init__(self, region_id, subnet_id, description=None, ip_address=None, vip_type=None, network_id=None, project_id=None, client_token=None):
        """
        :param region_id: 资源池ID
        :param description: VIP 描述信息,0-128个字符
        :param ip_address: VIP 地址
        :param subnet_id: 子网 ID
        :param vip_type: VIP类型 虚拟IP的类型，v4-IPv4类型虚IP，v6-IPv6类型虚IP
        :param network_id: VPC ID 此字段再私有云没有意义，vpc 通过subnet 获取
        :param project_id: 企业项目id（非必填，传了正确的uuid形式会校验企业项目的正确性）
        :param client_token: 可传但是不进行校验， 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一 （非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.description = description
        self.ip_address = ip_address
        self.subnet_id = subnet_id
        self.vip_type = vip_type
        self.network_id = network_id
        self.project_id = project_id
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: VIP 描述信息,0-128个字符
        """
        self.description = description

    def set_ip_address(self, ip_address):
        """
        :param ip_address: VIP 地址
        """
        self.ip_address = ip_address

    def set_vip_type(self, vip_type):
        """
        :param vip_type: VIP类型 虚拟IP的类型，v4-IPv4类型虚IP，v6-IPv6类型虚IP
        """
        self.vip_type = vip_type

    def set_network_id(self, network_id):
        """
        :param network_id: VPC ID 此字段再私有云没有意义，vpc 通过subnet 获取
        """
        self.network_id = network_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id（非必填，传了正确的uuid形式会校验企业项目的正确性）
        """
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验， 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一 （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

