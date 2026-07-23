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


class QueryMetricDataMaxHybridRequest(CTYunRequest):
    """
    查询某个设备的历史数据，以period为周期，返回每个周期内的最大值
    """

    def __init__(self, request_param):
        super(QueryMetricDataMaxHybridRequest, self).__init__("/v4/monitor/query-metricdata-max", "POST", "monitor", "application/json")
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
        if self.parameters.device_type is not None:
            body_param["deviceType"] = self.parameters.device_type
        if self.parameters.item_name_list is not None:
            body_param["itemNameList"] = self.parameters.item_name_list
        if self.parameters.device_uuid_list is not None:
            body_param["deviceUUIDList"] = self.parameters.device_uuid_list
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.period is not None:
            body_param["period"] = self.parameters.period
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


class QueryMetricDataMaxHybridRequestParam(object):

    def __init__(self, region_id, device_type, item_name_list, device_uuid_list, start_time, end_time, page_no=None, page_size=None, period=None):
        """
        :param region_id: 资源池ID
        :param device_type: 本参数表示设备类型。取值范围：vm：云主机。bare_metal：裸金属。disk：云磁盘。scaling：弹性伸缩。traffic：共享带宽。eip：弹性IP。elb：负载均衡。listener：监听器。cstor_sfs：弹性文件。
        :param item_name_list: 待查的监控项名称 注意:此参数为数组
        :param device_uuid_list: 查询设备ID列表   注：弹性IP设备ID传IP地址(例:100.127.176.100) 注意:此参数为数组
        :param start_time: 查询起始时间戳
        :param end_time: 查询结束时间戳
        :param page_no: 页码，0或不传默认值:1，小于0时报错
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        :param period: 聚合周期，单位：秒，默认300
        """
        self.region_id = region_id
        self.device_type = device_type
        self.item_name_list = item_name_list
        self.device_uuid_list = device_uuid_list
        self.start_time = start_time
        self.end_time = end_time
        self.page_no = page_no
        self.page_size = page_size
        self.period = period

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，0或不传默认值:1，小于0时报错
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def set_period(self, period):
        """
        :param period: 聚合周期，单位：秒，默认300
        """
        self.period = period

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_type is None:
            raise Exception("device_type can not None")
        if self.item_name_list is None:
            raise Exception("item_name_list can not None")
        if self.device_uuid_list is None:
            raise Exception("device_uuid_list can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

