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


class GetBucketStatisticsRequest(CTYunRequest):
    """
    查询桶统计信息
    """

    def __init__(self, request_param):
        super(GetBucketStatisticsRequest, self).__init__("/v4/oss/get-bucket-statistics", "GET", "zos", "")
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
        if self.parameters.bucket is not None:
            query_param["bucket"] = self.parameters.bucket
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


class GetBucketStatisticsRequestParam(object):

    def __init__(self, region_id, start_time, end_time, bucket=None):
        """
        :param bucket: 存储桶名	
        :param region_id: 区域ID	
        :param start_time: 日期-小时 格式的时间字符串，时区为 UTC 时区	
        :param end_time: 日期-小时 格式的时间字符串，时区为 UTC 时区	
        """
        self.bucket = bucket
        self.region_id = region_id
        self.start_time = start_time
        self.end_time = end_time

    def set_bucket(self, bucket):
        """
        :param bucket: 存储桶名	
        """
        self.bucket = bucket

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

