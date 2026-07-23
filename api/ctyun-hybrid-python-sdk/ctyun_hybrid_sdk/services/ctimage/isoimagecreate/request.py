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


class IsoImageCreateRequest(CTYunRequest):
    """
    创建iso镜像
    """

    def __init__(self, request_param):
        super(IsoImageCreateRequest, self).__init__("/v4/image/create-from-iso", "POST", "ctimage", "application/json")
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
        if self.parameters.import_from is not None:
            body_param["importFrom"] = self.parameters.import_from
        if self.parameters.image_properties is not None:
            if type(self.parameters.image_properties) is dict:
                image_properties_dict_value = self.parameters.image_properties
            else:
                image_properties_dict_value = self.parameters.image_properties.get_dic()
            body_param["imageProperties"] = image_properties_dict_value
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class ImageProperties(object):

    def __init__(self, name, arch, os_type, os_distro, os_version, description=None):
        """
        :param name: 镜像名称   
         长度为2-32字符   
         支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param arch: 系统架构   
         aarch64/x86_64/i386/loongarch64
        :param os_type: 操作系统类型   
         linux/windows
        :param os_distro: 系统平台（除windows之外的都是linux）   
         Windows Server/CentOS/Ubuntu/CTyunOS/Anolis/Debian/Fedora/KylinOS/openEuler/UnionTechOS/Linx/NFSChina/Other
        :param os_version: 镜像版本(最长100个字符)
        :param description: 描述(长度为 1~128 个字符)
        """
        self.name = name
        self.arch = arch
        self.os_type = os_type
        self.os_distro = os_distro
        self.os_version = os_version
        self.description = description
        self.check_param()

    def set_description(self, description):
        """
        :param description: 描述(长度为 1~128 个字符)
        """
        self.description = description

    def get_dic(self):
        obj_dict = dict()
        if self.name is not None:
            obj_dict["name"] = self.name
        if self.arch is not None:
            obj_dict["arch"] = self.arch
        if self.os_type is not None:
            obj_dict["osType"] = self.os_type
        if self.os_distro is not None:
            obj_dict["osDistro"] = self.os_distro
        if self.os_version is not None:
            obj_dict["osVersion"] = self.os_version
        if self.description is not None:
            obj_dict["description"] = self.description
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.arch is None:
            raise Exception("arch can not None")
        if self.os_type is None:
            raise Exception("os_type can not None")
        if self.os_distro is None:
            raise Exception("os_distro can not None")
        if self.os_version is None:
            raise Exception("os_version can not None")


class IsoImageCreateRequestParam(object):

    def __init__(self, region_id, import_from, image_properties, az_name=None, project_id=None):
        """
        :param region_id: 资源池id
        :param az_name: 可用区id
        :param import_from: 镜像文件地址（对象存储复制url，桶和桶文件必须是公共读及以上）
        :param image_properties: 镜像文件属性
        :param project_id: 项目id
        """
        self.region_id = region_id
        self.az_name = az_name
        self.import_from = import_from
        self.image_properties = image_properties
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区id
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 项目id
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.import_from is None:
            raise Exception("import_from can not None")
        if self.image_properties is None:
            raise Exception("image_properties can not None")

