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


class QueryAlarmTrendHybridRequest(CTYunRequest):
    """
    调用此接口可根据时间范围查询指定资源池告警次数的变化趋势。
    """

    def __init__(self, request_param):
        super(QueryAlarmTrendHybridRequest, self).__init__("/v4.1/monitor/query-alarm-trend", "GET", "monitor", "")
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
        if self.parameters.start_time is not None:
            query_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            query_param["endTime"] = self.parameters.end_time
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryAlarmTrendHybridRequestParam(object):

    def __init__(self, region_id, start_time=None, end_time=None):
        """
        :param region_id: 
        :param start_time: 起始时间戳，startTime和endTime需同时传或同时不传， startTime和endTime同时不传时按最近7天的范围计算。   
         参数说明：1. startTime - endTime 指定范围的秒数，如果属于同一天，则会统计当天全天周期；即使只有1s，也会统计当天全天周期。   2.  0点隶属于上一天。
        :param end_time: 结束时间戳，配合startTime一起使用
        """
        self.region_id = region_id
        self.start_time = start_time
        self.end_time = end_time

    def set_start_time(self, start_time):
        """
        :param start_time: 起始时间戳，startTime和endTime需同时传或同时不传， startTime和endTime同时不传时按最近7天的范围计算。   
         参数说明：1. startTime - endTime 指定范围的秒数，如果属于同一天，则会统计当天全天周期；即使只有1s，也会统计当天全天周期。   2.  0点隶属于上一天。
        """
        self.start_time = start_time

    def set_end_time(self, end_time):
        """
        :param end_time: 结束时间戳，配合startTime一起使用
        """
        self.end_time = end_time

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

