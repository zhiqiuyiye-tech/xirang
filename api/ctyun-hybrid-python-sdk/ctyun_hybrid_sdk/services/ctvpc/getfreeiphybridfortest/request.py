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


class GetFreeIpHybridForTestRequest(CTYunRequest):
    """
    内部测试使用，查询可用eip网段地址
    """

    def __init__(self, request_param):
        super(GetFreeIpHybridForTestRequest, self).__init__("/v4/eip/free-ip", "GET", "ctvpc", "")
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
        if self.parameters.client_token is not None:
            query_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.provider is not None:
            query_param["provider"] = self.parameters.provider
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetFreeIpHybridForTestRequestParam(object):

    def __init__(self, region_id, client_token=None, provider=None, project_id=None):
        """
        :param client_token: token
        :param region_id: 资源池ID
        :param provider: 网关类型，默认internet
        :param project_id: 企业项目id
        """
        self.client_token = client_token
        self.region_id = region_id
        self.provider = provider
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: token
        """
        self.client_token = client_token

    def set_provider(self, provider):
        """
        :param provider: 网关类型，默认internet
        """
        self.provider = provider

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

