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


class AbortMultipartUploadRequest(CTYunRequest):
    """
    用于取消MultipartUpload事件并删除对应的Part数据
    """

    def __init__(self, request_param):
        super(AbortMultipartUploadRequest, self).__init__("/v4/oss/abort-multipart-upload", "POST", "zos", "application/json")
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
        if self.parameters.upload_id is not None:
            body_param["uploadID"] = self.parameters.upload_id
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


class AbortMultipartUploadRequestParam(object):

    def __init__(self, region_id, bucket, key, upload_id, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 文件key
        :param upload_id: 分段上传的ID
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id

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
        if self.upload_id is None:
            raise Exception("upload_id can not None")

