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


class CdaVpcUpdateRequest(CTYunRequest):
    """
    仅支持修改子网
    """

    def __init__(self, request_param):
        super(CdaVpcUpdateRequest, self).__init__("/v4/cda/vpc/update", "POST", "cda", "application/json")
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
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.vpc_subnet is not None:
            body_param["vpcSubnet"] = self.parameters.vpc_subnet
        if self.parameters.vpc_subnet_ipv6 is not None:
            body_param["vpcSubnetIPv6"] = self.parameters.vpc_subnet_ipv6
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
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


class CdaVpcUpdateRequestParam(object):

    def __init__(self, bandwidth, ip_version, vpc_id, gateway_name, region_id=None, vpc_subnet=None, vpc_subnet_ipv6=None, resource_pool=None, account=None):
        """
        :param region_id: 资源池ID，此接口中无实际意义
        :param bandwidth: 单位MB
        :param ip_version: IPV4 （默认)/DUALSTACK/IPV6(三选一)
        :param vpc_id: VPC ID
        :param vpc_subnet: vpc ipv4子网列表(IPv4和DUALSTACK必填) 注意:此参数为数组
        :param vpc_subnet_ipv6: vpc ipv6子网列表(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略) 注意:此参数为数组
        :param gateway_name: 网关名称
        :param resource_pool: 资源池id，此接口中无实际意义
        :param account: 此接口中无实际意义
        """
        self.region_id = region_id
        self.bandwidth = bandwidth
        self.ip_version = ip_version
        self.vpc_id = vpc_id
        self.vpc_subnet = vpc_subnet
        self.vpc_subnet_ipv6 = vpc_subnet_ipv6
        self.gateway_name = gateway_name
        self.resource_pool = resource_pool
        self.account = account

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID，此接口中无实际意义
        """
        self.region_id = region_id

    def set_vpc_subnet(self, vpc_subnet):
        """
        :param vpc_subnet: vpc ipv4子网列表(IPv4和DUALSTACK必填)
        """
        self.vpc_subnet = vpc_subnet

    def set_vpc_subnet_ipv6(self, vpc_subnet_ipv6):
        """
        :param vpc_subnet_ipv6: vpc ipv6子网列表(IPv6和DUALSTACK必填)  (公有云字段，混合云暂不匹配，忽略)
        """
        self.vpc_subnet_ipv6 = vpc_subnet_ipv6

    def set_resource_pool(self, resource_pool):
        """
        :param resource_pool: 资源池id，此接口中无实际意义
        """
        self.resource_pool = resource_pool

    def set_account(self, account):
        """
        :param account: 此接口中无实际意义
        """
        self.account = account

    def check_param(self):
        """
        the param required check
        """
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")

