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


class GetObjectRetentionRequest(CTYunRequest):
    """
    获取对象合规保留配置
    """

    def __init__(self, request_param):
        super(GetObjectRetentionRequest, self).__init__("/v4/oss/get-object-retention", "GET", "zos", "")
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
        if self.parameters.key is not None:
            query_param["key"] = self.parameters.key
        if self.parameters.version_id is not None:
            query_param["versionID"] = self.parameters.version_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetObjectRetentionRequestParam(object):

    def __init__(self, bucket, region_id, key, version_id=None):
        """
        :param bucket: 桶名	
        :param region_id: 区域 ID	
        :param key: 对象名称	
        :param version_id: 版本ID，在开启多版本时可使用	
        """
        self.bucket = bucket
        self.region_id = region_id
        self.key = key
        self.version_id = version_id

    def set_version_id(self, version_id):
        """
        :param version_id: 版本ID，在开启多版本时可使用	
        """
        self.version_id = version_id

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key is None:
            raise Exception("key can not None")

