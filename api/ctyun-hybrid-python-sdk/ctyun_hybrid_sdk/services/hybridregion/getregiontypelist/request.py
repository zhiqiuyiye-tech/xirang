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


class GetRegionTypeListRequest(CTYunRequest):
    """
    查询资源池类型列表
    """

    def __init__(self, request_param):
        super(GetRegionTypeListRequest, self).__init__("/v1/regions/region-type", "GET", "hybridregion", "")
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
        if self.parameters.region_type_code is not None:
            query_param["regionTypeCode"] = self.parameters.region_type_code
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetRegionTypeListRequestParam(object):

    def __init__(self, region_type_code=None, status=None):
        """
        :param region_type_code: 资源池类型Code
        :param status: 1-筛选上线状态的资源池类型 ，只有1筛选，其余参数无效
        """
        self.region_type_code = region_type_code
        self.status = status

    def set_region_type_code(self, region_type_code):
        """
        :param region_type_code: 资源池类型Code
        """
        self.region_type_code = region_type_code

    def set_status(self, status):
        """
        :param status: 1-筛选上线状态的资源池类型 ，只有1筛选，其余参数无效
        """
        self.status = status

    def check_param(self):
        """
        the param required check
        """
        pass

