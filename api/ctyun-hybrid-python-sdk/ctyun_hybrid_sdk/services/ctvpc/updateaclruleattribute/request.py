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


class UpdateAclRuleAttributeRequest(CTYunRequest):
    """
    只有用户创建的ACL规则才能修改，ACL默认创建的ACL规则不允许修改
    """

    def __init__(self, request_param):
        super(UpdateAclRuleAttributeRequest, self).__init__("/v4/acl-rule/update", "POST", "ctvpc", "application/json")
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

    def __init__(self, acl_rule_id, priority, protocol, ip_version, direction, source_ip_address, destination_ip_address, action, enabled, destination_port=None, source_port=None):
        """
        :param acl_rule_id: ACL规则ID
        :param priority: 优先级 1-32767
        :param protocol: all, icmp, tcp, udp, icmp6
        :param ip_version: ipv4,  ipv6
        :param direction: 类型,ingress, egress
        :param destination_port: 目标地址端口号，用：分割（protocol为tcp和udp时必传，其他协议该参数不传）
        :param source_port: 源地址端口号，用：分割（protocol为tcp和udp时必传，其他协议该参数不传）
        :param source_ip_address: 源地址
        :param destination_ip_address: 目的地址
        :param action: accept-允许, drop-拒绝（公有云必选）
        :param enabled: disable-禁用, enable-启用（公有云必选）
        """
        self.acl_rule_id = acl_rule_id
        self.priority = priority
        self.protocol = protocol
        self.ip_version = ip_version
        self.direction = direction
        self.destination_port = destination_port
        self.source_port = source_port
        self.source_ip_address = source_ip_address
        self.destination_ip_address = destination_ip_address
        self.action = action
        self.enabled = enabled
        self.check_param()

    def set_destination_port(self, destination_port):
        """
        :param destination_port: 目标地址端口号，用：分割（protocol为tcp和udp时必传，其他协议该参数不传）
        """
        self.destination_port = destination_port

    def set_source_port(self, source_port):
        """
        :param source_port: 源地址端口号，用：分割（protocol为tcp和udp时必传，其他协议该参数不传）
        """
        self.source_port = source_port

    def get_dic(self):
        obj_dict = dict()
        if self.acl_rule_id is not None:
            obj_dict["aclRuleID"] = self.acl_rule_id
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.ip_version is not None:
            obj_dict["ipVersion"] = self.ip_version
        if self.direction is not None:
            obj_dict["direction"] = self.direction
        if self.destination_port is not None:
            obj_dict["destinationPort"] = self.destination_port
        if self.source_port is not None:
            obj_dict["sourcePort"] = self.source_port
        if self.source_ip_address is not None:
            obj_dict["sourceIpAddress"] = self.source_ip_address
        if self.destination_ip_address is not None:
            obj_dict["destinationIpAddress"] = self.destination_ip_address
        if self.action is not None:
            obj_dict["action"] = self.action
        if self.enabled is not None:
            obj_dict["enabled"] = self.enabled
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.acl_rule_id is None:
            raise Exception("acl_rule_id can not None")
        if self.priority is None:
            raise Exception("priority can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")
        if self.direction is None:
            raise Exception("direction can not None")
        if self.source_ip_address is None:
            raise Exception("source_ip_address can not None")
        if self.destination_ip_address is None:
            raise Exception("destination_ip_address can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.enabled is None:
            raise Exception("enabled can not None")


class UpdateAclRuleAttributeRequestParam(object):

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

