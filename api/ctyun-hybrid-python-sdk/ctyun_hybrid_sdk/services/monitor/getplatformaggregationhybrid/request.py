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


class GetPlatformAggregationHybridRequest(CTYunRequest):
    """
    查询平台监控聚合图表信息
    """

    def __init__(self, request_param):
        super(GetPlatformAggregationHybridRequest, self).__init__("/v4/monitor/get-platform-aggregation", "GET", "monitor", "")
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
        if self.parameters.code is not None:
            query_param["code"] = self.parameters.code
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.from_value is not None:
            query_param["from"] = self.parameters.from_value
        if self.parameters.to is not None:
            query_param["to"] = self.parameters.to
        if self.parameters.instance is not None:
            query_param["instance"] = self.parameters.instance
        if self.parameters.server is not None:
            query_param["server"] = self.parameters.server
        if self.parameters.db is not None:
            query_param["db"] = self.parameters.db
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetPlatformAggregationHybridRequestParam(object):

    def __init__(self, code, type, from_value, to, instance=None, server=None, db=None):
        """
        :param code: 监控指标
        :param type: 组件类型，当前支持：关系型数据库-opengauss，时序数据库-victoriametrics，消息队列-rabbitmq，缓存-redis
        :param from_value: 起始时间
        :param to: 结束时间
        :param instance: 监控实例，组件选择时序数据库-victoriametrics，消息队列-rabbitmq，缓存-redis时，必填
        :param server: 监控服务，组件选择关系型数据库-opengauss时，必填
        :param db: 监控数据库，组件选择关系型数据库-opengauss时，必填
        """
        self.code = code
        self.type = type
        self.from_value = from_value
        self.to = to
        self.instance = instance
        self.server = server
        self.db = db

    def set_instance(self, instance):
        """
        :param instance: 监控实例，组件选择时序数据库-victoriametrics，消息队列-rabbitmq，缓存-redis时，必填
        """
        self.instance = instance

    def set_server(self, server):
        """
        :param server: 监控服务，组件选择关系型数据库-opengauss时，必填
        """
        self.server = server

    def set_db(self, db):
        """
        :param db: 监控数据库，组件选择关系型数据库-opengauss时，必填
        """
        self.db = db

    def check_param(self):
        """
        the param required check
        """
        if self.code is None:
            raise Exception("code can not None")
        if self.type is None:
            raise Exception("type can not None")
        if self.from_value is None:
            raise Exception("from_value can not None")
        if self.to is None:
            raise Exception("to can not None")

