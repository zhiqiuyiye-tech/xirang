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


class ListPartsRequest(CTYunRequest):
    """
    查询特定分段上传中的已上传的分段的信息
    """

    def __init__(self, request_param):
        super(ListPartsRequest, self).__init__("/v4/oss/list-parts", "GET", "zos", "")
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
        if self.parameters.key is not None:
            query_param["key"] = self.parameters.key
        if self.parameters.max_parts is not None:
            query_param["maxParts"] = self.parameters.max_parts
        if self.parameters.part_number_marker is not None:
            query_param["partNumberMarker"] = self.parameters.part_number_marker
        if self.parameters.upload_id is not None:
            query_param["uploadID"] = self.parameters.upload_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListPartsRequestParam(object):

    def __init__(self, region_id, bucket, key, upload_id, max_parts=None, part_number_marker=None):
        """
        :param region_id: 资源池id
        :param bucket: bucket名称
        :param key: 文件名称
        :param max_parts: 最多返回的分段数目
        :param part_number_marker: list的分段编号的起始编号，只有分段编号大于这个数字的分段信息才会返回
        :param upload_id: 分段上传的ID
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.max_parts = max_parts
        self.part_number_marker = part_number_marker
        self.upload_id = upload_id

    def set_max_parts(self, max_parts):
        """
        :param max_parts: 最多返回的分段数目
        """
        self.max_parts = max_parts

    def set_part_number_marker(self, part_number_marker):
        """
        :param part_number_marker: list的分段编号的起始编号，只有分段编号大于这个数字的分段信息才会返回
        """
        self.part_number_marker = part_number_marker

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

