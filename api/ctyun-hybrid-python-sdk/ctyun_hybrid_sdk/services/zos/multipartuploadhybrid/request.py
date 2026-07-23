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


class MultipartUploadHybridRequest(CTYunRequest):
    """
    该接口用于实现分片上传操作中片段的上传。   
       
    在上传任何一个分片之前，必须执行Initial Multipart Upload操作来初始化分片上传操作，初始化成功后，OOS会返回一个上传ID，这是一个唯一的标识，用户必须在调用Upload Part接口时加入该ID。   
       
    分片号PartNumber可以唯一标识一个片段并且定义该分片在对象中的位置，范围从1到10000。如果用户用之前上传过的片段的分片号来上传新的分片，之前的分片将会被覆盖。   
       
    除了最后一个分片外，所有分片的都不小于5M，最后一个分片的大小不受限制。   
       
    为了确保数据不会由于网络传输而毁坏，需要在每个分片上传请求中指定Content-MD5头，OOS通过提供的Content-MD5值来检查数据的完整性，如果不匹配，则会返回一个错误信息。   
       
    与V1暂未对齐，V1中body使用string类型，V2使用文件流上传[form-data格式]
    """

    def __init__(self, request_param):
        super(MultipartUploadHybridRequest, self).__init__("/v4/oss/action-multipart-upload", "POST", "zos", "multipart/form-data")
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
        if self.parameters.part_number is not None:
            body_param["partNumber"] = self.parameters.part_number
        if self.parameters.body is not None:
            body_param["body"] = self.parameters.body
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


class MultipartUploadHybridRequestParam(object):

    def __init__(self, region_id, bucket, key, upload_id, part_number, body, ):
        """
        :param region_id: 资源池ID
        :param bucket: 桶名称
        :param key: 对象名
        :param upload_id: 分段上传的ID
        :param part_number: 当前分段上传的编号
        :param body: 要上传的文件数据，文件流
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.part_number = part_number
        self.body = body

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
        if self.part_number is None:
            raise Exception("part_number can not None")
        if self.body is None:
            raise Exception("body can not None")

