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


class CreateLoadBalancerRequest(CTYunRequest):
    """
    创建负载均衡实例，创建elb时，eipID绑定失败会报错(eip已经被绑定/eip不存在)   
    
    """

    def __init__(self, request_param):
        super(CreateLoadBalancerRequest, self).__init__("/v4/elb/create-loadbalancer", "POST", "ctelb", "application/json")
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
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.private_ip_address is not None:
            body_param["privateIpAddress"] = self.parameters.private_ip_address
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.sla_name is not None:
            body_param["slaName"] = self.parameters.sla_name
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.delete_protection is not None:
            body_param["deleteProtection"] = self.parameters.delete_protection
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.gw_enabled is not None:
            body_param["gwEnabled"] = self.parameters.gw_enabled
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


class CreateLoadBalancerRequestParam(object):

    def __init__(self, region_id, subnet_id, name, sla_name, description=None, private_ip_address=None, vpc_id=None, eip_id=None, resource_type=None, delete_protection=None, client_token=None, project_id=None, gw_enabled=None):
        """
        :param region_id: 资源id
        :param subnet_id: 子网ID
        :param name: 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        :param vpc_id: vpc id 。 私有云传了也不校验，可以忽略。
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        :param sla_name: lb的规格名称:4.0资源池支持：elb.s1.small，elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large  3.0资源池：支持：CLASSICAL，STANDARD_1，EHANCED_1，ADVANCED_1，HIGH_1，EXTREME_1
        :param resource_type: 源类型。internal：内网负载均衡，external：公网负载均衡（公有云新增，实际不传不影响），默认internal
        :param delete_protection: 删除保护。false（不开启）、true（开）。 默认：不开启
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 企业项目ID，默认使用子网所属企业项目
        :param gw_enabled: 是否开启防火墙引流，2.2.6版本支持
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.private_ip_address = private_ip_address
        self.vpc_id = vpc_id
        self.eip_id = eip_id
        self.sla_name = sla_name
        self.resource_type = resource_type
        self.delete_protection = delete_protection
        self.client_token = client_token
        self.project_id = project_id
        self.gw_enabled = gw_enabled

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_private_ip_address(self, private_ip_address):
        """
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        """
        self.private_ip_address = private_ip_address

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc id 。 私有云传了也不校验，可以忽略。
        """
        self.vpc_id = vpc_id

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        """
        self.eip_id = eip_id

    def set_resource_type(self, resource_type):
        """
        :param resource_type: 源类型。internal：内网负载均衡，external：公网负载均衡（公有云新增，实际不传不影响），默认internal
        """
        self.resource_type = resource_type

    def set_delete_protection(self, delete_protection):
        """
        :param delete_protection: 删除保护。false（不开启）、true（开）。 默认：不开启
        """
        self.delete_protection = delete_protection

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认使用子网所属企业项目
        """
        self.project_id = project_id

    def set_gw_enabled(self, gw_enabled):
        """
        :param gw_enabled: 是否开启防火墙引流，2.2.6版本支持
        """
        self.gw_enabled = gw_enabled

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.sla_name is None:
            raise Exception("sla_name can not None")

