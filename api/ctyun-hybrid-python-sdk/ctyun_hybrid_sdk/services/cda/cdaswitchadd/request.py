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


class CdaSwitchAddRequest(CTYunRequest):
    """
    专线交换机创建
    """

    def __init__(self, request_param):
        super(CdaSwitchAddRequest, self).__init__("/v4/cda/switch/add", "POST", "cda", "application/json")
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
        if self.parameters.switch_id is not None:
            body_param["switchId"] = self.parameters.switch_id
        if self.parameters.resource_pool_name is not None:
            body_param["resourcePoolName"] = self.parameters.resource_pool_name
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.factory is not None:
            body_param["factory"] = self.parameters.factory
        if self.parameters.access_point is not None:
            body_param["accessPoint"] = self.parameters.access_point
        if self.parameters.device_model is not None:
            body_param["deviceModel"] = self.parameters.device_model
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.ip is not None:
            body_param["ip"] = self.parameters.ip
        if self.parameters.login_port is not None:
            body_param["loginPort"] = self.parameters.login_port
        if self.parameters.as_value is not None:
            body_param["as"] = self.parameters.as_value
        if self.parameters.username is not None:
            body_param["username"] = self.parameters.username
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.configure_port is not None:
            body_param["configurePort"] = self.parameters.configure_port
        if self.parameters.vtep_vlan is not None:
            body_param["vtepVlan"] = self.parameters.vtep_vlan
        if self.parameters.vtep_ip is not None:
            body_param["vtepIp"] = self.parameters.vtep_ip
        if self.parameters.sys_mac is not None:
            body_param["sysMac"] = self.parameters.sys_mac
        if self.parameters.has_bleaf_route is not None:
            body_param["hasBleafRoute"] = self.parameters.has_bleaf_route
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


class CdaSwitchAddRequestParam(object):

    def __init__(self, region_id, switch_id, resource_pool_name, resource_type, resource_pool, name, factory, access_point, device_model, hostname, ip, login_port, as_value, username, password, configure_port, vtep_vlan, vtep_ip, sys_mac=None, has_bleaf_route=None):
        """
        :param region_id: 资源池id
        :param switch_id: 交换机ID(唯一值)，uuid格式
        :param resource_pool_name: 资源池名称
        :param resource_type: 资源池类型:CNP;MAZ
        :param resource_pool: 同regionID，以regionID为准，此参数无实际意义
        :param name: 交换机名称
        :param factory: 厂商
        :param access_point: 接入点 AP1、AP2
        :param device_model: 型号
        :param hostname: 交换机hostname
        :param ip: 交换机ip
        :param login_port: 登录port
        :param as_value: as号
        :param username: 登录名
        :param password: 登录密码
        :param configure_port: 配置端口
        :param vtep_vlan: VTEP VLAN
        :param vtep_ip: VTEP IP
        :param sys_mac: 交换机mac（多az并且是锐捷交换机则必填）（mac是查交换机配置查出来）
        :param has_bleaf_route: 标记交换机是否要配置BLEAF路由，默认为false（只有部分锐捷交换机需要配置）
        """
        self.region_id = region_id
        self.switch_id = switch_id
        self.resource_pool_name = resource_pool_name
        self.resource_type = resource_type
        self.resource_pool = resource_pool
        self.name = name
        self.factory = factory
        self.access_point = access_point
        self.device_model = device_model
        self.hostname = hostname
        self.ip = ip
        self.login_port = login_port
        self.as_value = as_value
        self.username = username
        self.password = password
        self.configure_port = configure_port
        self.vtep_vlan = vtep_vlan
        self.vtep_ip = vtep_ip
        self.sys_mac = sys_mac
        self.has_bleaf_route = has_bleaf_route

    def set_sys_mac(self, sys_mac):
        """
        :param sys_mac: 交换机mac（多az并且是锐捷交换机则必填）（mac是查交换机配置查出来）
        """
        self.sys_mac = sys_mac

    def set_has_bleaf_route(self, has_bleaf_route):
        """
        :param has_bleaf_route: 标记交换机是否要配置BLEAF路由，默认为false（只有部分锐捷交换机需要配置）
        """
        self.has_bleaf_route = has_bleaf_route

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.switch_id is None:
            raise Exception("switch_id can not None")
        if self.resource_pool_name is None:
            raise Exception("resource_pool_name can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.resource_pool is None:
            raise Exception("resource_pool can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.factory is None:
            raise Exception("factory can not None")
        if self.access_point is None:
            raise Exception("access_point can not None")
        if self.device_model is None:
            raise Exception("device_model can not None")
        if self.hostname is None:
            raise Exception("hostname can not None")
        if self.ip is None:
            raise Exception("ip can not None")
        if self.login_port is None:
            raise Exception("login_port can not None")
        if self.as_value is None:
            raise Exception("as_value can not None")
        if self.username is None:
            raise Exception("username can not None")
        if self.password is None:
            raise Exception("password can not None")
        if self.configure_port is None:
            raise Exception("configure_port can not None")
        if self.vtep_vlan is None:
            raise Exception("vtep_vlan can not None")
        if self.vtep_ip is None:
            raise Exception("vtep_ip can not None")

