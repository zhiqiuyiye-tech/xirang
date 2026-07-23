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


class AsyncCreateLoadbalanceRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容创建4.0资源
    """

    def __init__(self, request_param):
        super(AsyncCreateLoadbalanceRequest, self).__init__("/v4/elb/async-create-loadbalance", "POST", "ctelb", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.private_ip_address is not None:
            body_param["privateIpAddress"] = self.parameters.private_ip_address
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
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


class AsyncCreateLoadbalanceRequestParam(object):

    def __init__(self, client_token, region_id, subnet_id, name, resource_type, vpc_id=None, description=None, private_ip_address=None, eip_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池id
        :param vpc_id: vpc的ID
        :param subnet_id: 子网的ID
        :param name: 名称
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        :param resource_type: 资源类型。internal：内网负载均衡，external：公网负载均衡
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        """
        self.client_token = client_token
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.resource_type = resource_type
        self.private_ip_address = private_ip_address
        self.eip_id = eip_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc的ID
        """
        self.vpc_id = vpc_id

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

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        """
        self.eip_id = eip_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")

