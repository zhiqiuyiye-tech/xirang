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


class AddEndpointWhitelistRequest(CTYunRequest):
    """
    添加终端节点白名单，acs类型资源池反向终端节点不支持白名单功能
    """

    def __init__(self, request_param):
        super(AddEndpointWhitelistRequest, self).__init__("/v4/vpce/add-endpoint-whitelist", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_id is not None:
            body_param["endpointID"] = self.parameters.endpoint_id
        if self.parameters.whitelist is not None:
            body_param["whitelist"] = self.parameters.whitelist
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class AddEndpointWhitelistRequestParam(object):

    def __init__(self, region_id, endpoint_id, whitelist, client_token=None):
        """
        :param region_id: 资源池id
        :param endpoint_id: 终端节点ID
        :param whitelist: 白名单 总数最大20个 注意:此参数为数组
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        """
        self.region_id = region_id
        self.endpoint_id = endpoint_id
        self.whitelist = whitelist
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，可传但是不进行校验
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")
        if self.whitelist is None:
            raise Exception("whitelist can not None")

