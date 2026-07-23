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


class GetSegmentsOpenApiRequest(CTYunRequest):
    """
    获取可用地址范围
    """

    def __init__(self, request_param):
        super(GetSegmentsOpenApiRequest, self).__init__("/v4/eipPool/segments", "GET", "ctvpc", "")
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
        if self.parameters.provider is not None:
            query_param["provider"] = self.parameters.provider
        if self.parameters.eip_group_id is not None:
            query_param["eipGroupID"] = self.parameters.eip_group_id
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetSegmentsOpenApiRequestParam(object):

    def __init__(self, provider, region_id, eip_group_id=None):
        """
        :param provider: 
        :param eip_group_id: 
        :param region_id: 
        """
        self.provider = provider
        self.eip_group_id = eip_group_id
        self.region_id = region_id

    def set_eip_group_id(self, eip_group_id):
        """
        :param eip_group_id: 
        """
        self.eip_group_id = eip_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.provider is None:
            raise Exception("provider can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

