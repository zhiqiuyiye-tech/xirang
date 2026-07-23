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


class CreateSubnetRequest(CTYunRequest):
    """
    创建子网。   
       
    ## 接口约束   
       
    调用该接口创建 Subnet 时，请注意：   
       
    - 一个 Subnet 只能指定一个网段，创建后无法修改网段。   
    - 共享vpc在共享企业项目下创建子网时需要指定共享企业项目的路由表   
       
    ## 接口差别   
    混合云入参多azName，非必填字段；缺clientToken字段，必填字段，字段不影响接口功能，混合云不必填当作对齐。
    """

    def __init__(self, request_param):
        super(CreateSubnetRequest, self).__init__("/v4/vpc/create-subnet", "POST", "ctvpc", "application/json")
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
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.cidr is not None:
            body_param["CIDR"] = self.parameters.cidr
        if self.parameters.enable_ipv6 is not None:
            body_param["enableIpv6"] = self.parameters.enable_ipv6
        if self.parameters.subnet_type is not None:
            body_param["subnetType"] = self.parameters.subnet_type
        if self.parameters.dns_list is not None:
            body_param["dnsList"] = self.parameters.dns_list
        if self.parameters.subnet_gateway_ip is not None:
            body_param["subnetGatewayIP"] = self.parameters.subnet_gateway_ip
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.route_table_id is not None:
            body_param["routeTableID"] = self.parameters.route_table_id
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreateSubnetRequestParam(object):

    def __init__(self, region_id, name, vpc_id, cidr, az_name=None, enable_ipv6=None, subnet_type=None, dns_list=None, subnet_gateway_ip=None, description=None, route_table_id=None, project_id=None):
        """
        :param region_id: 资源池 ID
        :param name: subnet名称。只能由数字，字母，中文，下划线，连字符组成，中文 / 英文字母开头，不能以 http: / https: 开头，长度 2 - 32
        :param vpc_id: 虚拟私有云uuid
        :param az_name: 可用区名称   
         (差异点说明：公有云文档无此参数，j2.0已对齐，若需要传此参数，2.0传参为az1,az2等，建议不区分az)
        :param cidr: 子网网段（需和VPC网段对齐，例：vpc  10.169.0.0/16、子网cidr：10.169.18.0/24，网关10.169.18.1）
        :param enable_ipv6: 是否开启 IPv6 网段。取值：false（默认值）:不开启，true: 开启
        :param subnet_type: 子网类型：common（普通子网）/ cbm（裸金属子网），默认为普通子网 | common |。私有云需要此字段，公有云不需要 
        :param dns_list: 子网dns列表,最多同时支持4个dns地址，不传入会返回默认的dns地址 注意:此参数为数组
        :param subnet_gateway_ip: 子网网关 IP
        :param description: 长度0-128，支持英文、中文、数字, 特殊字符：!~@#￥%……&*()_-+=<>?:"{},./;'[]·！（）——-+={}\\
        :param route_table_id: 路由表ID，可手动指定子网绑定的路由表（注：在共享企业项目场景下必须指定相同企业项目的路由表）
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.name = name
        self.vpc_id = vpc_id
        self.az_name = az_name
        self.cidr = cidr
        self.enable_ipv6 = enable_ipv6
        self.subnet_type = subnet_type
        self.dns_list = dns_list
        self.subnet_gateway_ip = subnet_gateway_ip
        self.description = description
        self.route_table_id = route_table_id
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称   
         (差异点说明：公有云文档无此参数，j2.0已对齐，若需要传此参数，2.0传参为az1,az2等，建议不区分az)
        """
        self.az_name = az_name

    def set_enable_ipv6(self, enable_ipv6):
        """
        :param enable_ipv6: 是否开启 IPv6 网段。取值：false（默认值）:不开启，true: 开启
        """
        self.enable_ipv6 = enable_ipv6

    def set_subnet_type(self, subnet_type):
        """
        :param subnet_type: 子网类型：common（普通子网）/ cbm（裸金属子网），默认为普通子网 | common |。私有云需要此字段，公有云不需要 
        """
        self.subnet_type = subnet_type

    def set_dns_list(self, dns_list):
        """
        :param dns_list: 子网dns列表,最多同时支持4个dns地址，不传入会返回默认的dns地址
        """
        self.dns_list = dns_list

    def set_subnet_gateway_ip(self, subnet_gateway_ip):
        """
        :param subnet_gateway_ip: 子网网关 IP
        """
        self.subnet_gateway_ip = subnet_gateway_ip

    def set_description(self, description):
        """
        :param description: 长度0-128，支持英文、中文、数字, 特殊字符：!~@#￥%……&*()_-+=<>?:"{},./;'[]·！（）——-+={}\\
        """
        self.description = description

    def set_route_table_id(self, route_table_id):
        """
        :param route_table_id: 路由表ID，可手动指定子网绑定的路由表（注：在共享企业项目场景下必须指定相同企业项目的路由表）
        """
        self.route_table_id = route_table_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.cidr is None:
            raise Exception("cidr can not None")

