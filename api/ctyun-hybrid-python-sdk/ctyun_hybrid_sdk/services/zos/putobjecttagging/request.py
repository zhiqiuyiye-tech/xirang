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


class PutObjectTaggingRequest(CTYunRequest):
    """
    设置或更新对象（Object）的标签（Tagging）信息
    """

    def __init__(self, request_param):
        super(PutObjectTaggingRequest, self).__init__("/v4/oss/put-object-tagging", "POST", "zos", "application/json")
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
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.version_id is not None:
            body_param["versionID"] = self.parameters.version_id
        if self.parameters.tagging is not None:
            if type(self.parameters.tagging) is dict:
                tagging_dict_value = self.parameters.tagging
            else:
                tagging_dict_value = self.parameters.tagging.get_dic()
            body_param["tagging"] = tagging_dict_value
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


class Tagging(object):

    def __init__(self, tag_set, ):
        """
        :param tag_set: 标签集
        """
        self.tag_set = tag_set
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.tag_set is not None:
            tag_set_array = []
            for item in self.tag_set:
                if type(item) is dict:
                    tag_set_array.append(item)
                else:
                    tag_set_array.append(item.get_dic())
            obj_dict["tagSet"] = tag_set_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.tag_set is None:
            raise Exception("tag_set can not None")


class TagSet(object):

    def __init__(self, key, value, ):
        """
        :param key: 长度为2-63个字符；支持中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)；不支持连续连字符（--）。
        :param value: 长度为2-63个字符；支持中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)；不支持连续连字符（--）。
        """
        self.key = key
        self.value = value
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.value is not None:
            obj_dict["value"] = self.value
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.key is None:
            raise Exception("key can not None")
        if self.value is None:
            raise Exception("value can not None")


class PutObjectTaggingRequestParam(object):

    def __init__(self, region_id, key, bucket, tagging, version_id=None):
        """
        :param region_id: 资源池id
        :param key: 对象名
        :param bucket: 桶名称
        :param version_id: 多版本场景下，指定对象的特定版本
        :param tagging: 标签集
        """
        self.region_id = region_id
        self.key = key
        self.bucket = bucket
        self.version_id = version_id
        self.tagging = tagging

    def set_version_id(self, version_id):
        """
        :param version_id: 多版本场景下，指定对象的特定版本
        """
        self.version_id = version_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key is None:
            raise Exception("key can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.tagging is None:
            raise Exception("tagging can not None")

