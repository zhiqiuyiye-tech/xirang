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


class GetBucketUsageRequest(CTYunRequest):
    """
    查询oss桶使用量
    """

    def __init__(self, request_param):
        super(GetBucketUsageRequest, self).__init__("/v4/oss/get-bucket-usage", "GET", "zos", "")
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
        if self.parameters.start is not None:
            query_param["start"] = self.parameters.start
        if self.parameters.end is not None:
            query_param["end"] = self.parameters.end
        if self.parameters.bucket is not None:
            query_param["bucket"] = self.parameters.bucket
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetBucketUsageRequestParam(object):

    def __init__(self, region_id, start, end, bucket=None):
        """
        :param region_id: 资源池id
        :param start: 开始时间 UTC时间：2020-09-20T10:00:00Z
        :param end: 结束时间 UTC时间：2020-09-20T10:00:00Z
        :param bucket: 桶名
        """
        self.region_id = region_id
        self.start = start
        self.end = end
        self.bucket = bucket

    def set_bucket(self, bucket):
        """
        :param bucket: 桶名
        """
        self.bucket = bucket

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.start is None:
            raise Exception("start can not None")
        if self.end is None:
            raise Exception("end can not None")

