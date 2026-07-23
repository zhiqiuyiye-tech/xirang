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


class GetEcsResourceAssessHybridRequest(CTYunRequest):
    """
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.AvailableZoneNotFound -- 非法的可用区   
    Compute.Param.Error -- 参数错误   
    Compute.CommonInternalError -- 内部错误   
    
    """

    def __init__(self, request_param):
        super(GetEcsResourceAssessHybridRequest, self).__init__("/v4/ecs/get-resources-assess", "POST", "ctecs", "application/json")
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
        if self.parameters.flavor_list is not None:
            flavor_list = []
            if isinstance(self.parameters.flavor_list, list):
                for item in self.parameters.flavor_list:
                    if type(item) is dict:
                        flavor_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        flavor_list.append(item_dict_value)
            else:
                flavor_list.append(self.parameters.flavor_list.get_dic())
            body_param["flavorList"] = flavor_list
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


class Flavor(object):

    def __init__(self, flavor_name, availability_zone=None, local_disk=None):
        """
        :param flavor_name: 规格名称
        :param availability_zone: 规格的集群参数，flavor的availability_zone参数
        :param local_disk: 创建kir4规格族支持传递
        """
        self.flavor_name = flavor_name
        self.availability_zone = availability_zone
        self.local_disk = local_disk
        self.check_param()

    def set_availability_zone(self, availability_zone):
        """
        :param availability_zone: 规格的集群参数，flavor的availability_zone参数
        """
        self.availability_zone = availability_zone

    def set_local_disk(self, local_disk):
        """
        :param local_disk: 创建kir4规格族支持传递
        """
        self.local_disk = local_disk

    def get_dic(self):
        obj_dict = dict()
        if self.flavor_name is not None:
            obj_dict["flavorName"] = self.flavor_name
        if self.availability_zone is not None:
            obj_dict["availabilityZone"] = self.availability_zone
        if self.local_disk is not None:
            if type(self.local_disk) is dict:
                obj_dict["localDisk"] = self.local_disk
            else:
                obj_dict["localDisk"] = self.local_disk.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.flavor_name is None:
            raise Exception("flavor_name can not None")


class LocalDisk(object):

    def __init__(self, disk_type=None, disk_size=None):
        """
        :param disk_type: 本地盘类型
        :param disk_size: 本地盘大小
        """
        self.disk_type = disk_type
        self.disk_size = disk_size

    def set_disk_type(self, disk_type):
        """
        :param disk_type: 本地盘类型
        """
        self.disk_type = disk_type

    def set_disk_size(self, disk_size):
        """
        :param disk_size: 本地盘大小
        """
        self.disk_size = disk_size

    def get_dic(self):
        obj_dict = dict()
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.disk_size is not None:
            obj_dict["diskSize"] = self.disk_size
        return obj_dict


class GetEcsResourceAssessHybridRequestParam(object):

    def __init__(self, region_id, flavor_list, az_name=None):
        """
        :param region_id: 资源池ID 
        :param az_name: 4.0必填
        :param flavor_list: 查询的规格列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.az_name = az_name
        self.flavor_list = flavor_list

    def set_az_name(self, az_name):
        """
        :param az_name: 4.0必填
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.flavor_list is None:
            raise Exception("flavor_list can not None")

