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


class V41describeScalingHistoryMetricDataRequest(CTYunRequest):
    """
    具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |内存使用率|mem_util|%|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|   
    |实例个数|instance_count|个|
    """

    def __init__(self, request_param):
        super(V41describeScalingHistoryMetricDataRequest, self).__init__("/v4.1/monitor/query-scaling-historymetricdata", "POST", "monitor", "application/json")
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
        if self.parameters.device_uuid_list is not None:
            body_param["deviceUUIDList"] = self.parameters.device_uuid_list
        if self.parameters.item_name_list is not None:
            body_param["itemNameList"] = self.parameters.item_name_list
        if self.parameters.period is not None:
            body_param["period"] = self.parameters.period
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
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


class V41describeScalingHistoryMetricDataRequestParam(object):

    def __init__(self, region_id, device_uuid_list, item_name_list, start_time, end_time, period=None):
        """
        :param region_id: 资源池ID
        :param device_uuid_list: 查询设备ID列表(建议:设备数不大于20，可以重复)注：弹性伸缩组只有一个ID 注意:此参数为数组
        :param item_name_list: 监控项指标(调用监控项列表查询接口/v4/monitor/query-monitor-items获取。相同指标只返回一次。建议:指标数不超过50个) 注意:此参数为数组
        :param period: 可选参数，聚合周期，单位：秒。传空时,默认300
        :param start_time: 查询起始时间戳(秒)
        :param end_time: 查询结束时间戳(秒)
        """
        self.region_id = region_id
        self.device_uuid_list = device_uuid_list
        self.item_name_list = item_name_list
        self.period = period
        self.start_time = start_time
        self.end_time = end_time

    def set_period(self, period):
        """
        :param period: 可选参数，聚合周期，单位：秒。传空时,默认300
        """
        self.period = period

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_uuid_list is None:
            raise Exception("device_uuid_list can not None")
        if self.item_name_list is None:
            raise Exception("item_name_list can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

