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


class CtvpnConnectionAddRequest(CTYunRequest):
    """
    VPN连接创建
    """

    def __init__(self, request_param):
        super(CtvpnConnectionAddRequest, self).__init__("/v4/vpn/connection/add", "POST", "ctvpn", "application/json")
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
        if self.parameters.dst_cidr is not None:
            body_param["dstCidr"] = self.parameters.dst_cidr
        if self.parameters.vpn_gateway_id is not None:
            body_param["vpnGatewayID"] = self.parameters.vpn_gateway_id
        if self.parameters.user_gateway_id is not None:
            body_param["userGatewayID"] = self.parameters.user_gateway_id
        if self.parameters.transform_protocol is not None:
            body_param["transformProtocol"] = self.parameters.transform_protocol
        if self.parameters.src_subnet is not None:
            body_param["srcSubnet"] = self.parameters.src_subnet
        if self.parameters.psk is not None:
            body_param["psk"] = self.parameters.psk
        if self.parameters.phase1_negotiation_mode is not None:
            body_param["phase1NegotiationMode"] = self.parameters.phase1_negotiation_mode
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.ike_auth_algorithm is not None:
            body_param["ikeAuthAlgorithm"] = self.parameters.ike_auth_algorithm
        if self.parameters.ike_encryption_algorithm is not None:
            body_param["ikeEncryptionAlgorithm"] = self.parameters.ike_encryption_algorithm
        if self.parameters.ike_lifetime is not None:
            body_param["ikeLifetime"] = self.parameters.ike_lifetime
        if self.parameters.ike_pfs is not None:
            body_param["ikePfs"] = self.parameters.ike_pfs
        if self.parameters.ike_version is not None:
            body_param["ikeVersion"] = self.parameters.ike_version
        if self.parameters.ipsec_auth_algorithm is not None:
            body_param["ipsecAuthAlgorithm"] = self.parameters.ipsec_auth_algorithm
        if self.parameters.ipsec_pfs is not None:
            body_param["ipsecPfs"] = self.parameters.ipsec_pfs
        if self.parameters.ipsec_life_time is not None:
            body_param["ipsecLifeTime"] = self.parameters.ipsec_life_time
        if self.parameters.ipsec_encryption_algorithm is not None:
            body_param["ipsecEncryptionAlgorithm"] = self.parameters.ipsec_encryption_algorithm
        if self.parameters.customer_id is not None:
            body_param["customerID"] = self.parameters.customer_id
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


class CtvpnConnectionAddRequestParam(object):

    def __init__(self, dst_cidr, vpn_gateway_id, user_gateway_id, src_subnet, psk, region_id, name, transform_protocol=None, phase1_negotiation_mode=None, ike_auth_algorithm=None, ike_encryption_algorithm=None, ike_lifetime=None, ike_pfs=None, ike_version=None, ipsec_auth_algorithm=None, ipsec_pfs=None, ipsec_life_time=None, ipsec_encryption_algorithm=None, customer_id=None):
        """
        :param dst_cidr: 对端网段["192.168.0.0/24"] 注意:此参数为数组
        :param vpn_gateway_id: vpn网关id
        :param user_gateway_id: 用户网关id
        :param transform_protocol: ipsec传输协议，默认值ESP
        :param src_subnet: 本端子网["192.168.0.0/24"] 注意:此参数为数组
        :param psk: 密钥 需要做base64编码
        :param phase1_negotiation_mode: 协商模式，默认值Main，选择IKEVerion时策略版本为“v1”时,可以配置协商模式取值支持Main、Aggressive。
        :param region_id: 区域id
        :param name: 名称，长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param ike_auth_algorithm: ike认证算法，默认值SHA1，支持的算法:SHA1 SHA256 SHA384 SHA512
        :param ike_encryption_algorithm: ike加密算法，默认值AES-128，支持的算法:AES-128、AES-192、AES-   
         256、3DES。
        :param ike_lifetime: ike生命周期，默认值86400，安全联盟(SA一SecuitxAssociations)的生存时间，单位:秒。在超过生存时间后，安全联盟将被重新协商。
        :param ike_pfs: DH算法，默认值Group5
        :param ike_version: ike版本，默认值v1，支持的版本:v1、v2。
        :param ipsec_auth_algorithm: ipsec认证算法，默认值SHA1
        :param ipsec_pfs: PFS，默认值DH Group5，可选值 DH Group5 DH Group2 DH Group14
        :param ipsec_life_time: ipsec生命周期，默认值3600
        :param ipsec_encryption_algorithm: ipsec加密算法，默认值AES-128
        :param customer_id: 用户id，此接口中无实际意义
        """
        self.dst_cidr = dst_cidr
        self.vpn_gateway_id = vpn_gateway_id
        self.user_gateway_id = user_gateway_id
        self.transform_protocol = transform_protocol
        self.src_subnet = src_subnet
        self.psk = psk
        self.phase1_negotiation_mode = phase1_negotiation_mode
        self.region_id = region_id
        self.name = name
        self.ike_auth_algorithm = ike_auth_algorithm
        self.ike_encryption_algorithm = ike_encryption_algorithm
        self.ike_lifetime = ike_lifetime
        self.ike_pfs = ike_pfs
        self.ike_version = ike_version
        self.ipsec_auth_algorithm = ipsec_auth_algorithm
        self.ipsec_pfs = ipsec_pfs
        self.ipsec_life_time = ipsec_life_time
        self.ipsec_encryption_algorithm = ipsec_encryption_algorithm
        self.customer_id = customer_id

    def set_transform_protocol(self, transform_protocol):
        """
        :param transform_protocol: ipsec传输协议，默认值ESP
        """
        self.transform_protocol = transform_protocol

    def set_phase1_negotiation_mode(self, phase1_negotiation_mode):
        """
        :param phase1_negotiation_mode: 协商模式，默认值Main，选择IKEVerion时策略版本为“v1”时,可以配置协商模式取值支持Main、Aggressive。
        """
        self.phase1_negotiation_mode = phase1_negotiation_mode

    def set_ike_auth_algorithm(self, ike_auth_algorithm):
        """
        :param ike_auth_algorithm: ike认证算法，默认值SHA1，支持的算法:SHA1 SHA256 SHA384 SHA512
        """
        self.ike_auth_algorithm = ike_auth_algorithm

    def set_ike_encryption_algorithm(self, ike_encryption_algorithm):
        """
        :param ike_encryption_algorithm: ike加密算法，默认值AES-128，支持的算法:AES-128、AES-192、AES-   
         256、3DES。
        """
        self.ike_encryption_algorithm = ike_encryption_algorithm

    def set_ike_lifetime(self, ike_lifetime):
        """
        :param ike_lifetime: ike生命周期，默认值86400，安全联盟(SA一SecuitxAssociations)的生存时间，单位:秒。在超过生存时间后，安全联盟将被重新协商。
        """
        self.ike_lifetime = ike_lifetime

    def set_ike_pfs(self, ike_pfs):
        """
        :param ike_pfs: DH算法，默认值Group5
        """
        self.ike_pfs = ike_pfs

    def set_ike_version(self, ike_version):
        """
        :param ike_version: ike版本，默认值v1，支持的版本:v1、v2。
        """
        self.ike_version = ike_version

    def set_ipsec_auth_algorithm(self, ipsec_auth_algorithm):
        """
        :param ipsec_auth_algorithm: ipsec认证算法，默认值SHA1
        """
        self.ipsec_auth_algorithm = ipsec_auth_algorithm

    def set_ipsec_pfs(self, ipsec_pfs):
        """
        :param ipsec_pfs: PFS，默认值DH Group5，可选值 DH Group5 DH Group2 DH Group14
        """
        self.ipsec_pfs = ipsec_pfs

    def set_ipsec_life_time(self, ipsec_life_time):
        """
        :param ipsec_life_time: ipsec生命周期，默认值3600
        """
        self.ipsec_life_time = ipsec_life_time

    def set_ipsec_encryption_algorithm(self, ipsec_encryption_algorithm):
        """
        :param ipsec_encryption_algorithm: ipsec加密算法，默认值AES-128
        """
        self.ipsec_encryption_algorithm = ipsec_encryption_algorithm

    def set_customer_id(self, customer_id):
        """
        :param customer_id: 用户id，此接口中无实际意义
        """
        self.customer_id = customer_id

    def check_param(self):
        """
        the param required check
        """
        if self.dst_cidr is None:
            raise Exception("dst_cidr can not None")
        if self.vpn_gateway_id is None:
            raise Exception("vpn_gateway_id can not None")
        if self.user_gateway_id is None:
            raise Exception("user_gateway_id can not None")
        if self.src_subnet is None:
            raise Exception("src_subnet can not None")
        if self.psk is None:
            raise Exception("psk can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")

