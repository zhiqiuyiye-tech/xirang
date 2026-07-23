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


class CtvpnConnectionUpdateRequest(CTYunRequest):
    """
    VPN连接修改
    """

    def __init__(self, request_param):
        super(CtvpnConnectionUpdateRequest, self).__init__("/v4/vpn/connection/update", "POST", "ctvpn", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.dst_cidr is not None:
            body_param["dstCidr"] = self.parameters.dst_cidr
        if self.parameters.psk is not None:
            body_param["psk"] = self.parameters.psk
        if self.parameters.src_subnet is not None:
            body_param["srcSubnet"] = self.parameters.src_subnet
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
        if self.parameters.ipsec_encryption_algorithm is not None:
            body_param["ipsecEncryptionAlgorithm"] = self.parameters.ipsec_encryption_algorithm
        if self.parameters.ipsec_lifetime is not None:
            body_param["ipsecLifetime"] = self.parameters.ipsec_lifetime
        if self.parameters.ipsec_pfs is not None:
            body_param["ipsecPfs"] = self.parameters.ipsec_pfs
        if self.parameters.phase1_negotiation_mode is not None:
            body_param["phase1NegotiationMode"] = self.parameters.phase1_negotiation_mode
        if self.parameters.transform_protocol is not None:
            body_param["transformProtocol"] = self.parameters.transform_protocol
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


class CtvpnConnectionUpdateRequestParam(object):

    def __init__(self, region_id, name, id, dst_cidr, psk, src_subnet, ike_auth_algorithm=None, ike_encryption_algorithm=None, ike_lifetime=None, ike_pfs=None, ike_version=None, ipsec_auth_algorithm=None, ipsec_encryption_algorithm=None, ipsec_lifetime=None, ipsec_pfs=None, phase1_negotiation_mode=None, transform_protocol=None, customer_id=None):
        """
        :param region_id: 资源池id
        :param name: 名称，长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param id: vpn连接id
        :param dst_cidr: 对端网段["192.168.0.0/24"] 注意:此参数为数组
        :param psk: 密钥 需要做base64编码
        :param src_subnet: 本端子网["192.168.0.0/24"] 注意:此参数为数组
        :param ike_auth_algorithm: ike认证算法
        :param ike_encryption_algorithm: ike加密算法
        :param ike_lifetime: ike生命周期
        :param ike_pfs: DH算法
        :param ike_version: 支持的版本:v1、v2。
        :param ipsec_auth_algorithm: ipsec认证算法
        :param ipsec_encryption_algorithm: ipsec加密算法
        :param ipsec_lifetime: ipsec生命周期
        :param ipsec_pfs: 可选值 DH Group5 DH Group2 DH Group14
        :param phase1_negotiation_mode: 协商模式
        :param transform_protocol: ipsec传输协议
        :param customer_id: 用户id，此接口中无实际意义
        """
        self.region_id = region_id
        self.name = name
        self.id = id
        self.dst_cidr = dst_cidr
        self.psk = psk
        self.src_subnet = src_subnet
        self.ike_auth_algorithm = ike_auth_algorithm
        self.ike_encryption_algorithm = ike_encryption_algorithm
        self.ike_lifetime = ike_lifetime
        self.ike_pfs = ike_pfs
        self.ike_version = ike_version
        self.ipsec_auth_algorithm = ipsec_auth_algorithm
        self.ipsec_encryption_algorithm = ipsec_encryption_algorithm
        self.ipsec_lifetime = ipsec_lifetime
        self.ipsec_pfs = ipsec_pfs
        self.phase1_negotiation_mode = phase1_negotiation_mode
        self.transform_protocol = transform_protocol
        self.customer_id = customer_id

    def set_ike_auth_algorithm(self, ike_auth_algorithm):
        """
        :param ike_auth_algorithm: ike认证算法
        """
        self.ike_auth_algorithm = ike_auth_algorithm

    def set_ike_encryption_algorithm(self, ike_encryption_algorithm):
        """
        :param ike_encryption_algorithm: ike加密算法
        """
        self.ike_encryption_algorithm = ike_encryption_algorithm

    def set_ike_lifetime(self, ike_lifetime):
        """
        :param ike_lifetime: ike生命周期
        """
        self.ike_lifetime = ike_lifetime

    def set_ike_pfs(self, ike_pfs):
        """
        :param ike_pfs: DH算法
        """
        self.ike_pfs = ike_pfs

    def set_ike_version(self, ike_version):
        """
        :param ike_version: 支持的版本:v1、v2。
        """
        self.ike_version = ike_version

    def set_ipsec_auth_algorithm(self, ipsec_auth_algorithm):
        """
        :param ipsec_auth_algorithm: ipsec认证算法
        """
        self.ipsec_auth_algorithm = ipsec_auth_algorithm

    def set_ipsec_encryption_algorithm(self, ipsec_encryption_algorithm):
        """
        :param ipsec_encryption_algorithm: ipsec加密算法
        """
        self.ipsec_encryption_algorithm = ipsec_encryption_algorithm

    def set_ipsec_lifetime(self, ipsec_lifetime):
        """
        :param ipsec_lifetime: ipsec生命周期
        """
        self.ipsec_lifetime = ipsec_lifetime

    def set_ipsec_pfs(self, ipsec_pfs):
        """
        :param ipsec_pfs: 可选值 DH Group5 DH Group2 DH Group14
        """
        self.ipsec_pfs = ipsec_pfs

    def set_phase1_negotiation_mode(self, phase1_negotiation_mode):
        """
        :param phase1_negotiation_mode: 协商模式
        """
        self.phase1_negotiation_mode = phase1_negotiation_mode

    def set_transform_protocol(self, transform_protocol):
        """
        :param transform_protocol: ipsec传输协议
        """
        self.transform_protocol = transform_protocol

    def set_customer_id(self, customer_id):
        """
        :param customer_id: 用户id，此接口中无实际意义
        """
        self.customer_id = customer_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.dst_cidr is None:
            raise Exception("dst_cidr can not None")
        if self.psk is None:
            raise Exception("psk can not None")
        if self.src_subnet is None:
            raise Exception("src_subnet can not None")

