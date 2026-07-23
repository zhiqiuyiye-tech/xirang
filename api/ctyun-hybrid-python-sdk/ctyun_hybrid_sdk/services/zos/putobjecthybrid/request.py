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


class PutObjectHybridRequest(CTYunRequest):
    """
    s3 sdk接口不支持append操作，append和appendPosition字段暂不生效   
    与V1暂未对齐，V1中body使用string类型，V2使用文件流上传[form-data格式]；V2 otherParams字段需要将object转为string，格式为：{"contentType": "utf-8"}
    """

    def __init__(self, request_param):
        super(PutObjectHybridRequest, self).__init__("/v4/oss/put-object", "POST", "zos", "multipart/form-data")
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
        if self.parameters.acl is not None:
            body_param["acl"] = self.parameters.acl
        if self.parameters.body is not None:
            body_param["body"] = self.parameters.body
        if self.parameters.other_params is not None:
            body_param["otherParams"] = self.parameters.other_params
        if self.parameters.append is not None:
            body_param["append"] = self.parameters.append
        if self.parameters.append_position is not None:
            body_param["appendPosition"] = self.parameters.append_position
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


class PutObjectHybridRequestParam(object):

    def __init__(self, region_id, bucket, key, acl=None, body=None, other_params=None, append=None, append_position=None):
        """
        :param region_id: 资源池ID
        :param bucket: 桶名称
        :param key: 文件key
        :param acl: Object的访问控制，默认private，private/public-read-write/public-read/authenticated-read
        :param body: 上传对象的内容，可以为文件流或字节流，不传递此参数默认为0字节内容
        :param other_params: 其他相关设置，按照json的k-v格式设置，可设置以下参数：   
         cacheControl string 缓存指令   
         contentDisposition string 文件名称   
         contentEncoding string 编码格式   
         contentLanguage string 编码语言   
         contentLength int32 用于描述HTTP消息体的传输大小   
         contentType string 编码格式   
         expires string 缓存内容的绝对过期时间   
         grantFullControl string 赋予指定账户对存储桶的读写权限   
         grantRead string 赋予指定账户对存储桶的读权限   
         serverSideEncryption string 服务器端加密规则   
         storageClass string 存储类型
        :param append: 是否以追加模式上传Object
        :param append_position: 追加模式下，指定追加的位置
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.acl = acl
        self.body = body
        self.other_params = other_params
        self.append = append
        self.append_position = append_position

    def set_acl(self, acl):
        """
        :param acl: Object的访问控制，默认private，private/public-read-write/public-read/authenticated-read
        """
        self.acl = acl

    def set_body(self, body):
        """
        :param body: 上传对象的内容，可以为文件流或字节流，不传递此参数默认为0字节内容
        """
        self.body = body

    def set_other_params(self, other_params):
        """
        :param other_params: 其他相关设置，按照json的k-v格式设置，可设置以下参数：   
         cacheControl string 缓存指令   
         contentDisposition string 文件名称   
         contentEncoding string 编码格式   
         contentLanguage string 编码语言   
         contentLength int32 用于描述HTTP消息体的传输大小   
         contentType string 编码格式   
         expires string 缓存内容的绝对过期时间   
         grantFullControl string 赋予指定账户对存储桶的读写权限   
         grantRead string 赋予指定账户对存储桶的读权限   
         serverSideEncryption string 服务器端加密规则   
         storageClass string 存储类型
        """
        self.other_params = other_params

    def set_append(self, append):
        """
        :param append: 是否以追加模式上传Object
        """
        self.append = append

    def set_append_position(self, append_position):
        """
        :param append_position: 追加模式下，指定追加的位置
        """
        self.append_position = append_position

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

