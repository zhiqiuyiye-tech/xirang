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


class VolumeSpecAssessRequest(CTYunRequest):
    """
    对指定资源池可用区下的硬盘类型开通大小进行可行性校验（可批量校验）   
    入参为[regiongID,azID,volumeType]的总容量，[regiongID,azID,volumeType]不可重复   
    notAllowedInfo返回校验失败的数据   
    接口返回成功，notAllowedInfo为空则代表全部校验成功
    """

    def __init__(self, request_param):
        super(VolumeSpecAssessRequest, self).__init__("/v4/ebs/spec-assess", "POST", "ebs", "application/json")
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
        if self.parameters.volume_type_size is not None:
            volume_type_size = []
            if isinstance(self.parameters.volume_type_size, list):
                for item in self.parameters.volume_type_size:
                    if type(item) is dict:
                        volume_type_size.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        volume_type_size.append(item_dict_value)
            else:
                volume_type_size.append(self.parameters.volume_type_size.get_dic())
            body_param["volumeTypeSize"] = volume_type_size
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


class VolumeTypeSize(object):

    def __init__(self, region_id, volume_type, total_size, az_id=None):
        """
        :param region_id: 资源池ID
        :param az_id: 4.0资源池必传
        :param volume_type: 支持公有云的SAS SATA SSD-genric SSD FAST-SSD，同时也支持产销品中的规格
        :param total_size: 单位GB
        """
        self.region_id = region_id
        self.az_id = az_id
        self.volume_type = volume_type
        self.total_size = total_size
        self.check_param()

    def set_az_id(self, az_id):
        """
        :param az_id: 4.0资源池必传
        """
        self.az_id = az_id

    def get_dic(self):
        obj_dict = dict()
        if self.region_id is not None:
            obj_dict["regionID"] = self.region_id
        if self.az_id is not None:
            obj_dict["azID"] = self.az_id
        if self.volume_type is not None:
            obj_dict["volumeType"] = self.volume_type
        if self.total_size is not None:
            obj_dict["totalSize"] = self.total_size
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.volume_type is None:
            raise Exception("volume_type can not None")
        if self.total_size is None:
            raise Exception("total_size can not None")


class VolumeSpecAssessRequestParam(object):

    def __init__(self, volume_type_size, ):
        """
        :param volume_type_size: 待开通类型及容量 注意:此参数为数组
        """
        self.volume_type_size = volume_type_size

    def check_param(self):
        """
        the param required check
        """
        if self.volume_type_size is None:
            raise Exception("volume_type_size can not None")

