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


class PutBucketTaggingRequest(CTYunRequest):
    """
    设置存储空间标签
    """

    def __init__(self, request_param):
        super(PutBucketTaggingRequest, self).__init__("/v4/oss/put-bucket-tagging", "POST", "zos", "application/json")
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
        :param key: 标签key，长度不超过63
        :param value: 标签value，长度不超过255
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


class PutBucketTaggingRequestParam(object):

    def __init__(self, bucket, region_id, tagging, ):
        """
        :param bucket: 桶名称
        :param region_id: 资源池ID
        :param tagging: 标签集
        """
        self.bucket = bucket
        self.region_id = region_id
        self.tagging = tagging

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.tagging is None:
            raise Exception("tagging can not None")

