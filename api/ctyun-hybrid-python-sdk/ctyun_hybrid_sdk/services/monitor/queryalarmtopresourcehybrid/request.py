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


class QueryAlarmTopResourceHybridRequest(CTYunRequest):
    """
    调用此接口可查询指定资源池下告警Top实例。
    """

    def __init__(self, request_param):
        super(QueryAlarmTopResourceHybridRequest, self).__init__("/v4/monitor/query-alarm-top-resource", "GET", "monitor", "")
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
        if self.parameters.range is not None:
            query_param["range"] = self.parameters.range
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryAlarmTopResourceHybridRequestParam(object):

    def __init__(self, region_id, range=None):
        """
        :param region_id: 资源池ID
        :param range: 时间范围，默认值:7d，取值示例：7d，24h，6h 分别代表最近7天，最近24小时，最近6小时。 时间范围最长不能超过3个月
        """
        self.region_id = region_id
        self.range = range

    def set_range(self, range):
        """
        :param range: 时间范围，默认值:7d，取值示例：7d，24h，6h 分别代表最近7天，最近24小时，最近6小时。 时间范围最长不能超过3个月
        """
        self.range = range

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

