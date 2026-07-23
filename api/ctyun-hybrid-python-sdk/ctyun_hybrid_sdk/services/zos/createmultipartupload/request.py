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


class CreateMultipartUploadRequest(CTYunRequest):
    """
    实现初始化分片上传，成功执行此请求以后会返回 Upload ID 用于后续的分块上传
    """

    def __init__(self, request_param):
        super(CreateMultipartUploadRequest, self).__init__("/v4/oss/create-multipart-upload", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
        if self.parameters.acl is not None:
            body_param["ACL"] = self.parameters.acl
        if self.parameters.storage_class is not None:
            body_param["storageClass"] = self.parameters.storage_class
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


class CreateMultipartUploadRequestParam(object):

    def __init__(self, region_id, bucket, key, acl, storage_class=None):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 文件key
        :param acl: ACL, 可选的有 private, public-read, public-read-write, authenticated-read
        :param storage_class: 存储类，可选的有 STANDARD, STANDARD_IA, GLACIER
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.acl = acl
        self.storage_class = storage_class

    def set_storage_class(self, storage_class):
        """
        :param storage_class: 存储类，可选的有 STANDARD, STANDARD_IA, GLACIER
        """
        self.storage_class = storage_class

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.key is None:
            raise Exception("key can not None")
        if self.acl is None:
            raise Exception("acl can not None")

