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


class UnfreezeObjectRequest(CTYunRequest):
    """
    只有归档对象才可解冻
    """

    def __init__(self, request_param):
        super(UnfreezeObjectRequest, self).__init__("/v4/oss/unfreeze-object", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
        if self.parameters.version_id is not None:
            body_param["versionID"] = self.parameters.version_id
        if self.parameters.days is not None:
            body_param["days"] = self.parameters.days
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


class UnfreezeObjectRequestParam(object):

    def __init__(self, bucket, region_id, key, days, version_id=None):
        """
        :param bucket: 桶名	
        :param region_id: 区域 ID	
        :param key: 需要解冻的对象名称	
        :param version_id: 对象版本号	
        :param days: 解冻天数(范围：1~31)	
        """
        self.bucket = bucket
        self.region_id = region_id
        self.key = key
        self.version_id = version_id
        self.days = days

    def set_version_id(self, version_id):
        """
        :param version_id: 对象版本号	
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
        if self.days is None:
            raise Exception("days can not None")

