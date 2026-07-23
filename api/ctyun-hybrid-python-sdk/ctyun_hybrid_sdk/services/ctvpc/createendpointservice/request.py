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


class CreateEndpointServiceRequest(CTYunRequest):
    """
    创建终端节点服务.当type为反向reverse时，自动创建不指定的中转ip。中转ip列表可产看详情信息。
    """

    def __init__(self, request_param):
        super(CreateEndpointServiceRequest, self).__init__("/v4/vpce/create-endpoint-service", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.instance_type is not None:
            body_param["instanceType"] = self.parameters.instance_type
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.instance_i_d6 is not None:
            body_param["instanceID6"] = self.parameters.instance_i_d6
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.underlay_i_p6 is not None:
            body_param["underlayIP6"] = self.parameters.underlay_i_p6
        if self.parameters.underlay_ip is not None:
            body_param["underlayIP"] = self.parameters.underlay_ip
        if self.parameters.auto_connection is not None:
            body_param["autoConnection"] = self.parameters.auto_connection
        if self.parameters.dns_name is not None:
            body_param["dnsName"] = self.parameters.dns_name
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
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


class Rule(object):

    def __init__(self, protocol, server_port, endpoint_port, ):
        """
        :param protocol: 协议，TCP:TCP协议,UDP:UDP协议
        :param server_port: 服务端口(用于创建backend传入)(1-65535)
        :param endpoint_port: 节点端口(用于创建rule传入)(1-65535)
        """
        self.protocol = protocol
        self.server_port = server_port
        self.endpoint_port = endpoint_port
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.server_port is not None:
            obj_dict["serverPort"] = self.server_port
        if self.endpoint_port is not None:
            obj_dict["endpointPort"] = self.endpoint_port
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.server_port is None:
            raise Exception("server_port can not None")
        if self.endpoint_port is None:
            raise Exception("endpoint_port can not None")


class CreateEndpointServiceRequestParam(object):

    def __init__(self, region_id, name, vpc_id, auto_connection, client_token=None, description=None, type=None, instance_type=None, instance_id=None, instance_i_d6=None, subnet_id=None, underlay_i_p6=None, underlay_ip=None, dns_name=None, ip_version=None, rules=None, project_id=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池 ID
        :param name: 终端节点服务名称，长度为2-32字符，支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param vpc_id: 所属的专有网络id
        :param type: 接口还是反向，interface:接口，reverse:反向,默认interface
        :param instance_type: 服务后端实例类型，vm:虚机类型,bm:物理机,vip:vip类型,lb:负载均衡类型,underlay:内网ip类型, 当 type 为 interface 时，必填
        :param instance_id: 服务后端实例id,若服务后端实例类型为内网ip类型时，该字段为内网ip的值。 当 type 为 interface 时，必填
        :param instance_i_d6:  后端服务为vip时，v6的vip id
        :param subnet_id: 服务后端子网id,若instanceType为非underlay类型，此参数必传
        :param underlay_i_p6: instance_type为天翼云内网资源时，v6的underlay ip
        :param underlay_ip: instance_type为天翼云内网资源时，v4的underlay ip
        :param auto_connection: 是否自动连接，true 表示自动链接，false 表示非自动链接
        :param dns_name: dns 名字，仅支持有权限的用户设置 。包含*   点 .   中划线-  大小写字母，数字，最长253。*只能是开头，中划线不能是开头结尾，每段最长63。总长度最大253
        :param ip_version: ip地址类型：0-ipv4，2-双栈
        :param rules: 节点服务规则 注意:此参数为数组
        :param project_id: 企业项目ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.name = name
        self.description = description
        self.vpc_id = vpc_id
        self.type = type
        self.instance_type = instance_type
        self.instance_id = instance_id
        self.instance_i_d6 = instance_i_d6
        self.subnet_id = subnet_id
        self.underlay_i_p6 = underlay_i_p6
        self.underlay_ip = underlay_ip
        self.auto_connection = auto_connection
        self.dns_name = dns_name
        self.ip_version = ip_version
        self.rules = rules
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_type(self, type):
        """
        :param type: 接口还是反向，interface:接口，reverse:反向,默认interface
        """
        self.type = type

    def set_instance_type(self, instance_type):
        """
        :param instance_type: 服务后端实例类型，vm:虚机类型,bm:物理机,vip:vip类型,lb:负载均衡类型,underlay:内网ip类型, 当 type 为 interface 时，必填
        """
        self.instance_type = instance_type

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 服务后端实例id,若服务后端实例类型为内网ip类型时，该字段为内网ip的值。 当 type 为 interface 时，必填
        """
        self.instance_id = instance_id

    def set_instance_i_d6(self, instance_i_d6):
        """
        :param instance_i_d6:  后端服务为vip时，v6的vip id
        """
        self.instance_i_d6 = instance_i_d6

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 服务后端子网id,若instanceType为非underlay类型，此参数必传
        """
        self.subnet_id = subnet_id

    def set_underlay_i_p6(self, underlay_i_p6):
        """
        :param underlay_i_p6: instance_type为天翼云内网资源时，v6的underlay ip
        """
        self.underlay_i_p6 = underlay_i_p6

    def set_underlay_ip(self, underlay_ip):
        """
        :param underlay_ip: instance_type为天翼云内网资源时，v4的underlay ip
        """
        self.underlay_ip = underlay_ip

    def set_dns_name(self, dns_name):
        """
        :param dns_name: dns 名字，仅支持有权限的用户设置 。包含*   点 .   中划线-  大小写字母，数字，最长253。*只能是开头，中划线不能是开头结尾，每段最长63。总长度最大253
        """
        self.dns_name = dns_name

    def set_ip_version(self, ip_version):
        """
        :param ip_version: ip地址类型：0-ipv4，2-双栈
        """
        self.ip_version = ip_version

    def set_rules(self, rules):
        """
        :param rules: 节点服务规则
        """
        self.rules = rules

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
        if self.auto_connection is None:
            raise Exception("auto_connection can not None")

