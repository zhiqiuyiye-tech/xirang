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


class QueryItemsHybridRequest(CTYunRequest):
    """
    2.2.7.2提供   
    当前事件告警只支持弹性云主机vm
    """

    def __init__(self, request_param):
        super(QueryItemsHybridRequest, self).__init__("/v4/monitor/query-items", "GET", "monitor", "")
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
        if self.parameters.service is not None:
            query_param["service"] = self.parameters.service
        if self.parameters.dimension is not None:
            query_param["dimension"] = self.parameters.dimension
        if self.parameters.item_type is not None:
            query_param["itemType"] = self.parameters.item_type
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryItemsHybridRequestParam(object):

    def __init__(self, region_id, service=None, dimension=None, item_type=None):
        """
        :param region_id: 资源池ID
        :param service: 服务
        :param dimension: 维度(需要先填写服务)
        :param item_type: 本参数表示监控项类型。不传返回指标类型。取值范围：series：指标类型。event：事件类型。根据以上范围取值。当前只支持返回指标类型或事件类型。
        """
        self.region_id = region_id
        self.service = service
        self.dimension = dimension
        self.item_type = item_type

    def set_service(self, service):
        """
        :param service: 服务
        """
        self.service = service

    def set_dimension(self, dimension):
        """
        :param dimension: 维度(需要先填写服务)
        """
        self.dimension = dimension

    def set_item_type(self, item_type):
        """
        :param item_type: 本参数表示监控项类型。不传返回指标类型。取值范围：series：指标类型。event：事件类型。根据以上范围取值。当前只支持返回指标类型或事件类型。
        """
        self.item_type = item_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

