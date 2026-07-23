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


class PutBucketQuotaRequest(CTYunRequest):
    """
    对桶配额进行修改。
    """

    def __init__(self, request_param):
        super(PutBucketQuotaRequest, self).__init__("/v4/oss/put-bucket-quota", "POST", "zos", "application/json")
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
        if self.parameters.enabled is not None:
            body_param["enabled"] = self.parameters.enabled
        if self.parameters.max_size_kb is not None:
            body_param["maxSizeKb"] = self.parameters.max_size_kb
        if self.parameters.max_objects is not None:
            body_param["maxObjects"] = self.parameters.max_objects
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


class PutBucketQuotaRequestParam(object):

    def __init__(self, bucket, region_id, enabled=None, max_size_kb=None, max_objects=None):
        """
        :param bucket: 桶名
        :param region_id: 资源池ID
        :param enabled: 是否开启配额限制，默认值为false，值为true时maxSizeKb和maxObjects至少一个大于等于0
        :param max_size_kb: 最大的size容量(单位KB)，传入小于0或不传值均为无限制，开启配额时maxSizeKb和maxObjects有一个需要大于0
        :param max_objects: 最大的objects数量，传入小于0或不传值均为无限制，开启配额时maxSizeKb和maxObjects有一个需要大于0
        """
        self.bucket = bucket
        self.region_id = region_id
        self.enabled = enabled
        self.max_size_kb = max_size_kb
        self.max_objects = max_objects

    def set_enabled(self, enabled):
        """
        :param enabled: 是否开启配额限制，默认值为false，值为true时maxSizeKb和maxObjects至少一个大于等于0
        """
        self.enabled = enabled

    def set_max_size_kb(self, max_size_kb):
        """
        :param max_size_kb: 最大的size容量(单位KB)，传入小于0或不传值均为无限制，开启配额时maxSizeKb和maxObjects有一个需要大于0
        """
        self.max_size_kb = max_size_kb

    def set_max_objects(self, max_objects):
        """
        :param max_objects: 最大的objects数量，传入小于0或不传值均为无限制，开启配额时maxSizeKb和maxObjects有一个需要大于0
        """
        self.max_objects = max_objects

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

