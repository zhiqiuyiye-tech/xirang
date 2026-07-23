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


class CreateTargetGroupRequest(CTYunRequest):
    """
    创建后端服务组   
       
    #### 备注   
    * 3.0 已支持，需先创建监听器再创建后端服务组，不支持全端口监听
    """

    def __init__(self, request_param):
        super(CreateTargetGroupRequest, self).__init__("/v4/elb/create-target-group", "POST", "ctelb", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.algorithm is not None:
            body_param["algorithm"] = self.parameters.algorithm
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.health_check_id is not None:
            body_param["healthCheckID"] = self.parameters.health_check_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.session_sticky is not None:
            if type(self.parameters.session_sticky) is dict:
                session_sticky_dict_value = self.parameters.session_sticky
            else:
                session_sticky_dict_value = self.parameters.session_sticky.get_dic()
            body_param["sessionSticky"] = session_sticky_dict_value
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.pool_protocol is not None:
            body_param["poolProtocol"] = self.parameters.pool_protocol
        if self.parameters.all_port_forward is not None:
            body_param["allPortForward"] = self.parameters.all_port_forward
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.listener_id is not None:
            body_param["listenerID"] = self.parameters.listener_id
        if self.parameters.connection_drain_config is not None:
            if type(self.parameters.connection_drain_config) is dict:
                connection_drain_config_dict_value = self.parameters.connection_drain_config
            else:
                connection_drain_config_dict_value = self.parameters.connection_drain_config.get_dic()
            body_param["connectionDrainConfig"] = connection_drain_config_dict_value
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


class SessionSticky(object):

    def __init__(self, session_sticky_mode, source_ip_timeout=None, rewrite_cookie_name=None, cookie_expire=None):
        """
        :param source_ip_timeout: 源IP会话保持超时时间。SOURCE_IP模式必填
        :param rewrite_cookie_name: cookie重写名称，REWRITE模式必填
        :param session_sticky_mode: 会话保持模式，支持取值：CLOSE（关闭）、INSERT（插入）、REWRITE（重写）、SOURCE_IP（源IP）（SOURCE_IP只支持wrr和lc;INSERT/REWRITE只支持wrr，CLOSE支持wrr,lc,sh）
        :param cookie_expire: cookie过期时间。INSERT模式必填
        """
        self.source_ip_timeout = source_ip_timeout
        self.rewrite_cookie_name = rewrite_cookie_name
        self.session_sticky_mode = session_sticky_mode
        self.cookie_expire = cookie_expire
        self.check_param()

    def set_source_ip_timeout(self, source_ip_timeout):
        """
        :param source_ip_timeout: 源IP会话保持超时时间。SOURCE_IP模式必填
        """
        self.source_ip_timeout = source_ip_timeout

    def set_rewrite_cookie_name(self, rewrite_cookie_name):
        """
        :param rewrite_cookie_name: cookie重写名称，REWRITE模式必填
        """
        self.rewrite_cookie_name = rewrite_cookie_name

    def set_cookie_expire(self, cookie_expire):
        """
        :param cookie_expire: cookie过期时间。INSERT模式必填
        """
        self.cookie_expire = cookie_expire

    def get_dic(self):
        obj_dict = dict()
        if self.source_ip_timeout is not None:
            obj_dict["sourceIpTimeout"] = self.source_ip_timeout
        if self.rewrite_cookie_name is not None:
            obj_dict["rewriteCookieName"] = self.rewrite_cookie_name
        if self.session_sticky_mode is not None:
            obj_dict["sessionStickyMode"] = self.session_sticky_mode
        if self.cookie_expire is not None:
            obj_dict["cookieExpire"] = self.cookie_expire
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.session_sticky_mode is None:
            raise Exception("session_sticky_mode can not None")


class ConnectionDrainConfig(object):

    def __init__(self, connection_drain_enabled, connection_drain_timeout, ):
        """
        :param connection_drain_enabled: 0-关闭 1-开启；若使用则必填
        :param connection_drain_timeout: 优雅中断时间0~900
        """
        self.connection_drain_enabled = connection_drain_enabled
        self.connection_drain_timeout = connection_drain_timeout
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.connection_drain_enabled is not None:
            obj_dict["connectionDrainEnabled"] = self.connection_drain_enabled
        if self.connection_drain_timeout is not None:
            obj_dict["connectionDrainTimeout"] = self.connection_drain_timeout
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.connection_drain_enabled is None:
            raise Exception("connection_drain_enabled can not None")
        if self.connection_drain_timeout is None:
            raise Exception("connection_drain_timeout can not None")


class CreateTargetGroupRequestParam(object):

    def __init__(self, name, algorithm, region_id, vpc_id, health_check_id=None, description=None, session_sticky=None, client_token=None, pool_protocol=None, all_port_forward=None, protocol=None, listener_id=None, connection_drain_config=None):
        """
        :param name: 名称
        :param algorithm: 调度算法。取值范围：rr（轮询）、wrr（带权重轮询）、lc（最少连接）、sh（源IP哈希）、th（四元组哈希）（调度算法为sh时，sessionStickyMode必须关闭）底层暂时传递rr，查询返回为wrr，因为rr是wrr的特殊情况，未来会逐步废弃rr。
        :param region_id: 区域ID
        :param vpc_id: #多az 专用这里和公有云对齐
        :param health_check_id: 健康检查ID，3.0/acs忽略该参数
        :param description: 详情
        :param session_sticky: 会话保持 方式
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param pool_protocol: 未对齐公有云，优先使用--底层兼容 传健康检查ID必传 0:unset 1:TCP 2:UDP 3:HTTP 4:HTTPS   
         （v2 https创建出来实际是http的，可正常绑定https监听器）
        :param all_port_forward: 0-不开启 1-开启
        :param protocol: 对齐公有云，与poolProtocol含义一样，支持TCP\\UDP\\HTTP\\HTTPS；3.0/acs资源池protocol和poolProtocol参数必传一个，不支持unset
        :param listener_id: 监听器ID，3.0/acs必传，4.0忽略
        :param connection_drain_config: 优雅中断特性，4.0底座1.25.05开始支持，云管V2.2.6版本开始支持，不使用非必填
        """
        self.name = name
        self.algorithm = algorithm
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.health_check_id = health_check_id
        self.description = description
        self.session_sticky = session_sticky
        self.client_token = client_token
        self.pool_protocol = pool_protocol
        self.all_port_forward = all_port_forward
        self.protocol = protocol
        self.listener_id = listener_id
        self.connection_drain_config = connection_drain_config

    def set_health_check_id(self, health_check_id):
        """
        :param health_check_id: 健康检查ID，3.0/acs忽略该参数
        """
        self.health_check_id = health_check_id

    def set_description(self, description):
        """
        :param description: 详情
        """
        self.description = description

    def set_session_sticky(self, session_sticky):
        """
        :param session_sticky: 会话保持 方式
        """
        self.session_sticky = session_sticky

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_pool_protocol(self, pool_protocol):
        """
        :param pool_protocol: 未对齐公有云，优先使用--底层兼容 传健康检查ID必传 0:unset 1:TCP 2:UDP 3:HTTP 4:HTTPS   
         （v2 https创建出来实际是http的，可正常绑定https监听器）
        """
        self.pool_protocol = pool_protocol

    def set_all_port_forward(self, all_port_forward):
        """
        :param all_port_forward: 0-不开启 1-开启
        """
        self.all_port_forward = all_port_forward

    def set_protocol(self, protocol):
        """
        :param protocol: 对齐公有云，与poolProtocol含义一样，支持TCP\\UDP\\HTTP\\HTTPS；3.0/acs资源池protocol和poolProtocol参数必传一个，不支持unset
        """
        self.protocol = protocol

    def set_listener_id(self, listener_id):
        """
        :param listener_id: 监听器ID，3.0/acs必传，4.0忽略
        """
        self.listener_id = listener_id

    def set_connection_drain_config(self, connection_drain_config):
        """
        :param connection_drain_config: 优雅中断特性，4.0底座1.25.05开始支持，云管V2.2.6版本开始支持，不使用非必填
        """
        self.connection_drain_config = connection_drain_config

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.algorithm is None:
            raise Exception("algorithm can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")

