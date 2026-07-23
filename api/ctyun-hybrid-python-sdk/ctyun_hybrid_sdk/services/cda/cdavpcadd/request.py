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


class CdaVpcAddRequest(CTYunRequest):
    """
    专线网关添加VPC
    """

    def __init__(self, request_param):
        super(CdaVpcAddRequest, self).__init__("/v4/cda/vpc/add", "POST", "cda", "application/json")
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
        if self.parameters.dc_type is not None:
            body_param["dcType"] = self.parameters.dc_type
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.vpc_name is not None:
            body_param["vpcName"] = self.parameters.vpc_name
        if self.parameters.vpc_network_segment is not None:
            body_param["vpcNetworkSegment"] = self.parameters.vpc_network_segment
        if self.parameters.vpc_network_segment_ipv6 is not None:
            body_param["vpcNetworkSegmentIPv6"] = self.parameters.vpc_network_segment_ipv6
        if self.parameters.vpc_subnet is not None:
            body_param["vpcSubnet"] = self.parameters.vpc_subnet
        if self.parameters.vpc_subnet_ipv6 is not None:
            body_param["vpcSubnetIPv6"] = self.parameters.vpc_subnet_ipv6
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


class CdaVpcAddRequestParam(object):

    def __init__(self, region_id, dc_type, bandwidth, gateway_name, ip_version, vpc_id, vpc_network_segment, vpc_subnet, account=None, vpc_name=None, vpc_network_segment_ipv6=None, vpc_subnet_ipv6=None):
        """
        :param region_id: 区域ID
        :param dc_type: vpc的资源池类型(CNP/EMAZ) 4.0默认传EMAZ
        :param account: 天翼云账号，此接口中无实际意义
        :param bandwidth: 带宽(M)
        :param gateway_name: 专线网关名称（唯一）（只能是字母和数字）
        :param ip_version: IPV4 （默认)/DUALSTACK/IPV6(三选一)
        :param vpc_id: VPC ID
        :param vpc_name: 此接口中无实际意义
        :param vpc_network_segment: VPC网段(IPv4或DUALSTACK必填)	 公有云非必传，混合云必传
        :param vpc_network_segment_ipv6: VPC网段(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略)
        :param vpc_subnet: vpc ipv4子网列表(IPv4和DUALSTACK必填)   公有云非必传，混合云必传 注意:此参数为数组
        :param vpc_subnet_ipv6: vpc ipv6子网列表(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略) 注意:此参数为数组
        """
        self.region_id = region_id
        self.dc_type = dc_type
        self.account = account
        self.bandwidth = bandwidth
        self.gateway_name = gateway_name
        self.ip_version = ip_version
        self.vpc_id = vpc_id
        self.vpc_name = vpc_name
        self.vpc_network_segment = vpc_network_segment
        self.vpc_network_segment_ipv6 = vpc_network_segment_ipv6
        self.vpc_subnet = vpc_subnet
        self.vpc_subnet_ipv6 = vpc_subnet_ipv6

    def set_account(self, account):
        """
        :param account: 天翼云账号，此接口中无实际意义
        """
        self.account = account

    def set_vpc_name(self, vpc_name):
        """
        :param vpc_name: 此接口中无实际意义
        """
        self.vpc_name = vpc_name

    def set_vpc_network_segment_ipv6(self, vpc_network_segment_ipv6):
        """
        :param vpc_network_segment_ipv6: VPC网段(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略)
        """
        self.vpc_network_segment_ipv6 = vpc_network_segment_ipv6

    def set_vpc_subnet_ipv6(self, vpc_subnet_ipv6):
        """
        :param vpc_subnet_ipv6: vpc ipv6子网列表(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略)
        """
        self.vpc_subnet_ipv6 = vpc_subnet_ipv6

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.dc_type is None:
            raise Exception("dc_type can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.vpc_network_segment is None:
            raise Exception("vpc_network_segment can not None")
        if self.vpc_subnet is None:
            raise Exception("vpc_subnet can not None")

