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


class ExportPrivateImageRequest(CTYunRequest):
    """
    导出私有镜像   
    开发未对齐原因：混合云返回镜像链接，公有云无返回参数   
    首次是导出下发，导出成功后会返回正常url
    """

    def __init__(self, request_param):
        super(ExportPrivateImageRequest, self).__init__("/v4/image/export", "POST", "ctimage", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.attr is not None:
            if type(self.parameters.attr) is dict:
                attr_dict_value = self.parameters.attr
            else:
                attr_dict_value = self.parameters.attr.get_dic()
            body_param["attr"] = attr_dict_value
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.filename is not None:
            body_param["filename"] = self.parameters.filename
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


class Attr(object):

    def __init__(self, dest_backend, ):
        """
        :param dest_backend: 对象存储后端名称，这个研发给出，为固定值(目前固定为shared)
        """
        self.dest_backend = dest_backend
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.dest_backend is not None:
            obj_dict["destBackend"] = self.dest_backend
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.dest_backend is None:
            raise Exception("dest_backend can not None")


class ExportPrivateImageRequestParam(object):

    def __init__(self, region_id, image_id, attr, az_name=None, bucket=None, filename=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区  公有云字段，混合云暂不支持，忽略
        :param image_id: 镜像id
        :param attr: 存储属性
        :param bucket: 对象存储的桶ID  私有镜像必传
        :param filename: 在对象存储的桶中的存储名称  私有镜像必传, 选定桶才生效，命名规则：支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾，长度1-1023   
         注意：对象存储如果未开启版本管理，导出的镜像和已有文件名称相同时，会覆盖同名文件
        """
        self.region_id = region_id
        self.az_name = az_name
        self.image_id = image_id
        self.attr = attr
        self.bucket = bucket
        self.filename = filename

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区  公有云字段，混合云暂不支持，忽略
        """
        self.az_name = az_name

    def set_bucket(self, bucket):
        """
        :param bucket: 对象存储的桶ID  私有镜像必传
        """
        self.bucket = bucket

    def set_filename(self, filename):
        """
        :param filename: 在对象存储的桶中的存储名称  私有镜像必传, 选定桶才生效，命名规则：支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾，长度1-1023   
         注意：对象存储如果未开启版本管理，导出的镜像和已有文件名称相同时，会覆盖同名文件
        """
        self.filename = filename

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")
        if self.attr is None:
            raise Exception("attr can not None")

