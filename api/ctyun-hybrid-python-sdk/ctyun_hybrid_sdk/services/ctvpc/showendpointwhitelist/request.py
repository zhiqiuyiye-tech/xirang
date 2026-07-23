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


class ShowEndpointWhitelistRequest(CTYunRequest):
    """
    查询终端节点白名单
    """

    def __init__(self, request_param):
        super(ShowEndpointWhitelistRequest, self).__init__("/v4/vpce/show-endpoint-whitelist", "GET", "ctvpc", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.endpoint_id is not None:
            query_param["endpointID"] = self.parameters.endpoint_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowEndpointWhitelistRequestParam(object):

    def __init__(self, region_id, endpoint_id, ):
        """
        :param region_id: 资源池id
        :param endpoint_id: 终端节点 ID，支持模糊查询
        """
        self.region_id = region_id
        self.endpoint_id = endpoint_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")

