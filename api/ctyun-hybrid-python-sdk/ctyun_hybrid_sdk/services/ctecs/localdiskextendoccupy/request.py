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


class LocalDiskExtendOccupyRequest(CTYunRequest):
    """
    1 支持一次预占多个AZ下多个虚机的多个本地盘，部分失败会回滚所有已成功的预占。   
    2 本地盘状态为已预占状态occupied时，不能再次发起预占。   
    3 传入localDisizeSize为扩容后的盘大小。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.LocalDisk.OccupyFailed -- 预占失败   
    Compute.CommonInternalError -- 内部错误
    """

    def __init__(self, request_param):
        super(LocalDiskExtendOccupyRequest, self).__init__("/v4/ecs/localdisk/extend-occupy", "POST", "ctecs", "application/json")
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
        if self.parameters.local_disks is not None:
            local_disks = []
            if isinstance(self.parameters.local_disks, list):
                for item in self.parameters.local_disks:
                    if type(item) is dict:
                        local_disks.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        local_disks.append(item_dict_value)
            else:
                local_disks.append(self.parameters.local_disks.get_dic())
            body_param["localDisks"] = local_disks
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


class LocalDisk(object):

    def __init__(self, local_disk_id, local_disk_size, ):
        """
        :param local_disk_id: 本地盘ID
        :param local_disk_size: 扩容后的盘大小
        """
        self.local_disk_id = local_disk_id
        self.local_disk_size = local_disk_size
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.local_disk_id is not None:
            obj_dict["localDiskID"] = self.local_disk_id
        if self.local_disk_size is not None:
            obj_dict["localDiskSize"] = self.local_disk_size
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.local_disk_id is None:
            raise Exception("local_disk_id can not None")
        if self.local_disk_size is None:
            raise Exception("local_disk_size can not None")


class LocalDiskExtendOccupyRequestParam(object):

    def __init__(self, region_id, local_disks, ):
        """
        :param region_id: 资源池ID
        :param local_disks:  注意:此参数为数组
        """
        self.region_id = region_id
        self.local_disks = local_disks

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.local_disks is None:
            raise Exception("local_disks can not None")

