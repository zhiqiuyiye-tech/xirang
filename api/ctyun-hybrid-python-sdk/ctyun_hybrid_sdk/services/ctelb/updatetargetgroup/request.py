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


class UpdateTargetGroupRequest(CTYunRequest):
    """
    更新后端服务组   
       
    #### 备注   
    * 不支持3.0，因为无法兼容更换健康检查逻辑
    """

    def __init__(self, request_param):
        super(UpdateTargetGroupRequest, self).__init__("/v4/elb/update-target-group", "POST", "ctelb", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.algorithm is not None:
            body_param["algorithm"] = self.parameters.algorithm
        if self.parameters.session_sticky is not None:
            if type(self.parameters.session_sticky) is dict:
                session_sticky_dict_value = self.parameters.session_sticky
            else:
                session_sticky_dict_value = self.parameters.session_sticky.get_dic()
            body_param["sessionSticky"] = session_sticky_dict_value
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.health_check_id is not None:
            body_param["healthCheckID"] = self.parameters.health_check_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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
        :param session_sticky_mode: 会话保持模式，支持取值：CLOSE（关闭）、INSERT（插入）、REWRITE（重写）、SOURCE_IP（源IP）（底层说创建为SOURCE_IP时协议为4层，其余未传协议，故创建为close不能修改为source_ip,创建为source_ip可以修改为close）
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


class UpdateTargetGroupRequestParam(object):

    def __init__(self, region_id, id, name=None, algorithm=None, session_sticky=None, description=None, health_check_id=None, az_name=None, client_token=None, project_id=None, connection_drain_config=None):
        """
        :param region_id: 
        :param id: 主机组id
        :param name: 名称
        :param algorithm: 调度算法。取值范围：rr（轮询）、wrr（带权重轮询）、lc（最少连接）、sh（源IP哈希）、th（四元组哈希）
        :param session_sticky: 会话保持 
        :param description: 主机组描述
        :param health_check_id: 健康检查ID
        :param az_name: 多az专用(私有云忽略)
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        :param project_id: （非必填，并且此字段在私有云不具有实际意义）
        :param connection_drain_config: 优雅中断特性，4.0底座1.25.05开始支持，云管V2.2.6版本开始支持，不使用非必填
        """
        self.region_id = region_id
        self.id = id
        self.name = name
        self.algorithm = algorithm
        self.session_sticky = session_sticky
        self.description = description
        self.health_check_id = health_check_id
        self.az_name = az_name
        self.client_token = client_token
        self.project_id = project_id
        self.connection_drain_config = connection_drain_config

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_algorithm(self, algorithm):
        """
        :param algorithm: 调度算法。取值范围：rr（轮询）、wrr（带权重轮询）、lc（最少连接）、sh（源IP哈希）、th（四元组哈希）
        """
        self.algorithm = algorithm

    def set_session_sticky(self, session_sticky):
        """
        :param session_sticky: 会话保持 
        """
        self.session_sticky = session_sticky

    def set_description(self, description):
        """
        :param description: 主机组描述
        """
        self.description = description

    def set_health_check_id(self, health_check_id):
        """
        :param health_check_id: 健康检查ID
        """
        self.health_check_id = health_check_id

    def set_az_name(self, az_name):
        """
        :param az_name: 多az专用(私有云忽略)
        """
        self.az_name = az_name

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.project_id = project_id

    def set_connection_drain_config(self, connection_drain_config):
        """
        :param connection_drain_config: 优雅中断特性，4.0底座1.25.05开始支持，云管V2.2.6版本开始支持，不使用非必填
        """
        self.connection_drain_config = connection_drain_config

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

