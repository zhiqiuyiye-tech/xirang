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


class IaasGetSummaryRequest(CTYunRequest):
    """
    查询资源池概况，比如地域，多az信息，支持的cpu架构，资源池占用类型，资源池版本信息等   
    开发未对齐原因：混合云资源池返回值不支持省、市等字段
    """

    def __init__(self, request_param):
        super(IaasGetSummaryRequest, self).__init__("/v4/region/get-summary", "GET", "common", "")
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
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IaasGetSummaryRequestParam(object):

    def __init__(self, region_id, ):
        """
        :param region_id: 资源池ID
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

