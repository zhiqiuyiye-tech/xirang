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


class PortCreateRequest(CTYunRequest):
    """
    创建弹性网卡
    """

    def __init__(self, request_param):
        super(PortCreateRequest, self).__init__("/v4/ecs/ports/create", "POST", "ctecs", "application/json")
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
        if self.parameters.primary_private_ip is not None:
            body_param["primaryPrivateIp"] = self.parameters.primary_private_ip
        if self.parameters.ipv6_addresses is not None:
            body_param["ipv6Addresses"] = self.parameters.ipv6_addresses
        if self.parameters.secondary_private_ip_count is not None:
            body_param["secondaryPrivateIpCount"] = self.parameters.secondary_private_ip_count
        if self.parameters.secondary_private_ips is not None:
            body_param["secondaryPrivateIps"] = self.parameters.secondary_private_ips
        if self.parameters.security_group_ids is not None:
            body_param["securityGroupIds"] = self.parameters.security_group_ids
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class PortCreateRequestParam(object):

    def __init__(self, region_id, subnet_id, name=None, description=None, primary_private_ip=None, ipv6_addresses=None, secondary_private_ip_count=None, secondary_private_ips=None, security_group_ids=None, client_token=None):
        """
        :param region_id: 资源池id
        :param subnet_id: 子网id
        :param name: 网卡名称，满足以下规则：支持拉丁字母、中文、数字，下划线，连字符，中文/英文字母开头，不能以http:/https:开头，长度2-32
        :param description: 网卡的描述，满足以下规则：支持拉丁字母、中文、数字, 特殊字符：*~!@#$%^&*()_-+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+={}\\|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param primary_private_ip: 弹性网卡的主私有IP地址
        :param ipv6_addresses: Ipv6地址，多个ip地址用逗号隔开 注意:此参数为数组
        :param secondary_private_ip_count: 第二个IP数量，不能和secondaryPrivateIps同时指定,建议不超过10个
        :param secondary_private_ips: 第二个IPs ，ip address为subnet内空闲ip，多个ip地址用逗号隔开；辅助私网IP地址，不能和secondaryPrivateIpCount同时指定，建议不超过10个 注意:此参数为数组
        :param security_group_ids: 安全组ID，多个id用逗号隔开。为空时使用vpc默认安全组 注意:此参数为数组
        :param client_token: 可传但是不进行校验，公有云需要暂无功能（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.primary_private_ip = primary_private_ip
        self.ipv6_addresses = ipv6_addresses
        self.secondary_private_ip_count = secondary_private_ip_count
        self.secondary_private_ips = secondary_private_ips
        self.security_group_ids = security_group_ids
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 网卡名称，满足以下规则：支持拉丁字母、中文、数字，下划线，连字符，中文/英文字母开头，不能以http:/https:开头，长度2-32
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 网卡的描述，满足以下规则：支持拉丁字母、中文、数字, 特殊字符：*~!@#$%^&*()_-+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+={}\\|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_primary_private_ip(self, primary_private_ip):
        """
        :param primary_private_ip: 弹性网卡的主私有IP地址
        """
        self.primary_private_ip = primary_private_ip

    def set_ipv6_addresses(self, ipv6_addresses):
        """
        :param ipv6_addresses: Ipv6地址，多个ip地址用逗号隔开
        """
        self.ipv6_addresses = ipv6_addresses

    def set_secondary_private_ip_count(self, secondary_private_ip_count):
        """
        :param secondary_private_ip_count: 第二个IP数量，不能和secondaryPrivateIps同时指定,建议不超过10个
        """
        self.secondary_private_ip_count = secondary_private_ip_count

    def set_secondary_private_ips(self, secondary_private_ips):
        """
        :param secondary_private_ips: 第二个IPs ，ip address为subnet内空闲ip，多个ip地址用逗号隔开；辅助私网IP地址，不能和secondaryPrivateIpCount同时指定，建议不超过10个
        """
        self.secondary_private_ips = secondary_private_ips

    def set_security_group_ids(self, security_group_ids):
        """
        :param security_group_ids: 安全组ID，多个id用逗号隔开。为空时使用vpc默认安全组
        """
        self.security_group_ids = security_group_ids

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验，公有云需要暂无功能（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

