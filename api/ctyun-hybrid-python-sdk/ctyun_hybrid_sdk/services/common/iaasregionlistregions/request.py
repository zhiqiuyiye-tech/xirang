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


class IaasRegionListRegionsRequest(CTYunRequest):
    """
    查询租户可见的资源池列表。仅查询4.0多可用区的资源池   
       
    该接口所属rbac模块
    """

    def __init__(self, request_param):
        super(IaasRegionListRegionsRequest, self).__init__("/v4/region/list-regions", "GET", "common", "")
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
        if self.parameters.region_name is not None:
            query_param["regionName"] = self.parameters.region_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IaasRegionListRegionsRequestParam(object):

    def __init__(self, region_name=None):
        """
        :param region_name: 资源池名称
        """
        self.region_name = region_name

    def set_region_name(self, region_name):
        """
        :param region_name: 资源池名称
        """
        self.region_name = region_name

    def check_param(self):
        """
        the param required check
        """
        pass

