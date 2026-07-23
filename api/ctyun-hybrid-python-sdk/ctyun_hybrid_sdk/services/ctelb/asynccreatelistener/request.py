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


class AsyncCreateListenerRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，注意该接口不兼容创建4.0资源池资源
    """

    def __init__(self, request_param):
        super(AsyncCreateListenerRequest, self).__init__("/v4/elb/async-create-listener", "POST", "ctelb", "application/json")
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
        if self.parameters.load_balance_id is not None:
            body_param["loadBalanceID"] = self.parameters.load_balance_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.protocol_port is not None:
            body_param["protocolPort"] = self.parameters.protocol_port
        if self.parameters.certificate_id is not None:
            body_param["certificateID"] = self.parameters.certificate_id
        if self.parameters.ca_enabled is not None:
            body_param["caEnabled"] = self.parameters.ca_enabled
        if self.parameters.client_certificate_id is not None:
            body_param["clientCertificateID"] = self.parameters.client_certificate_id
        if self.parameters.target_group is not None:
            if type(self.parameters.target_group) is dict:
                target_group_dict_value = self.parameters.target_group
            else:
                target_group_dict_value = self.parameters.target_group.get_dic()
            body_param["targetGroup"] = target_group_dict_value
        if self.parameters.access_control_id is not None:
            body_param["accessControlID"] = self.parameters.access_control_id
        if self.parameters.access_control_type is not None:
            body_param["accessControlType"] = self.parameters.access_control_type
        if self.parameters.forwarded_for_enabled is not None:
            body_param["forwardedForEnabled"] = self.parameters.forwarded_for_enabled
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


class TargetGroup(object):

    def __init__(self, name, algorithm, targets=None, health_check=None, session_sticky=None):
        """
        :param name: 后端服务组名字
        :param algorithm: 负载均衡算法，支持: rr (轮询), lc (最少链接)
        :param targets: 后端服务
        :param health_check: 健康检查配置
        :param session_sticky: 会话保持
        """
        self.name = name
        self.algorithm = algorithm
        self.targets = targets
        self.health_check = health_check
        self.session_sticky = session_sticky
        self.check_param()

    def set_targets(self, targets):
        """
        :param targets: 后端服务
        """
        self.targets = targets

    def set_health_check(self, health_check):
        """
        :param health_check: 健康检查配置
        """
        self.health_check = health_check

    def set_session_sticky(self, session_sticky):
        """
        :param session_sticky: 会话保持
        """
        self.session_sticky = session_sticky

    def get_dic(self):
        obj_dict = dict()
        if self.name is not None:
            obj_dict["name"] = self.name
        if self.algorithm is not None:
            obj_dict["algorithm"] = self.algorithm
        if self.targets is not None:
            targets_array = []
            for item in self.targets:
                if type(item) is dict:
                    targets_array.append(item)
                else:
                    targets_array.append(item.get_dic())
            obj_dict["targets"] = targets_array
        if self.health_check is not None:
            if type(self.health_check) is dict:
                obj_dict["healthCheck"] = self.health_check
            else:
                obj_dict["healthCheck"] = self.health_check.get_dic()
        if self.session_sticky is not None:
            if type(self.session_sticky) is dict:
                obj_dict["sessionSticky"] = self.session_sticky
            else:
                obj_dict["sessionSticky"] = self.session_sticky.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.algorithm is None:
            raise Exception("algorithm can not None")


class Target(object):

    def __init__(self, instance_id, protocol_port, instance_type, weight, address, ):
        """
        :param instance_id: 后端服务主机 id
        :param protocol_port: 后端服务监听端口
        :param instance_type: 后端服务主机类型，目前支持 vm
        :param weight: 后端服务主机权重: 1 - 256
        :param address: 后端服务主机主网卡所在的 IP
        """
        self.instance_id = instance_id
        self.protocol_port = protocol_port
        self.instance_type = instance_type
        self.weight = weight
        self.address = address
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.instance_id is not None:
            obj_dict["instanceID"] = self.instance_id
        if self.protocol_port is not None:
            obj_dict["protocolPort"] = self.protocol_port
        if self.instance_type is not None:
            obj_dict["instanceType"] = self.instance_type
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        if self.address is not None:
            obj_dict["address"] = self.address
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.protocol_port is None:
            raise Exception("protocol_port can not None")
        if self.instance_type is None:
            raise Exception("instance_type can not None")
        if self.weight is None:
            raise Exception("weight can not None")
        if self.address is None:
            raise Exception("address can not None")


class HealthCheck(object):

    def __init__(self, protocol, timeout=None, interval=None, max_retry=None, http_method=None, http_url_path=None, http_expected_codes=None):
        """
        :param protocol: 健康检查协议。取值范围：TCP、UDP、HTTP
        :param timeout: 健康检查响应的最大超时时间，取值范围：2-60秒，默认为2秒
        :param interval: 负载均衡进行健康检查的时间间隔，取值范围：1-20940秒，默认为5秒
        :param max_retry: 最大重试次数，取值范围：1-10次，默认为2次
        :param http_method: 仅当protocol为HTTP时必填且生效,HTTP请求的方法默认GET，{GET/HEAD}
        :param http_url_path: 仅当protocol为HTTP时必填且生效,默认为'/',支持的最大字符长度：80
        :param http_expected_codes: 仅当protocol为HTTP时必填且生效，最长支持64个字符，只能是三位数，可以以,分隔表示多个，或者以-分割表示范围，默认200
        """
        self.protocol = protocol
        self.timeout = timeout
        self.interval = interval
        self.max_retry = max_retry
        self.http_method = http_method
        self.http_url_path = http_url_path
        self.http_expected_codes = http_expected_codes
        self.check_param()

    def set_timeout(self, timeout):
        """
        :param timeout: 健康检查响应的最大超时时间，取值范围：2-60秒，默认为2秒
        """
        self.timeout = timeout

    def set_interval(self, interval):
        """
        :param interval: 负载均衡进行健康检查的时间间隔，取值范围：1-20940秒，默认为5秒
        """
        self.interval = interval

    def set_max_retry(self, max_retry):
        """
        :param max_retry: 最大重试次数，取值范围：1-10次，默认为2次
        """
        self.max_retry = max_retry

    def set_http_method(self, http_method):
        """
        :param http_method: 仅当protocol为HTTP时必填且生效,HTTP请求的方法默认GET，{GET/HEAD}
        """
        self.http_method = http_method

    def set_http_url_path(self, http_url_path):
        """
        :param http_url_path: 仅当protocol为HTTP时必填且生效,默认为'/',支持的最大字符长度：80
        """
        self.http_url_path = http_url_path

    def set_http_expected_codes(self, http_expected_codes):
        """
        :param http_expected_codes: 仅当protocol为HTTP时必填且生效，最长支持64个字符，只能是三位数，可以以,分隔表示多个，或者以-分割表示范围，默认200
        """
        self.http_expected_codes = http_expected_codes

    def get_dic(self):
        obj_dict = dict()
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.timeout is not None:
            obj_dict["timeout"] = self.timeout
        if self.interval is not None:
            obj_dict["interval"] = self.interval
        if self.max_retry is not None:
            obj_dict["maxRetry"] = self.max_retry
        if self.http_method is not None:
            obj_dict["httpMethod"] = self.http_method
        if self.http_url_path is not None:
            obj_dict["httpUrlPath"] = self.http_url_path
        if self.http_expected_codes is not None:
            obj_dict["httpExpectedCodes"] = self.http_expected_codes
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.protocol is None:
            raise Exception("protocol can not None")


class SessionSticky(object):

    def __init__(self, session_type, cookie_name=None, persistence_timeout=None):
        """
        :param session_type: 会话保持类型。取值范围：APP_COOKIE、HTTP_COOKIE、SOURCE_IP
        :param cookie_name: cookie名称，当 sessionType 为 APP_COOKIE 时，为必填参数
        :param persistence_timeout: 会话过期时间，当 sessionType 为 APP_COOKIE 或 SOURCE_IP 时，为必填参数
        """
        self.session_type = session_type
        self.cookie_name = cookie_name
        self.persistence_timeout = persistence_timeout
        self.check_param()

    def set_cookie_name(self, cookie_name):
        """
        :param cookie_name: cookie名称，当 sessionType 为 APP_COOKIE 时，为必填参数
        """
        self.cookie_name = cookie_name

    def set_persistence_timeout(self, persistence_timeout):
        """
        :param persistence_timeout: 会话过期时间，当 sessionType 为 APP_COOKIE 或 SOURCE_IP 时，为必填参数
        """
        self.persistence_timeout = persistence_timeout

    def get_dic(self):
        obj_dict = dict()
        if self.session_type is not None:
            obj_dict["sessionType"] = self.session_type
        if self.cookie_name is not None:
            obj_dict["cookieName"] = self.cookie_name
        if self.persistence_timeout is not None:
            obj_dict["persistenceTimeout"] = self.persistence_timeout
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.session_type is None:
            raise Exception("session_type can not None")


class AsyncCreateListenerRequestParam(object):

    def __init__(self, client_token, region_id, load_balance_id, name, protocol, protocol_port, target_group, description=None, certificate_id=None, ca_enabled=None, client_certificate_id=None, access_control_id=None, access_control_type=None, forwarded_for_enabled=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池id
        :param load_balance_id: 负载均衡实例ID
        :param name: 监听器名称
        :param description: 描述
        :param protocol: 监听协议。取值范围：TCP、UDP、HTTP、HTTPS
        :param protocol_port: 负载均衡实例监听端口。取值：1-65535
        :param certificate_id: 证书ID。当protocol为HTTPS时,此参数必选
        :param ca_enabled: 是否开启双向认证。false（不开启）、true（开启）
        :param client_certificate_id: 双向认证的证书ID
        :param target_group: 后端服务组
        :param access_control_id: 访问控制ID
        :param access_control_type: 访问控制类型。取值范围：Close（未启用）、White（白名单）、Black（黑名单）
        :param forwarded_for_enabled: x forward for功能。false（未开启）、true（开启）
        """
        self.client_token = client_token
        self.region_id = region_id
        self.load_balance_id = load_balance_id
        self.name = name
        self.description = description
        self.protocol = protocol
        self.protocol_port = protocol_port
        self.certificate_id = certificate_id
        self.ca_enabled = ca_enabled
        self.client_certificate_id = client_certificate_id
        self.target_group = target_group
        self.access_control_id = access_control_id
        self.access_control_type = access_control_type
        self.forwarded_for_enabled = forwarded_for_enabled

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_certificate_id(self, certificate_id):
        """
        :param certificate_id: 证书ID。当protocol为HTTPS时,此参数必选
        """
        self.certificate_id = certificate_id

    def set_ca_enabled(self, ca_enabled):
        """
        :param ca_enabled: 是否开启双向认证。false（不开启）、true（开启）
        """
        self.ca_enabled = ca_enabled

    def set_client_certificate_id(self, client_certificate_id):
        """
        :param client_certificate_id: 双向认证的证书ID
        """
        self.client_certificate_id = client_certificate_id

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

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.load_balance_id is None:
            raise Exception("load_balance_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.protocol_port is None:
            raise Exception("protocol_port can not None")
        if self.target_group is None:
            raise Exception("target_group can not None")

