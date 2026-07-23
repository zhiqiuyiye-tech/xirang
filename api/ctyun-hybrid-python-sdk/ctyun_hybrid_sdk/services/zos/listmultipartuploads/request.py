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


class ListMultipartUploadsRequest(CTYunRequest):
    """
    查询正在进行中的分段上传
    """

    def __init__(self, request_param):
        super(ListMultipartUploadsRequest, self).__init__("/v4/oss/list-multipart-uploads", "GET", "zos", "")
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
        if self.parameters.key_marker is not None:
            query_param["keyMarker"] = self.parameters.key_marker
        if self.parameters.prefix is not None:
            query_param["prefix"] = self.parameters.prefix
        if self.parameters.max_uploads is not None:
            query_param["maxUploads"] = self.parameters.max_uploads
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListMultipartUploadsRequestParam(object):

    def __init__(self, region_id, bucket, key_marker=None, prefix=None, max_uploads=None):
        """
        :param region_id: 资源池ID
        :param bucket: 桶名称
        :param key_marker: 只有Key大于KeyMarker的分段上传数据才会返回
        :param prefix: Key的前缀，只有以Prefix为开头的Key才会被返回
        :param max_uploads: 单次最多返回的分段上传数据，大小是1-1000，超过1000的数据会被视为1000
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key_marker = key_marker
        self.prefix = prefix
        self.max_uploads = max_uploads

    def set_key_marker(self, key_marker):
        """
        :param key_marker: 只有Key大于KeyMarker的分段上传数据才会返回
        """
        self.key_marker = key_marker

    def set_prefix(self, prefix):
        """
        :param prefix: Key的前缀，只有以Prefix为开头的Key才会被返回
        """
        self.prefix = prefix

    def set_max_uploads(self, max_uploads):
        """
        :param max_uploads: 单次最多返回的分段上传数据，大小是1-1000，超过1000的数据会被视为1000
        """
        self.max_uploads = max_uploads

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")

