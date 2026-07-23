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


class GetBucketUsageChartRequest(CTYunRequest):
    """
    查询oss桶流量和请求次数
    """

    def __init__(self, request_param):
        super(GetBucketUsageChartRequest, self).__init__("/v4/oss/get-bucket-usage-chart", "GET", "zos", "")
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
        if self.parameters.select_field is not None:
            query_param["selectField"] = self.parameters.select_field
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetBucketUsageChartRequestParam(object):

    def __init__(self, region_id, select_field, start_time=None, end_time=None):
        """
        :param region_id: 资源池id
        :param start_time: 开始时间(时间戳形式)，不传默认为一个月（前30天）,startTime和endTime需要同时传才生效
        :param end_time: 结束时间(时间戳形式)，不传默认为一个月（前30天），startTime和endTime需要同时传才生效
        :param select_field: 查询维度 bytes_send  总上传量(B)   
             out_bytes_send  外部上传量(B)   
             inner_bytes_send  内部上传量(B)   
             bytes_received  总下载量(B)   
             out_received  外部下载量(暂不支持)   
             inner_received  内部下载量（暂不支持）   
             standard_ops  标准存储请求量   
             ia_ops  低频存储请求量   
             glacier_ops  归档存储请求量   
             all_ops 所有请求量
        """
        self.region_id = region_id
        self.start_time = start_time
        self.end_time = end_time
        self.select_field = select_field

    def set_start_time(self, start_time):
        """
        :param start_time: 开始时间(时间戳形式)，不传默认为一个月（前30天）,startTime和endTime需要同时传才生效
        """
        self.start_time = start_time

    def set_end_time(self, end_time):
        """
        :param end_time: 结束时间(时间戳形式)，不传默认为一个月（前30天），startTime和endTime需要同时传才生效
        """
        self.end_time = end_time

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.select_field is None:
            raise Exception("select_field can not None")

