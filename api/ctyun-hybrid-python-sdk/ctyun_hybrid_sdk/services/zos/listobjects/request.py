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


class ListObjectsRequest(CTYunRequest):
    """
    开发未对齐原因：v1版本只实现了/v4/oss/list-objects接口对应了公有云的/v4/oss/list-object-versions接口功能，   
    v2版本和公有云对齐开发两个接口，该接口取消deleteMarkers字段接口和contents中isLatest、versionID字段，需要此信息请使用/v4/oss/list-object-versions接口
    """

    def __init__(self, request_param):
        super(ListObjectsRequest, self).__init__("/v4/oss/list-objects", "GET", "zos", "")
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
        if self.parameters.prefix is not None:
            query_param["prefix"] = self.parameters.prefix
        if self.parameters.marker is not None:
            query_param["marker"] = self.parameters.marker
        if self.parameters.max_keys is not None:
            query_param["maxKeys"] = self.parameters.max_keys
        if self.parameters.delimiter is not None:
            query_param["delimiter"] = self.parameters.delimiter
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListObjectsRequestParam(object):

    def __init__(self, region_id, bucket, prefix=None, marker=None, max_keys=None, delimiter=None):
        """
        :param region_id: 资源池id
        :param bucket: bucket名称
        :param prefix: 对象前缀检索
        :param marker: 起始对象键标记
        :param max_keys: 单次 ListObject 请求返回最大的条目数量
        :param delimiter: 定界符是您用来对键进行分组的字符
        """
        self.region_id = region_id
        self.bucket = bucket
        self.prefix = prefix
        self.marker = marker
        self.max_keys = max_keys
        self.delimiter = delimiter

    def set_prefix(self, prefix):
        """
        :param prefix: 对象前缀检索
        """
        self.prefix = prefix

    def set_marker(self, marker):
        """
        :param marker: 起始对象键标记
        """
        self.marker = marker

    def set_max_keys(self, max_keys):
        """
        :param max_keys: 单次 ListObject 请求返回最大的条目数量
        """
        self.max_keys = max_keys

    def set_delimiter(self, delimiter):
        """
        :param delimiter: 定界符是您用来对键进行分组的字符
        """
        self.delimiter = delimiter

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")

