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


class ModifyServiceIPVersionRequest(CTYunRequest):
    """
    添加终端节点白名单
    """

    def __init__(self, request_param):
        super(ModifyServiceIPVersionRequest, self).__init__("/v4/vpce/modify-endpoint-service-ip-version", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.instance_id_v6 is not None:
            body_param["instanceIDV6"] = self.parameters.instance_id_v6
        if self.parameters.underlay_ip6 is not None:
            body_param["underlayIp6"] = self.parameters.underlay_ip6
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.ipv6_address is not None:
            body_param["ipv6Address"] = self.parameters.ipv6_address
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


class ModifyServiceIPVersionRequestParam(object):

    def __init__(self, region_id, endpoint_service_id, client_token=None, ip_version=None, instance_id_v6=None, underlay_ip6=None, subnet_id=None, ipv6_address=None):
        """
        :param region_id: 资源池ID
        :param endpoint_service_id: 终端节点服务ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈
        :param instance_id_v6: 后端ipv6实例id，服务后端为vip时必填
        :param underlay_ip6: ipv6 underlay ip，服务为天翼云服务时必填
        :param subnet_id: 子网ID，overlay反向型终端节点服务必填（暂不支持）
        :param ipv6_address: 反向型终端节点服务ipv6中转ip（暂不支持）
        """
        self.region_id = region_id
        self.endpoint_service_id = endpoint_service_id
        self.client_token = client_token
        self.ip_version = ip_version
        self.instance_id_v6 = instance_id_v6
        self.underlay_ip6 = underlay_ip6
        self.subnet_id = subnet_id
        self.ipv6_address = ipv6_address

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        """
        self.client_token = client_token

    def set_ip_version(self, ip_version):
        """
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈
        """
        self.ip_version = ip_version

    def set_instance_id_v6(self, instance_id_v6):
        """
        :param instance_id_v6: 后端ipv6实例id，服务后端为vip时必填
        """
        self.instance_id_v6 = instance_id_v6

    def set_underlay_ip6(self, underlay_ip6):
        """
        :param underlay_ip6: ipv6 underlay ip，服务为天翼云服务时必填
        """
        self.underlay_ip6 = underlay_ip6

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网ID，overlay反向型终端节点服务必填（暂不支持）
        """
        self.subnet_id = subnet_id

    def set_ipv6_address(self, ipv6_address):
        """
        :param ipv6_address: 反向型终端节点服务ipv6中转ip（暂不支持）
        """
        self.ipv6_address = ipv6_address

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")

