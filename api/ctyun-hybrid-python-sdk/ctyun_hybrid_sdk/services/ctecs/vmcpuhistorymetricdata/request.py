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


class VmCpuHistoryMetricDataRequest(CTYunRequest):
    """
    该接口不推荐使用。建议使用-->历史监控数据：云主机(/v4.1/monitor/query-vm-historymetricdata)
    """

    def __init__(self, request_param):
        super(VmCpuHistoryMetricDataRequest, self).__init__("/v4/ecs/vm-cpu-history-metric-data", "POST", "ctecs", "application/json")
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
        if self.parameters.device_id_list is not None:
            body_param["deviceIDList"] = self.parameters.device_id_list
        if self.parameters.period is not None:
            body_param["period"] = self.parameters.period
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class VmCpuHistoryMetricDataRequestParam(object):

    def __init__(self, region_id, device_id_list, start_time, end_time, period=None, page=None, page_size=None):
        """
        :param region_id: 资源池id
        :param device_id_list: 云主机ID(建议:设备数不大于20) 注意:此参数为数组
        :param period: 可选参数，聚合周期，单位：秒。传空时,默认300
        :param start_time: 查询起始时间戳(秒)
        :param end_time: 查询结束时间戳(秒)
        :param page: 页码，0或不传默认值:1，小于0时报错
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.region_id = region_id
        self.device_id_list = device_id_list
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.page = page
        self.page_size = page_size

    def set_period(self, period):
        """
        :param period: 可选参数，聚合周期，单位：秒。传空时,默认300
        """
        self.period = period

    def set_page(self, page):
        """
        :param page: 页码，0或不传默认值:1，小于0时报错
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_id_list is None:
            raise Exception("device_id_list can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

