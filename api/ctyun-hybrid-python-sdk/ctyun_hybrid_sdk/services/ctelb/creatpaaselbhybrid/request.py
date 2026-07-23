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


class CreatPaaSElbHybridRequest(CTYunRequest):
    """
    创建性能保障型负载均衡实例；3,0底层性能保障型没有余量，无法创建
    """

    def __init__(self, request_param):
        super(CreatPaaSElbHybridRequest, self).__init__("/v4/elb/create-pgelb", "POST", "ctelb", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.private_ip_address is not None:
            body_param["privateIpAddress"] = self.parameters.private_ip_address
        if self.parameters.sla_name is not None:
            body_param["slaName"] = self.parameters.sla_name
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class CreatPaaSElbHybridRequestParam(object):

    def __init__(self, region_id, subnet_id, name, resource_type, sla_name, client_token=None, project_id=None, vpc_id=None, description=None, eip_id=None, private_ip_address=None, cycle_type=None, cycle_count=None, gw_enabled=None):
        """
        :param client_token: 公有云文档必传
        :param region_id: 资源池ID
        :param project_id: 企业项目 ID，默认为"0"（非必填，并且此字段在私有云不具有实际意义）
        :param vpc_id: 专有网络ID
        :param subnet_id: 子网ID
        :param name: 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填，当resourceType=internal时该项不起作用，不做校验
        :param resource_type: 网络类型：internal-内网 external-外网
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        :param sla_name: lb的规格名称, 支持:elb.s2.small(标准型I)，elb.s3.small(标准型II)，elb.s4.small(增强型I)，elb.s5.small(增强型II)，elb.s2.large(高阶型I)，elb.s3.large(高阶型II)，elb.s4.large(超强型I)，elb.s5.large(超强型II)
        :param cycle_type: 订购类型：month（包月） / year（包年）/on_demand(按需)不传默认为按需
        :param cycle_count: 订购时长, 当 cycleType = month, 支持续订 1 - 11 个月; 当 cycleType = year, 支持续订 1 - 5 年
        :param gw_enabled: 是否开启防火墙引流，2.2.6版本支持
        """
        self.client_token = client_token
        self.region_id = region_id
        self.project_id = project_id
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.eip_id = eip_id
        self.resource_type = resource_type
        self.private_ip_address = private_ip_address
        self.sla_name = sla_name
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.gw_enabled = gw_enabled

    def set_client_token(self, client_token):
        """
        :param client_token: 公有云文档必传
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为"0"（非必填，并且此字段在私有云不具有实际意义）
        """
        self.project_id = project_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 专有网络ID
        """
        self.vpc_id = vpc_id

    def set_description(self, description):
        """
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$%^&*()_-+= <>?:"{},./;'[]·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填，当resourceType=internal时该项不起作用，不做校验
        """
        self.eip_id = eip_id

    def set_private_ip_address(self, private_ip_address):
        """
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        """
        self.private_ip_address = private_ip_address

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 订购类型：month（包月） / year（包年）/on_demand(按需)不传默认为按需
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长, 当 cycleType = month, 支持续订 1 - 11 个月; 当 cycleType = year, 支持续订 1 - 5 年
        """
        self.cycle_count = cycle_count

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
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.sla_name is None:
            raise Exception("sla_name can not None")

