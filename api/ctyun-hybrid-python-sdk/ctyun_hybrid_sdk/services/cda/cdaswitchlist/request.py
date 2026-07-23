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


class CdaSwitchListRequest(CTYunRequest):
    """
    专线交换机查询
    """

    def __init__(self, request_param):
        super(CdaSwitchListRequest, self).__init__("/v4/cda/switch/list", "POST", "cda", "application/json")
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
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.switch_id is not None:
            body_param["switchId"] = self.parameters.switch_id
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.ip is not None:
            body_param["ip"] = self.parameters.ip
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


class CdaSwitchListRequestParam(object):

    def __init__(self, resource_pool, name=None, switch_id=None, hostname=None, ip=None):
        """
        :param resource_pool: 资源池ID
        :param name: 交换机name
        :param switch_id: 交换机ID
        :param hostname: 交换机hostname
        :param ip: 交换机IP
        """
        self.resource_pool = resource_pool
        self.name = name
        self.switch_id = switch_id
        self.hostname = hostname
        self.ip = ip

    def set_name(self, name):
        """
        :param name: 交换机name
        """
        self.name = name

    def set_switch_id(self, switch_id):
        """
        :param switch_id: 交换机ID
        """
        self.switch_id = switch_id

    def set_hostname(self, hostname):
        """
        :param hostname: 交换机hostname
        """
        self.hostname = hostname

    def set_ip(self, ip):
        """
        :param ip: 交换机IP
        """
        self.ip = ip

    def check_param(self):
        """
        the param required check
        """
        if self.resource_pool is None:
            raise Exception("resource_pool can not None")

