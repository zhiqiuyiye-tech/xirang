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


class CopyMultipartUploadHybridRequest(CTYunRequest):
    """
    可以将已经存在的Object作为分段上传的片段，拷贝生成一个新的片段。UploadId为新对象的分片上传ID。在上传任何一个分片之前，必须执行create-multipart-upload操作来初始化分片上传操作，初始化成功后，OOS会返回一个上传ID，这是一个唯一的标识，用户必须在调用Copy Part接口时加入该ID。   
       
    开发未对齐原因：公有云没有该接口，按照py接口开发的
    """

    def __init__(self, request_param):
        super(CopyMultipartUploadHybridRequest, self).__init__("/v4/oss/copy-multipart-upload", "POST", "zos", "application/json")
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
        if self.parameters.copy_source is not None:
            if type(self.parameters.copy_source) is dict:
                copy_source_dict_value = self.parameters.copy_source
            else:
                copy_source_dict_value = self.parameters.copy_source.get_dic()
            body_param["copySource"] = copy_source_dict_value
        if self.parameters.part_number is not None:
            body_param["partNumber"] = self.parameters.part_number
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
        :param bucket: 复制的桶
        :param key: 复制的文件
        :param version_id: 版本id
        """
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.check_param()

    def set_version_id(self, version_id):
        """
        :param version_id: 版本id
        """
        self.version_id = version_id

    def get_dic(self):
        obj_dict = dict()
        if self.bucket is not None:
            obj_dict["bucket"] = self.bucket
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.version_id is not None:
            obj_dict["versionId"] = self.version_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.key is None:
            raise Exception("key can not None")


class CopyMultipartUploadHybridRequestParam(object):

    def __init__(self, region_id, bucket, key, upload_id, copy_source, part_number, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 对象名
        :param upload_id: 分段上传的ID
        :param copy_source: 复制的桶的源
        :param part_number: 复制的序号
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.copy_source = copy_source
        self.part_number = part_number

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
        if self.copy_source is None:
            raise Exception("copy_source can not None")
        if self.part_number is None:
            raise Exception("part_number can not None")

