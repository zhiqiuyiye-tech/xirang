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


class IaasCtimageImportImageRequest(CTYunRequest):
    """
    使用指定的存在对象存储（原生版）Ⅰ 型的镜像文件来创建一份私有镜像。   
    开发未对齐原因：混合云异步执行会返回任务ID，公有云无返回结果
    """

    def __init__(self, request_param):
        super(IaasCtimageImportImageRequest, self).__init__("/v4/image/import", "POST", "ctimage", "application/json")
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
        if self.parameters.image_file_source is not None:
            body_param["imageFileSource"] = self.parameters.image_file_source
        if self.parameters.import_from_format is not None:
            body_param["importFromFormat"] = self.parameters.import_from_format
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

    def __init__(self, image_name, os_type, os_distro, os_version, disk_format=None, container_format=None, architecture=None, system_disk_size=None, disk_size=None, description=None, image_type=None, boot_mode=None, maximum_ram=None, minimum_ram=None):
        """
        :param image_name: 镜像名称
        :param disk_format: 磁盘格式。取值范围：raw，对齐公有云非必传，固定为raw, 传其他值无效
        :param container_format: 容器格式。取值范围：bare， 对齐公有云非必传，固定为bare，传其他值无效
        :param architecture: 系统架构,x86_64/i386/aarch64
        :param os_type: 操作系统类型,linux/windows/other
        :param os_distro: 系统发行版,（）Windows Server/CentOS/Ubuntu/CTyunOS/Anolis/Debian/Fedora/KylinOS/openEuler/UnionTechOS/Linx/NFSChina/Other
        :param os_version: 发行版本号，7.2/7.3/16.04/2008
        :param system_disk_size: 系统盘大小 单位GB(兼容diskSize)
        :param disk_size: 系统盘大小 单位GB，公有云参数
        :param description: 描述
        :param image_type: 镜像类型  非必传，不传的话默认是系统盘镜像文件；传data_disk_image_from_file，表示数据盘镜像文件
        :param boot_mode: 启动方式(暂不支持)
        :param maximum_ram: 最大内存，单位为 GB(暂不支持)
        :param minimum_ram: 最小内存，单位为 GB(暂不支持)
        """
        self.image_name = image_name
        self.disk_format = disk_format
        self.container_format = container_format
        self.architecture = architecture
        self.os_type = os_type
        self.os_distro = os_distro
        self.os_version = os_version
        self.system_disk_size = system_disk_size
        self.disk_size = disk_size
        self.description = description
        self.image_type = image_type
        self.boot_mode = boot_mode
        self.maximum_ram = maximum_ram
        self.minimum_ram = minimum_ram
        self.check_param()

    def set_disk_format(self, disk_format):
        """
        :param disk_format: 磁盘格式。取值范围：raw，对齐公有云非必传，固定为raw, 传其他值无效
        """
        self.disk_format = disk_format

    def set_container_format(self, container_format):
        """
        :param container_format: 容器格式。取值范围：bare， 对齐公有云非必传，固定为bare，传其他值无效
        """
        self.container_format = container_format

    def set_architecture(self, architecture):
        """
        :param architecture: 系统架构,x86_64/i386/aarch64
        """
        self.architecture = architecture

    def set_system_disk_size(self, system_disk_size):
        """
        :param system_disk_size: 系统盘大小 单位GB(兼容diskSize)
        """
        self.system_disk_size = system_disk_size

    def set_disk_size(self, disk_size):
        """
        :param disk_size: 系统盘大小 单位GB，公有云参数
        """
        self.disk_size = disk_size

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_image_type(self, image_type):
        """
        :param image_type: 镜像类型  非必传，不传的话默认是系统盘镜像文件；传data_disk_image_from_file，表示数据盘镜像文件
        """
        self.image_type = image_type

    def set_boot_mode(self, boot_mode):
        """
        :param boot_mode: 启动方式(暂不支持)
        """
        self.boot_mode = boot_mode

    def set_maximum_ram(self, maximum_ram):
        """
        :param maximum_ram: 最大内存，单位为 GB(暂不支持)
        """
        self.maximum_ram = maximum_ram

    def set_minimum_ram(self, minimum_ram):
        """
        :param minimum_ram: 最小内存，单位为 GB(暂不支持)
        """
        self.minimum_ram = minimum_ram

    def get_dic(self):
        obj_dict = dict()
        if self.image_name is not None:
            obj_dict["imageName"] = self.image_name
        if self.disk_format is not None:
            obj_dict["diskFormat"] = self.disk_format
        if self.container_format is not None:
            obj_dict["containerFormat"] = self.container_format
        if self.architecture is not None:
            obj_dict["architecture"] = self.architecture
        if self.os_type is not None:
            obj_dict["osType"] = self.os_type
        if self.os_distro is not None:
            obj_dict["osDistro"] = self.os_distro
        if self.os_version is not None:
            obj_dict["osVersion"] = self.os_version
        if self.system_disk_size is not None:
            obj_dict["systemDiskSize"] = self.system_disk_size
        if self.disk_size is not None:
            obj_dict["diskSize"] = self.disk_size
        if self.description is not None:
            obj_dict["description"] = self.description
        if self.image_type is not None:
            obj_dict["imageType"] = self.image_type
        if self.boot_mode is not None:
            obj_dict["bootMode"] = self.boot_mode
        if self.maximum_ram is not None:
            obj_dict["maximumRAM"] = self.maximum_ram
        if self.minimum_ram is not None:
            obj_dict["minimumRAM"] = self.minimum_ram
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.image_name is None:
            raise Exception("image_name can not None")
        if self.os_type is None:
            raise Exception("os_type can not None")
        if self.os_distro is None:
            raise Exception("os_distro can not None")
        if self.os_version is None:
            raise Exception("os_version can not None")


class IaasCtimageImportImageRequestParam(object):

    def __init__(self, region_id, image_file_source, image_properties, az_name=None, import_from_format=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区  python为必传，公有云非必传，v2兼容
        :param image_file_source: 导入的镜像的源(地址)
        :param import_from_format: 导入镜像的格式:raw/qcow2/vmdk/vhd
        :param image_properties: 镜像属性
        :param project_id: 项目id
        """
        self.region_id = region_id
        self.az_name = az_name
        self.image_file_source = image_file_source
        self.import_from_format = import_from_format
        self.image_properties = image_properties
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区  python为必传，公有云非必传，v2兼容
        """
        self.az_name = az_name

    def set_import_from_format(self, import_from_format):
        """
        :param import_from_format: 导入镜像的格式:raw/qcow2/vmdk/vhd
        """
        self.import_from_format = import_from_format

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
        if self.image_file_source is None:
            raise Exception("image_file_source can not None")
        if self.image_properties is None:
            raise Exception("image_properties can not None")

