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


class ExportAlertHistoryHybridRequest(CTYunRequest):
    """
    导出告警历史   
    返回字段：   
    监控对象、首次告警触发条件、告警ID、产品类型、告警级别、通知对象、所属用户、告警规则、发生时间、持续时间、状态、确认用户、清除用户（当前告警不返回此字段）
    """

    def __init__(self, request_param):
        super(ExportAlertHistoryHybridRequest, self).__init__("/v4/monitor/export-alert-history", "POST", "monitor", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
        if self.parameters.search_key is not None:
            body_param["searchKey"] = self.parameters.search_key
        if self.parameters.search_value is not None:
            body_param["searchValue"] = self.parameters.search_value
        if self.parameters.service is not None:
            body_param["service"] = self.parameters.service
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ExportAlertHistoryHybridRequestParam(object):

    def __init__(self, region_id, status, search_key=None, search_value=None, service=None, end_time=None, start_time=None):
        """
        :param region_id: 资源池ID
        :param status: 本参数表示状态。取值范围：   
         0：正在告警。   
         1：告警历史。   
         根据以上范围取值。
        :param search_key: 本参数表示搜索关键词。取值范围：   
         alarmRuleID：告警规则ID，精确查询。   
         name：告警规则名称，模糊查询。   
         根据以上范围取值。
        :param search_value: 配合searchKey使用，对应的值
        :param service: vm:云主机；ph:宿主机；bare_metal:裸金属；scaling:弹性伸缩；eip:弹性IP；elb:负载均衡 注意:此参数为数组
        :param end_time: 查询状态为告警历史（参数status=1）时的结束时间戳，默认值：当前时间戳， 配合startTime一起使用。查询为当前告警（status=0）时，不起作用
        :param start_time: 查询状态为告警历史（参数status=1）时的起始时间戳，  默认值：24小时前时间戳，startTime和endTime需同时传或同时不传。查询为当前告警（status=0）时，不起作用
        """
        self.region_id = region_id
        self.status = status
        self.search_key = search_key
        self.search_value = search_value
        self.service = service
        self.end_time = end_time
        self.start_time = start_time

    def set_search_key(self, search_key):
        """
        :param search_key: 本参数表示搜索关键词。取值范围：   
         alarmRuleID：告警规则ID，精确查询。   
         name：告警规则名称，模糊查询。   
         根据以上范围取值。
        """
        self.search_key = search_key

    def set_search_value(self, search_value):
        """
        :param search_value: 配合searchKey使用，对应的值
        """
        self.search_value = search_value

    def set_service(self, service):
        """
        :param service: vm:云主机；ph:宿主机；bare_metal:裸金属；scaling:弹性伸缩；eip:弹性IP；elb:负载均衡
        """
        self.service = service

    def set_end_time(self, end_time):
        """
        :param end_time: 查询状态为告警历史（参数status=1）时的结束时间戳，默认值：当前时间戳， 配合startTime一起使用。查询为当前告警（status=0）时，不起作用
        """
        self.end_time = end_time

    def set_start_time(self, start_time):
        """
        :param start_time: 查询状态为告警历史（参数status=1）时的起始时间戳，  默认值：24小时前时间戳，startTime和endTime需同时传或同时不传。查询为当前告警（status=0）时，不起作用
        """
        self.start_time = start_time

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.status is None:
            raise Exception("status can not None")

