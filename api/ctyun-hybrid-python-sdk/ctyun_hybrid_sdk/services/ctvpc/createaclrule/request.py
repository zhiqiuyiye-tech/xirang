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


class CreateAclRuleRequest(CTYunRequest):
    """
    创建aclrules：支持批量创建   
    1.15版本支持新返回格式   
    如果批量有成功也有失败的，返回当前acl下所有的acl规则id   
    如果创建都不成功，则返回空对象
    """

    def __init__(self, request_param):
        super(CreateAclRuleRequest, self).__init__("/v4/acl-rule/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.acl_id is not None:
            body_param["aclID"] = self.parameters.acl_id
        if self.parameters.rules is not None:
            rules = []
            if isinstance(self.parameters.rules, list):
                for item in self.parameters.rules:
                    if type(item) is dict:
                        rules.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        rules.append(item_dict_value)
            else:
                rules.append(self.parameters.rules.get_dic())
            body_param["rules"] = rules
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


class Rule(object):

    def __init__(self, protocol, source_ip_address, destination_ip_address, priority, ip_version, direction, enabled, action, source_port=None, destination_port=None, description=None):
        """
        :param protocol: all, icmp, tcp, udp, icmp6
        :param source_ip_address: 源地址
        :param source_port: 开始和结束port以:隔开（UDP和TCP协议时，端口号必填，其他协议勿填）
        :param destination_ip_address: 目的地址
        :param destination_port: 开始和结束port以:隔开（UDP和TCP协议时，端口号必填，其他协议勿填）
        :param priority: 优先级 1-32767
        :param ip_version: ipv4,  ipv6 (ICMP6只支持IPV6）
        :param direction: 类型,ingress, egress
        :param description: 描述 长度为0-50字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        :param enabled: disable, enable 状态：禁用/启用
        :param action: accept, drop 授权策略：允许/拒绝
        """
        self.protocol = protocol
        self.source_ip_address = source_ip_address
        self.source_port = source_port
        self.destination_ip_address = destination_ip_address
        self.destination_port = destination_port
        self.priority = priority
        self.ip_version = ip_version
        self.direction = direction
        self.description = description
        self.enabled = enabled
        self.action = action
        self.check_param()

    def set_source_port(self, source_port):
        """
        :param source_port: 开始和结束port以:隔开（UDP和TCP协议时，端口号必填，其他协议勿填）
        """
        self.source_port = source_port

    def set_destination_port(self, destination_port):
        """
        :param destination_port: 开始和结束port以:隔开（UDP和TCP协议时，端口号必填，其他协议勿填）
        """
        self.destination_port = destination_port

    def set_description(self, description):
        """
        :param description: 描述 长度为0-50字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        """
        self.description = description

    def get_dic(self):
        obj_dict = dict()
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.source_ip_address is not None:
            obj_dict["sourceIpAddress"] = self.source_ip_address
        if self.source_port is not None:
            obj_dict["sourcePort"] = self.source_port
        if self.destination_ip_address is not None:
            obj_dict["destinationIpAddress"] = self.destination_ip_address
        if self.destination_port is not None:
            obj_dict["destinationPort"] = self.destination_port
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.ip_version is not None:
            obj_dict["ipVersion"] = self.ip_version
        if self.direction is not None:
            obj_dict["direction"] = self.direction
        if self.description is not None:
            obj_dict["description"] = self.description
        if self.enabled is not None:
            obj_dict["enabled"] = self.enabled
        if self.action is not None:
            obj_dict["action"] = self.action
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.source_ip_address is None:
            raise Exception("source_ip_address can not None")
        if self.destination_ip_address is None:
            raise Exception("destination_ip_address can not None")
        if self.priority is None:
            raise Exception("priority can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.direction is None:
            raise Exception("direction can not None")
        if self.enabled is None:
            raise Exception("enabled can not None")
        if self.action is None:
            raise Exception("action can not None")


class CreateAclRuleRequestParam(object):

    def __init__(self, region_id, acl_id, rules, ):
        """
        :param region_id: 资源池ID
        :param acl_id: ACL ID
        :param rules: rule 规则数组 注意:此参数为数组
        """
        self.region_id = region_id
        self.acl_id = acl_id
        self.rules = rules

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.acl_id is None:
            raise Exception("acl_id can not None")
        if self.rules is None:
            raise Exception("rules can not None")

