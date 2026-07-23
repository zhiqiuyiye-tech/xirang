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


class GetBucketReplicationRequest(CTYunRequest):
    """
    查询存储空间复制规则
    """

    def __init__(self, request_param):
        super(GetBucketReplicationRequest, self).__init__("/v4/oss/get-bucket-replication", "GET", "zos", "")
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
        if self.parameters.bucket is not None:
            query_param["bucket"] = self.parameters.bucket
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetBucketReplicationRequestParam(object):

    def __init__(self, region_id, bucket, ):
        """
        :param region_id: 资源池id
        :param bucket: bucket名称
        """
        self.region_id = region_id
        self.bucket = bucket

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")

