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


class CdaPhysicalLineAddRequest(CTYunRequest):
    """
    物理专线创建
    """

    def __init__(self, request_param):
        super(CdaPhysicalLineAddRequest, self).__init__("/v4/cda/physical-line/add", "POST", "cda", "application/json")
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
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.resource_pool_name is not None:
            body_param["resourcePoolName"] = self.parameters.resource_pool_name
        if self.parameters.line_name is not None:
            body_param["lineName"] = self.parameters.line_name
        if self.parameters.switch_ip is not None:
            body_param["switchIp"] = self.parameters.switch_ip
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.port_type is not None:
            body_param["portType"] = self.parameters.port_type
        if self.parameters.is_shared is not None:
            body_param["isShared"] = self.parameters.is_shared
        if self.parameters.port_name is not None:
            body_param["portName"] = self.parameters.port_name
        if self.parameters.line_type is not None:
            body_param["lineType"] = self.parameters.line_type
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.vlan is not None:
            body_param["vlan"] = self.parameters.vlan
        if self.parameters.tag is not None:
            body_param["tag"] = self.parameters.tag
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.local_connect_ip is not None:
            body_param["localConnectIP"] = self.parameters.local_connect_ip
        if self.parameters.remote_connect_ip is not None:
            body_param["remoteConnectIP"] = self.parameters.remote_connect_ip
        if self.parameters.local_connect_ipv6 is not None:
            body_param["localConnectIPv6"] = self.parameters.local_connect_ipv6
        if self.parameters.remote_connect_ipv6 is not None:
            body_param["remoteConnectIPv6"] = self.parameters.remote_connect_ipv6
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.location is not None:
            body_param["location"] = self.parameters.location
        if self.parameters.access_point is not None:
            body_param["accessPoint"] = self.parameters.access_point
        if self.parameters.linecode is not None:
            body_param["linecode"] = self.parameters.linecode
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


class CdaPhysicalLineAddRequestParam(object):

    def __init__(self, region_id, account, line_name, switch_ip, hostname, port_type, is_shared, port_name, line_type, bandwidth, vlan, tag, ip_version, resource_pool=None, resource_pool_name=None, local_connect_ip=None, remote_connect_ip=None, local_connect_ipv6=None, remote_connect_ipv6=None, description=None, location=None, access_point=None, linecode=None):
        """
        :param region_id: 资源池id
        :param account: 账户
        :param resource_pool: 无实际意义
        :param resource_pool_name: 无实际意义
        :param line_name: 长度为2-63字符，不支持中文
        :param switch_ip: 交换机ip
        :param hostname: 交换机hostname
        :param port_type: 端口类型（10G、1G）
        :param is_shared: 端口类别：独享（0）、共享（1）两种，默认为共享
        :param port_name: 端口名称
        :param line_type: 专线类型（PON\\IPRAN）
        :param bandwidth: 1-999999999
        :param vlan: 接入端口放行vlan, 范围：1-4094
        :param tag: 是否带vlan tag,新增字段 0-不带tag 1-带tag
        :param ip_version: 专线类型：IPV4 / DUALSTACK / IPV6
        :param local_connect_ip: IPV4 / DUALSTACK 时必填
        :param remote_connect_ip: IPV4 / DUALSTACK 时必填
        :param local_connect_ipv6: IPV6 / DUALSTACK 时必填
        :param remote_connect_ipv6: IPV6 / DUALSTACK 时必填
        :param description: 长度为2-200字符 不支持中文 、中文符号
        :param location: 插入位置
        :param access_point: 接入点，多az必填：AP1、AP2
        :param linecode: 电路代号
        """
        self.region_id = region_id
        self.account = account
        self.resource_pool = resource_pool
        self.resource_pool_name = resource_pool_name
        self.line_name = line_name
        self.switch_ip = switch_ip
        self.hostname = hostname
        self.port_type = port_type
        self.is_shared = is_shared
        self.port_name = port_name
        self.line_type = line_type
        self.bandwidth = bandwidth
        self.vlan = vlan
        self.tag = tag
        self.ip_version = ip_version
        self.local_connect_ip = local_connect_ip
        self.remote_connect_ip = remote_connect_ip
        self.local_connect_ipv6 = local_connect_ipv6
        self.remote_connect_ipv6 = remote_connect_ipv6
        self.description = description
        self.location = location
        self.access_point = access_point
        self.linecode = linecode

    def set_resource_pool(self, resource_pool):
        """
        :param resource_pool: 无实际意义
        """
        self.resource_pool = resource_pool

    def set_resource_pool_name(self, resource_pool_name):
        """
        :param resource_pool_name: 无实际意义
        """
        self.resource_pool_name = resource_pool_name

    def set_local_connect_ip(self, local_connect_ip):
        """
        :param local_connect_ip: IPV4 / DUALSTACK 时必填
        """
        self.local_connect_ip = local_connect_ip

    def set_remote_connect_ip(self, remote_connect_ip):
        """
        :param remote_connect_ip: IPV4 / DUALSTACK 时必填
        """
        self.remote_connect_ip = remote_connect_ip

    def set_local_connect_ipv6(self, local_connect_ipv6):
        """
        :param local_connect_ipv6: IPV6 / DUALSTACK 时必填
        """
        self.local_connect_ipv6 = local_connect_ipv6

    def set_remote_connect_ipv6(self, remote_connect_ipv6):
        """
        :param remote_connect_ipv6: IPV6 / DUALSTACK 时必填
        """
        self.remote_connect_ipv6 = remote_connect_ipv6

    def set_description(self, description):
        """
        :param description: 长度为2-200字符 不支持中文 、中文符号
        """
        self.description = description

    def set_location(self, location):
        """
        :param location: 插入位置
        """
        self.location = location

    def set_access_point(self, access_point):
        """
        :param access_point: 接入点，多az必填：AP1、AP2
        """
        self.access_point = access_point

    def set_linecode(self, linecode):
        """
        :param linecode: 电路代号
        """
        self.linecode = linecode

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.account is None:
            raise Exception("account can not None")
        if self.line_name is None:
            raise Exception("line_name can not None")
        if self.switch_ip is None:
            raise Exception("switch_ip can not None")
        if self.hostname is None:
            raise Exception("hostname can not None")
        if self.port_type is None:
            raise Exception("port_type can not None")
        if self.is_shared is None:
            raise Exception("is_shared can not None")
        if self.port_name is None:
            raise Exception("port_name can not None")
        if self.line_type is None:
            raise Exception("line_type can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")
        if self.vlan is None:
            raise Exception("vlan can not None")
        if self.tag is None:
            raise Exception("tag can not None")
        if self.ip_version is None:
            raise Exception("ip_version can not None")

