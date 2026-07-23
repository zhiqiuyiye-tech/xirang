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


class CreateSecurityGroupInRulesOpenapiNewRequest(CTYunRequest):
    """
    创建安全组入向规则。公有云入参缺clientToken字段，暂不修改
    """

    def __init__(self, request_param):
        super(CreateSecurityGroupInRulesOpenapiNewRequest, self).__init__("/v4/vpc/create-security-group-ingress-new", "POST", "ctvpc", "application/json")
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
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.security_group_rules is not None:
            security_group_rules = []
            if isinstance(self.parameters.security_group_rules, list):
                for item in self.parameters.security_group_rules:
                    if type(item) is dict:
                        security_group_rules.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        security_group_rules.append(item_dict_value)
            else:
                security_group_rules.append(self.parameters.security_group_rules.get_dic())
            body_param["securityGroupRules"] = security_group_rules
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


class SecurityGroupRule(object):

    def __init__(self, direction, ethertype, action, protocol, priority=None, dest_cidr_ip=None, range=None, description=None, remote_type=None, remote_security_group_id=None):
        """
        :param direction: 入方向-ingress
        :param ethertype: IP类型:IPv4、IPv6;兼容大小写
        :param priority: 优先级:1~100，取值越小优先级越大，默认值为1
        :param action: 拒绝策略:允许-accept 拒绝-drop
        :param dest_cidr_ip: 远端地址:0.0.0.0/0，remote=0时必填
        :param range: 安全组开放的传输层协议相关的源端端口范围
        :param protocol: 协议: ANY、TCP、UDP、ICMP
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$% ^&()_-+= <>?:"{},./;'[]·~！@#￥*%……&（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param remote_type: remote 类型，0 表示使用 cidr，1 表示使用远端安全组，默认为 0
        :param remote_security_group_id: 远端安全组 id
        """
        self.direction = direction
        self.ethertype = ethertype
        self.priority = priority
        self.action = action
        self.dest_cidr_ip = dest_cidr_ip
        self.range = range
        self.protocol = protocol
        self.description = description
        self.remote_type = remote_type
        self.remote_security_group_id = remote_security_group_id
        self.check_param()

    def set_priority(self, priority):
        """
        :param priority: 优先级:1~100，取值越小优先级越大，默认值为1
        """
        self.priority = priority

    def set_dest_cidr_ip(self, dest_cidr_ip):
        """
        :param dest_cidr_ip: 远端地址:0.0.0.0/0，remote=0时必填
        """
        self.dest_cidr_ip = dest_cidr_ip

    def set_range(self, range):
        """
        :param range: 安全组开放的传输层协议相关的源端端口范围
        """
        self.range = range

    def set_description(self, description):
        """
        :param description: 支持拉丁字母、中文、数字, 特殊字符：\\~!@#$% ^&()_-+= <>?:"{},./;'[]·~！@#￥*%……&（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_remote_type(self, remote_type):
        """
        :param remote_type: remote 类型，0 表示使用 cidr，1 表示使用远端安全组，默认为 0
        """
        self.remote_type = remote_type

    def set_remote_security_group_id(self, remote_security_group_id):
        """
        :param remote_security_group_id: 远端安全组 id
        """
        self.remote_security_group_id = remote_security_group_id

    def get_dic(self):
        obj_dict = dict()
        if self.direction is not None:
            obj_dict["direction"] = self.direction
        if self.ethertype is not None:
            obj_dict["ethertype"] = self.ethertype
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.action is not None:
            obj_dict["action"] = self.action
        if self.dest_cidr_ip is not None:
            obj_dict["destCidrIp"] = self.dest_cidr_ip
        if self.range is not None:
            obj_dict["range"] = self.range
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.description is not None:
            obj_dict["description"] = self.description
        if self.remote_type is not None:
            obj_dict["remoteType"] = self.remote_type
        if self.remote_security_group_id is not None:
            obj_dict["remoteSecurityGroupID"] = self.remote_security_group_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.direction is None:
            raise Exception("direction can not None")
        if self.ethertype is None:
            raise Exception("ethertype can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")


class CreateSecurityGroupInRulesOpenapiNewRequestParam(object):

    def __init__(self, region_id, security_group_id, security_group_rules, client_token=None):
        """
        :param region_id: 资源池ID
        :param security_group_id: 安全组ID
        :param client_token: 可传但是不进行校验, 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param security_group_rules: 规则信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.security_group_id = security_group_id
        self.client_token = client_token
        self.security_group_rules = security_group_rules

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验, 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.security_group_id is None:
            raise Exception("security_group_id can not None")
        if self.security_group_rules is None:
            raise Exception("security_group_rules can not None")

