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


class GetRegionTotalRemainMetricRequest(CTYunRequest):
    """
    获取单资源池的总量和剩余量
    """

    def __init__(self, request_param):
        super(GetRegionTotalRemainMetricRequest, self).__init__("/v4/region/get-total-remain-metric", "GET", "common", "")
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
        if self.parameters.pool_type is not None:
            query_param["poolType"] = self.parameters.pool_type
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetRegionTotalRemainMetricRequestParam(object):

    def __init__(self, region_id, pool_type=None):
        """
        :param region_id: 
        :param pool_type: 查询全部资源池类型 暂时只支持maz，openapi只支持4.0的maz，其他忽略，该参数暂不支持
        """
        self.region_id = region_id
        self.pool_type = pool_type

    def set_pool_type(self, pool_type):
        """
        :param pool_type: 查询全部资源池类型 暂时只支持maz，openapi只支持4.0的maz，其他忽略，该参数暂不支持
        """
        self.pool_type = pool_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

