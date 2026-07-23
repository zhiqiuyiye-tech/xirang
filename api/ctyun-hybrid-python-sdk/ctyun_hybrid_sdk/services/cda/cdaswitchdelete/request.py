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


class CdaSwitchDeleteRequest(CTYunRequest):
    """
    专线交换机删除
    """

    def __init__(self, request_param):
        super(CdaSwitchDeleteRequest, self).__init__("/v4/cda/switch/delete", "POST", "cda", "application/json")
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
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.switch_id is not None:
            body_param["switchId"] = self.parameters.switch_id
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


class CdaSwitchDeleteRequestParam(object):

    def __init__(self, region_id, resource_pool, switch_id, ip, ):
        """
        :param region_id: 资源池ID
        :param resource_pool: 同资源池ID
        :param switch_id: 交换机ID
        :param ip: 交换机IP
        """
        self.region_id = region_id
        self.resource_pool = resource_pool
        self.switch_id = switch_id
        self.ip = ip

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.resource_pool is None:
            raise Exception("resource_pool can not None")
        if self.switch_id is None:
            raise Exception("switch_id can not None")
        if self.ip is None:
            raise Exception("ip can not None")

