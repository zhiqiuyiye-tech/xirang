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


class CreateEndpointRequest(CTYunRequest):
    """
    创建终端节点服务
    """

    def __init__(self, request_param):
        super(CreateEndpointRequest, self).__init__("/v4/vpce/create-endpoint", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_name is not None:
            body_param["endpointName"] = self.parameters.endpoint_name
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.whitelist is not None:
            body_param["whitelist"] = self.parameters.whitelist
        if self.parameters.whitelist6 is not None:
            body_param["whitelist6"] = self.parameters.whitelist6
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.whitelist_flag is not None:
            body_param["whitelistFlag"] = self.parameters.whitelist_flag
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.ip is not None:
            body_param["IP"] = self.parameters.ip
        if self.parameters.i_p6 is not None:
            body_param["IP6"] = self.parameters.i_p6
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.enable_dns is not None:
            body_param["enableDns"] = self.parameters.enable_dns
        if self.parameters.endpoint_service_type is not None:
            body_param["endpointServiceType"] = self.parameters.endpoint_service_type
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


class CreateEndpointRequestParam(object):

    def __init__(self, client_token, region_id, endpoint_name, endpoint_service_id, vpc_id, subnet_id, cycle_type, whitelist_flag, whitelist=None, whitelist6=None, description=None, ip=None, i_p6=None, ip_version=None, enable_dns=None, endpoint_service_type=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param endpoint_name: 终端节点名称，只能由数字，字母，-组成不能以数字和-开头，长度2-28
        :param endpoint_service_id: 终端节点关联的终端节点服务,若是使用dns云服务创建终端节点该参数不用传
        :param vpc_id: 虚拟私有云 id
        :param whitelist: 白名单 最大支持20个,ipv4Cidr格式 注意:此参数为数组
        :param whitelist6: ipv6白名单 注意:此参数为数组
        :param subnet_id: 子网id
        :param cycle_type: 收费类型：只能填写 on_demand
        :param whitelist_flag: 白名单开关 1.开启 0.关闭，默认1
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param ip: ipv4 vpc address
        :param i_p6: ipv6 vpc address
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈，默认0
        :param enable_dns: 是否开启 dns,默认不开启
        :param endpoint_service_type: 终端服务类型 默认0需要必传endpointServiceID，为1时不传。(930及以上版本支持)
        :param project_id: 企业项目ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.endpoint_name = endpoint_name
        self.endpoint_service_id = endpoint_service_id
        self.vpc_id = vpc_id
        self.whitelist = whitelist
        self.whitelist6 = whitelist6
        self.subnet_id = subnet_id
        self.cycle_type = cycle_type
        self.whitelist_flag = whitelist_flag
        self.description = description
        self.ip = ip
        self.i_p6 = i_p6
        self.ip_version = ip_version
        self.enable_dns = enable_dns
        self.endpoint_service_type = endpoint_service_type
        self.project_id = project_id

    def set_whitelist(self, whitelist):
        """
        :param whitelist: 白名单 最大支持20个,ipv4Cidr格式
        """
        self.whitelist = whitelist

    def set_whitelist6(self, whitelist6):
        """
        :param whitelist6: ipv6白名单
        """
        self.whitelist6 = whitelist6

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_ip(self, ip):
        """
        :param ip: ipv4 vpc address
        """
        self.ip = ip

    def set_i_p6(self, i_p6):
        """
        :param i_p6: ipv6 vpc address
        """
        self.i_p6 = i_p6

    def set_ip_version(self, ip_version):
        """
        :param ip_version: 0:ipv4, 1:ipv6（暂不支持）, 2:双栈，默认0
        """
        self.ip_version = ip_version

    def set_enable_dns(self, enable_dns):
        """
        :param enable_dns: 是否开启 dns,默认不开启
        """
        self.enable_dns = enable_dns

    def set_endpoint_service_type(self, endpoint_service_type):
        """
        :param endpoint_service_type: 终端服务类型 默认0需要必传endpointServiceID，为1时不传。(930及以上版本支持)
        """
        self.endpoint_service_type = endpoint_service_type

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_name is None:
            raise Exception("endpoint_name can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.whitelist_flag is None:
            raise Exception("whitelist_flag can not None")

