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


class InstanceDetachSfsV41Request(CTYunRequest):
    """
    此接口提供用户实现云主机卸载一个或多个文件系统的功能(仅4.0支持)   
       
    1. 云主机须处于运行状态   
    2. 云主机和文件系统应属于同一个VPC   
    3. 云主机仅支持部分镜像类型挂载，windows镜像：windows server 2012 数据中心版 R2 64位中文版（主镜像）、windows server 2012 标准版 R2 64位中文版、windows server 2016 数据中心版 64位中文版、windows server 2019 数据中心版 64位中文版。linux镜像：CentOS-7.8-x86_64、CentOS-7.9-x86_64（主镜像）、 CentOS-8.0-x86_64、 CentOS-8.1-x86_64、 CentOS-8.2-x86_64、Ubuntu-18.04-x86_64、Ubuntu-20.04-x86_64、Ctyunos-2.0.1_220311-x86_64
    """

    def __init__(self, request_param):
        super(InstanceDetachSfsV41Request, self).__init__("/v4/ecs/sfs/detach", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.force_del is not None:
            body_param["forceDel"] = self.parameters.force_del
        if self.parameters.sys_info_list is not None:
            sys_info_list = []
            if isinstance(self.parameters.sys_info_list, list):
                for item in self.parameters.sys_info_list:
                    if type(item) is dict:
                        sys_info_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        sys_info_list.append(item_dict_value)
            else:
                sys_info_list.append(self.parameters.sys_info_list.get_dic())
            body_param["sysInfoList"] = sys_info_list
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


class SysInfo(object):

    def __init__(self, file_sys_route, mount_point, ):
        """
        :param file_sys_route: 文件系统地址（固定值，每一个文件都有相对应的文件系统地址）
        :param mount_point: 挂载点
        """
        self.file_sys_route = file_sys_route
        self.mount_point = mount_point
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.file_sys_route is not None:
            obj_dict["fileSysRoute"] = self.file_sys_route
        if self.mount_point is not None:
            obj_dict["mountPoint"] = self.mount_point
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.file_sys_route is None:
            raise Exception("file_sys_route can not None")
        if self.mount_point is None:
            raise Exception("mount_point can not None")


class InstanceDetachSfsV41RequestParam(object):

    def __init__(self, region_id, instance_id, sys_info_list, force_del=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param force_del: 是否强制解绑 (true/false)，默认非强制
        :param sys_info_list: 所解绑的文件系统详细信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.force_del = force_del
        self.sys_info_list = sys_info_list

    def set_force_del(self, force_del):
        """
        :param force_del: 是否强制解绑 (true/false)，默认非强制
        """
        self.force_del = force_del

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.sys_info_list is None:
            raise Exception("sys_info_list can not None")

