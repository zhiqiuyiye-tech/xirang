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


class PutObjectHeaderRequest(CTYunRequest):
    """
    与公有云对齐，未与v1对齐：v1包含参数versionID，但实现逻辑为通过copy对象为新的对象修改header,无法对历史版本对象修改http头
    """

    def __init__(self, request_param):
        super(PutObjectHeaderRequest, self).__init__("/v4/oss/put-object-header", "POST", "zos", "application/json")
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
        if self.parameters.headers is not None:
            if type(self.parameters.headers) is dict:
                headers_dict_value = self.parameters.headers
            else:
                headers_dict_value = self.parameters.headers.get_dic()
            body_param["headers"] = headers_dict_value
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


class Headers(object):

    def __init__(self, content_encoding=None, cache_control=None, content_language=None, content_type=None, content_disposition=None):
        """
        :param content_encoding: 内容编码格式
        :param cache_control: 缓存指令
        :param content_language: 内容编码语言
        :param content_type: 内容类型
        :param content_disposition: 指示如何处理响应内容
        """
        self.content_encoding = content_encoding
        self.cache_control = cache_control
        self.content_language = content_language
        self.content_type = content_type
        self.content_disposition = content_disposition

    def set_content_encoding(self, content_encoding):
        """
        :param content_encoding: 内容编码格式
        """
        self.content_encoding = content_encoding

    def set_cache_control(self, cache_control):
        """
        :param cache_control: 缓存指令
        """
        self.cache_control = cache_control

    def set_content_language(self, content_language):
        """
        :param content_language: 内容编码语言
        """
        self.content_language = content_language

    def set_content_type(self, content_type):
        """
        :param content_type: 内容类型
        """
        self.content_type = content_type

    def set_content_disposition(self, content_disposition):
        """
        :param content_disposition: 指示如何处理响应内容
        """
        self.content_disposition = content_disposition

    def get_dic(self):
        obj_dict = dict()
        if self.content_encoding is not None:
            obj_dict["ContentEncoding"] = self.content_encoding
        if self.cache_control is not None:
            obj_dict["CacheControl"] = self.cache_control
        if self.content_language is not None:
            obj_dict["ContentLanguage"] = self.content_language
        if self.content_type is not None:
            obj_dict["ContentType"] = self.content_type
        if self.content_disposition is not None:
            obj_dict["ContentDisposition"] = self.content_disposition
        return obj_dict


class PutObjectHeaderRequestParam(object):

    def __init__(self, region_id, bucket, key, headers=None):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 对象名
        :param headers: HTTP头，仅限于 CacheControl, ContentDisposition, ContentEncoding, ContentLanguage, ContentType 五种
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.headers = headers

    def set_headers(self, headers):
        """
        :param headers: HTTP头，仅限于 CacheControl, ContentDisposition, ContentEncoding, ContentLanguage, ContentType 五种
        """
        self.headers = headers

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

