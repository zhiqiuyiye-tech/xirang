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


class CompleteMultipartUploadRequest(CTYunRequest):
    """
    接口通过合并之前的上传片段来完成一次分片上传过程。    
       
    用户首先初始化分片上传过程，然后通过Upload Part接口上传所有分片。在成功将一次分片上传过程的所有相关片段上传之后，调用这个接口来结束分片上传过程。当收到这个请求的时候，OOS会以分片号升序排列的方式将所有片段依次拼接来创建一个新的对象。在这个Complete Multipart Upload请求中，用户需要提供一个片段列表。同时，必须确保这个片段列表中的所有片段必须是已经上传完成的，Complete Multipart Upload操作会将片段列表中提供的片段拼接起来。对片段列表中的每个片段，需要提供该片段上传完成时返回的ETag头的值和对应的分片号。   
       
     OOS提供了不合并片段也可以读取Object内容的功能。在没有调用Complete Multipart Upload接口合并片段时，也可以通过调用Get Object接口来获取文件内容，OOS会根据最近一次创建的uploadId，以分片号升序的方式顺序读取片段内容，返回给客户端。
    """

    def __init__(self, request_param):
        super(CompleteMultipartUploadRequest, self).__init__("/v4/oss/complete-multipart-upload", "POST", "zos", "application/json")
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
        if self.parameters.multipart_upload is not None:
            if type(self.parameters.multipart_upload) is dict:
                multipart_upload_dict_value = self.parameters.multipart_upload
            else:
                multipart_upload_dict_value = self.parameters.multipart_upload.get_dic()
            body_param["multipartUpload"] = multipart_upload_dict_value
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


class MultipartUpload(object):

    def __init__(self, parts=None):
        """
        :param parts: 分段信息
        """
        self.parts = parts

    def set_parts(self, parts):
        """
        :param parts: 分段信息
        """
        self.parts = parts

    def get_dic(self):
        obj_dict = dict()
        if self.parts is not None:
            parts_array = []
            for item in self.parts:
                if type(item) is dict:
                    parts_array.append(item)
                else:
                    parts_array.append(item.get_dic())
            obj_dict["parts"] = parts_array
        return obj_dict


class Part(object):

    def __init__(self, e_tag, part_number, checksum_crc32=None, checksum_crc32c=None, checksum_sha1=None, checksum_sha256=None):
        """
        :param e_tag: 一块数据上传完毕后，服务器端返回的 Entity tag
        :param part_number: 分块序号，1 到10,000
        :param checksum_crc32: CRC32 摘要信息
        :param checksum_crc32c: CRC32C 摘要信息
        :param checksum_sha1: SHA1 摘要信息
        :param checksum_sha256: SHA256 摘要信息
        """
        self.e_tag = e_tag
        self.part_number = part_number
        self.checksum_crc32 = checksum_crc32
        self.checksum_crc32c = checksum_crc32c
        self.checksum_sha1 = checksum_sha1
        self.checksum_sha256 = checksum_sha256
        self.check_param()

    def set_checksum_crc32(self, checksum_crc32):
        """
        :param checksum_crc32: CRC32 摘要信息
        """
        self.checksum_crc32 = checksum_crc32

    def set_checksum_crc32c(self, checksum_crc32c):
        """
        :param checksum_crc32c: CRC32C 摘要信息
        """
        self.checksum_crc32c = checksum_crc32c

    def set_checksum_sha1(self, checksum_sha1):
        """
        :param checksum_sha1: SHA1 摘要信息
        """
        self.checksum_sha1 = checksum_sha1

    def set_checksum_sha256(self, checksum_sha256):
        """
        :param checksum_sha256: SHA256 摘要信息
        """
        self.checksum_sha256 = checksum_sha256

    def get_dic(self):
        obj_dict = dict()
        if self.e_tag is not None:
            obj_dict["ETag"] = self.e_tag
        if self.part_number is not None:
            obj_dict["partNumber"] = self.part_number
        if self.checksum_crc32 is not None:
            obj_dict["checksumCRC32"] = self.checksum_crc32
        if self.checksum_crc32c is not None:
            obj_dict["checksumCRC32C"] = self.checksum_crc32c
        if self.checksum_sha1 is not None:
            obj_dict["checksumSHA1"] = self.checksum_sha1
        if self.checksum_sha256 is not None:
            obj_dict["checksumSHA256"] = self.checksum_sha256
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.e_tag is None:
            raise Exception("e_tag can not None")
        if self.part_number is None:
            raise Exception("part_number can not None")


class CompleteMultipartUploadRequestParam(object):

    def __init__(self, region_id, bucket, key, upload_id, multipart_upload, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 文件key
        :param upload_id: 分段上传的ID
        :param multipart_upload: 所有成功上传的分段的分段信息
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.multipart_upload = multipart_upload

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
        if self.multipart_upload is None:
            raise Exception("multipart_upload can not None")

