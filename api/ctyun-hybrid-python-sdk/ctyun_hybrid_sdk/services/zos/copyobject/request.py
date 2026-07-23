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


class CopyObjectRequest(CTYunRequest):
    """
    复制对象(拷贝文件到其它桶)
    """

    def __init__(self, request_param):
        super(CopyObjectRequest, self).__init__("/v4/oss/copy-object", "POST", "zos", "application/json")
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
        if self.parameters.copy_source is not None:
            if type(self.parameters.copy_source) is dict:
                copy_source_dict_value = self.parameters.copy_source
            else:
                copy_source_dict_value = self.parameters.copy_source.get_dic()
            body_param["copySource"] = copy_source_dict_value
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


class CopySource(object):

    def __init__(self, bucket, key, version_id=None):
        """
        :param bucket: 源存储空间名
        :param key: 源对象名
        :param version_id: 源对象版本号
        """
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.check_param()

    def set_version_id(self, version_id):
        """
        :param version_id: 源对象版本号
        """
        self.version_id = version_id

    def get_dic(self):
        obj_dict = dict()
        if self.bucket is not None:
            obj_dict["bucket"] = self.bucket
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.version_id is not None:
            obj_dict["versionID"] = self.version_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.key is None:
            raise Exception("key can not None")


class CopyObjectRequestParam(object):

    def __init__(self, bucket, region_id, key, copy_source, ):
        """
        :param bucket: 目标存储空间名
        :param region_id: 区域 ID
        :param key: 目标对象名
        :param copy_source: 源文件信息
        """
        self.bucket = bucket
        self.region_id = region_id
        self.key = key
        self.copy_source = copy_source

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
        if self.copy_source is None:
            raise Exception("copy_source can not None")

