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


class CreateListenerRequest(CTYunRequest):
    """
    创建监听器   
       
    #### 备注   
    * 3.0/acs已支持创建，但是不支持设置限速、全端口监听等高级配置。使用说明：foward类型不需要传defaultAction配合创建后端服务组使用，redirect类型使用defaultAction
    """

    def __init__(self, request_param):
        super(CreateListenerRequest, self).__init__("/v4/elb/create-listener", "POST", "ctelb", "application/json")
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
        if self.parameters.load_balancer_id is not None:
            body_param["loadBalancerID"] = self.parameters.load_balancer_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.protocol_port is not None:
            body_param["protocolPort"] = self.parameters.protocol_port
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.default_action is not None:
            if type(self.parameters.default_action) is dict:
                default_action_dict_value = self.parameters.default_action
            else:
                default_action_dict_value = self.parameters.default_action.get_dic()
            body_param["defaultAction"] = default_action_dict_value
        if self.parameters.certificate_id is not None:
            body_param["certificateID"] = self.parameters.certificate_id
        if self.parameters.client_certificate_id is not None:
            body_param["clientCertificateID"] = self.parameters.client_certificate_id
        if self.parameters.ca_enabled is not None:
            body_param["caEnabled"] = self.parameters.ca_enabled
        if self.parameters.access_control_id is not None:
            body_param["accessControlID"] = self.parameters.access_control_id
        if self.parameters.access_control_type is not None:
            body_param["accessControlType"] = self.parameters.access_control_type
        if self.parameters.forwarded_for_enabled is not None:
            body_param["forwardedForEnabled"] = self.parameters.forwarded_for_enabled
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.limit_enabled is not None:
            body_param["limitEnabled"] = self.parameters.limit_enabled
        if self.parameters.listener_cps_qps is not None:
            body_param["listenerCpsQps"] = self.parameters.listener_cps_qps
        if self.parameters.nat_mode is not None:
            body_param["natMode"] = self.parameters.nat_mode
        if self.parameters.all_port_forward is not None:
            body_param["allPortForward"] = self.parameters.all_port_forward
        if self.parameters.start_port is not None:
            body_param["startPort"] = self.parameters.start_port
        if self.parameters.end_port is not None:
            body_param["endPort"] = self.parameters.end_port
        if self.parameters.forwarded_proto_enabled is not None:
            body_param["forwardedProtoEnabled"] = self.parameters.forwarded_proto_enabled
        if self.parameters.forwarded_port_enabled is not None:
            body_param["forwardedPortEnabled"] = self.parameters.forwarded_port_enabled
        if self.parameters.http2_enabled is not None:
            body_param["http2Enabled"] = self.parameters.http2_enabled
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


class DefaultAction(object):

    def __init__(self, type, forward_config=None, redirect_listener_id=None):
        """
        :param type: 默认规则动作类型。取值范围：forward、redirect
        :param forward_config: 转发配置，当type为forward时，此字段必填
        :param redirect_listener_id: 重定向监听器ID，当type为redirect时，此字段必填
        """
        self.type = type
        self.forward_config = forward_config
        self.redirect_listener_id = redirect_listener_id
        self.check_param()

    def set_forward_config(self, forward_config):
        """
        :param forward_config: 转发配置，当type为forward时，此字段必填
        """
        self.forward_config = forward_config

    def set_redirect_listener_id(self, redirect_listener_id):
        """
        :param redirect_listener_id: 重定向监听器ID，当type为redirect时，此字段必填
        """
        self.redirect_listener_id = redirect_listener_id

    def get_dic(self):
        obj_dict = dict()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.forward_config is not None:
            if type(self.forward_config) is dict:
                obj_dict["forwardConfig"] = self.forward_config
            else:
                obj_dict["forwardConfig"] = self.forward_config.get_dic()
        if self.redirect_listener_id is not None:
            obj_dict["redirectListenerID"] = self.redirect_listener_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class ForwardConfig(object):

    def __init__(self, target_groups=None):
        """
        :param target_groups: 后端服务组
        """
        self.target_groups = target_groups

    def set_target_groups(self, target_groups):
        """
        :param target_groups: 后端服务组
        """
        self.target_groups = target_groups

    def get_dic(self):
        obj_dict = dict()
        if self.target_groups is not None:
            target_groups_array = []
            for item in self.target_groups:
                if type(item) is dict:
                    target_groups_array.append(item)
                else:
                    target_groups_array.append(item.get_dic())
            obj_dict["targetGroups"] = target_groups_array
        return obj_dict


class TargetGroup(object):

    def __init__(self, target_group_id=None, weight=None):
        """
        :param target_group_id: 后端服务组ID
        :param weight: 后端主机权重，取值范围：1-256。默认为100
        """
        self.target_group_id = target_group_id
        self.weight = weight

    def set_target_group_id(self, target_group_id):
        """
        :param target_group_id: 后端服务组ID
        """
        self.target_group_id = target_group_id

    def set_weight(self, weight):
        """
        :param weight: 后端主机权重，取值范围：1-256。默认为100
        """
        self.weight = weight

    def get_dic(self):
        obj_dict = dict()
        if self.target_group_id is not None:
            obj_dict["targetGroupID"] = self.target_group_id
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        return obj_dict


class CreateListenerRequestParam(object):

    def __init__(self, region_id, load_balancer_id, name, protocol, description=None, protocol_port=None, default_action=None, certificate_id=None, client_certificate_id=None, ca_enabled=None, access_control_id=None, access_control_type=None, forwarded_for_enabled=None, client_token=None, limit_enabled=None, listener_cps_qps=None, nat_mode=None, all_port_forward=None, start_port=None, end_port=None, forwarded_proto_enabled=None, forwarded_port_enabled=None, http2_enabled=None):
        """
        :param region_id: 资源池ID
        :param load_balancer_id: 负载均衡实例ID 
        :param name: 监听器名称，英文字母、中文、特殊符号_(下划线) -(中划线) /(斜杠) 进行命名 // 不支持使用特殊符号、数字作为命名开头，不支持特殊符号作为命名结尾 // 命名长度为2-32位
        :param description: 描述	，长度为0～100字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，
        :param protocol_port: 负载均衡实例监听端口。取值：1-65535，开启全端口监听后无效为0，否则参数必填（全端口监听仅支持4.0）
        :param protocol: 监听协议。取值范围：TCP、UDP、HTTP、HTTPS（监听器协议为HTTPS时，certificateID为必传参数）、IPRAW(不支持allPortForward、listenerCpsQps、limitEnabled、accessControlType、caEnabled相关特性且同负载均衡下仅支持创建一个该协议监听器)
        :param default_action: 默认规则动作，4.0必传，3.0/acs忽略参数
        :param certificate_id: 证书ID。当protocol为HTTPS时,此参数必选
        :param client_certificate_id: 双向认证的证书ID
        :param ca_enabled: 是否开启双向认证。false（不开启）、true（开启）（caEnbaled为true时，需要传clientCertificateID，且certificateID证书类型为Server类型，clientCertificateID证书类型为Ca类型）
        :param access_control_id: 访问控制ID
        :param access_control_type: 访问控制类型。取值范围：Close（未启用）、White（白名单）、Black（黑名单）
        :param forwarded_for_enabled: x forward for功能。false（未开启）、true（开启）
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param limit_enabled: 监听器限速开关 0 关闭， 1开启 默认关闭
        :param listener_cps_qps: 限制的连接数或qps 取值范围 [10-500000]，开启限速时该参数必传（关闭时忽略该参数）
        :param nat_mode: 4层，NAT模式，默认0，0为FULLNAT，1为DNAT（客户端地址保持）
        :param all_port_forward: 全端口监听 0-不开启 1-开启
        :param start_port: 开启全端口监听使用，起始端口，1-65535
        :param end_port: 开启全端口监听使用，结束端口，1-65535
        :param forwarded_proto_enabled: x forworded Proto功能：0-未开启，1-开启，默认关闭
        :param forwarded_port_enabled: x forworded Port功能：0-未开启，1-开启，默认关闭
        :param http2_enabled: 开启http2.0，仅支持https类型，0未开启，1开启,默认关闭
        """
        self.region_id = region_id
        self.load_balancer_id = load_balancer_id
        self.name = name
        self.description = description
        self.protocol_port = protocol_port
        self.protocol = protocol
        self.default_action = default_action
        self.certificate_id = certificate_id
        self.client_certificate_id = client_certificate_id
        self.ca_enabled = ca_enabled
        self.access_control_id = access_control_id
        self.access_control_type = access_control_type
        self.forwarded_for_enabled = forwarded_for_enabled
        self.client_token = client_token
        self.limit_enabled = limit_enabled
        self.listener_cps_qps = listener_cps_qps
        self.nat_mode = nat_mode
        self.all_port_forward = all_port_forward
        self.start_port = start_port
        self.end_port = end_port
        self.forwarded_proto_enabled = forwarded_proto_enabled
        self.forwarded_port_enabled = forwarded_port_enabled
        self.http2_enabled = http2_enabled

    def set_description(self, description):
        """
        :param description: 描述	，长度为0～100字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，
        """
        self.description = description

    def set_protocol_port(self, protocol_port):
        """
        :param protocol_port: 负载均衡实例监听端口。取值：1-65535，开启全端口监听后无效为0，否则参数必填（全端口监听仅支持4.0）
        """
        self.protocol_port = protocol_port

    def set_default_action(self, default_action):
        """
        :param default_action: 默认规则动作，4.0必传，3.0/acs忽略参数
        """
        self.default_action = default_action

    def set_certificate_id(self, certificate_id):
        """
        :param certificate_id: 证书ID。当protocol为HTTPS时,此参数必选
        """
        self.certificate_id = certificate_id

    def set_client_certificate_id(self, client_certificate_id):
        """
        :param client_certificate_id: 双向认证的证书ID
        """
        self.client_certificate_id = client_certificate_id

    def set_ca_enabled(self, ca_enabled):
        """
        :param ca_enabled: 是否开启双向认证。false（不开启）、true（开启）（caEnbaled为true时，需要传clientCertificateID，且certificateID证书类型为Server类型，clientCertificateID证书类型为Ca类型）
        """
        self.ca_enabled = ca_enabled

    def set_access_control_id(self, access_control_id):
        """
        :param access_control_id: 访问控制ID
        """
        self.access_control_id = access_control_id

    def set_access_control_type(self, access_control_type):
        """
        :param access_control_type: 访问控制类型。取值范围：Close（未启用）、White（白名单）、Black（黑名单）
        """
        self.access_control_type = access_control_type

    def set_forwarded_for_enabled(self, forwarded_for_enabled):
        """
        :param forwarded_for_enabled: x forward for功能。false（未开启）、true（开启）
        """
        self.forwarded_for_enabled = forwarded_for_enabled

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_limit_enabled(self, limit_enabled):
        """
        :param limit_enabled: 监听器限速开关 0 关闭， 1开启 默认关闭
        """
        self.limit_enabled = limit_enabled

    def set_listener_cps_qps(self, listener_cps_qps):
        """
        :param listener_cps_qps: 限制的连接数或qps 取值范围 [10-500000]，开启限速时该参数必传（关闭时忽略该参数）
        """
        self.listener_cps_qps = listener_cps_qps

    def set_nat_mode(self, nat_mode):
        """
        :param nat_mode: 4层，NAT模式，默认0，0为FULLNAT，1为DNAT（客户端地址保持）
        """
        self.nat_mode = nat_mode

    def set_all_port_forward(self, all_port_forward):
        """
        :param all_port_forward: 全端口监听 0-不开启 1-开启
        """
        self.all_port_forward = all_port_forward

    def set_start_port(self, start_port):
        """
        :param start_port: 开启全端口监听使用，起始端口，1-65535
        """
        self.start_port = start_port

    def set_end_port(self, end_port):
        """
        :param end_port: 开启全端口监听使用，结束端口，1-65535
        """
        self.end_port = end_port

    def set_forwarded_proto_enabled(self, forwarded_proto_enabled):
        """
        :param forwarded_proto_enabled: x forworded Proto功能：0-未开启，1-开启，默认关闭
        """
        self.forwarded_proto_enabled = forwarded_proto_enabled

    def set_forwarded_port_enabled(self, forwarded_port_enabled):
        """
        :param forwarded_port_enabled: x forworded Port功能：0-未开启，1-开启，默认关闭
        """
        self.forwarded_port_enabled = forwarded_port_enabled

    def set_http2_enabled(self, http2_enabled):
        """
        :param http2_enabled: 开启http2.0，仅支持https类型，0未开启，1开启,默认关闭
        """
        self.http2_enabled = http2_enabled

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.load_balancer_id is None:
            raise Exception("load_balancer_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")

