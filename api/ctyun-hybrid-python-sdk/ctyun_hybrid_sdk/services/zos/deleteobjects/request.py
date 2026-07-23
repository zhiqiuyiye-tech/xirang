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


class DeleteObjectsRequest(CTYunRequest):
    """
    versionID不带版本的传"null"，带版本的传版本id才会真正的删除掉
    """

    def __init__(self, request_param):
        super(DeleteObjectsRequest, self).__init__("/v4/oss/delete-objects", "POST", "zos", "application/json")
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
        if self.parameters.delete is not None:
            if type(self.parameters.delete) is dict:
                delete_dict_value = self.parameters.delete
            else:
                delete_dict_value = self.parameters.delete.get_dic()
            body_param["delete"] = delete_dict_value
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


class Delete(object):

    def __init__(self, objects, quiet=None):
        """
        :param objects: 对象的数组
        :param quiet: 静默模式，默认 False。若为 true， 则响应不会返回每个对象的删除结果，仅返回失败的结果
        """
        self.objects = objects
        self.quiet = quiet
        self.check_param()

    def set_quiet(self, quiet):
        """
        :param quiet: 静默模式，默认 False。若为 true， 则响应不会返回每个对象的删除结果，仅返回失败的结果
        """
        self.quiet = quiet

    def get_dic(self):
        obj_dict = dict()
        if self.objects is not None:
            objects_array = []
            for item in self.objects:
                if type(item) is dict:
                    objects_array.append(item)
                else:
                    objects_array.append(item.get_dic())
            obj_dict["objects"] = objects_array
        if self.quiet is not None:
            obj_dict["quiet"] = self.quiet
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.objects is None:
            raise Exception("objects can not None")


class ObjectValue(object):

    def __init__(self, key, version_id=None):
        """
        :param key: 对象名
        :param version_id: verionID（versionID不带版本的传"null"，带版本的传版本id才会真正的删除掉），桶未开启版本控制，不传此版本ID会删除没有版本id及版本id为null的对象
        """
        self.key = key
        self.version_id = version_id
        self.check_param()

    def set_version_id(self, version_id):
        """
        :param version_id: verionID（versionID不带版本的传"null"，带版本的传版本id才会真正的删除掉），桶未开启版本控制，不传此版本ID会删除没有版本id及版本id为null的对象
        """
        self.version_id = version_id

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.version_id is not None:
            obj_dict["versionID"] = self.version_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.key is None:
            raise Exception("key can not None")


class DeleteObjectsRequestParam(object):

    def __init__(self, bucket, region_id, delete, ):
        """
        :param bucket: 存储空间名
        :param region_id: 资源池
        :param delete: 要删除的对象
        """
        self.bucket = bucket
        self.region_id = region_id
        self.delete = delete

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.delete is None:
            raise Exception("delete can not None")

