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


class EcsBatchRebuildRequest(CTYunRequest):
    """
    该接口提供用户重装多台云主机功能，通过填写相应云主机ID、镜像ID和密码对云主机进行重装。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    2. 若云主机存在快照，不允许执行重装操作。
    """

    def __init__(self, request_param):
        super(EcsBatchRebuildRequest, self).__init__("/v4/ecs/batch-rebuild", "POST", "ctecs", "application/json")
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
        if self.parameters.rebuild_info is not None:
            rebuild_info = []
            if isinstance(self.parameters.rebuild_info, list):
                for item in self.parameters.rebuild_info:
                    if type(item) is dict:
                        rebuild_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        rebuild_info.append(item_dict_value)
            else:
                rebuild_info.append(self.parameters.rebuild_info.get_dic())
            body_param["rebuildInfo"] = rebuild_info
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


class RebuildInfo(object):

    def __init__(self, id, image_id, password, user_data=None):
        """
        :param id: 云主机ID
        :param image_id: 镜像ID
        :param password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等
        :param user_data: 用户自定义数据,需要以Base64方式编码
        """
        self.id = id
        self.image_id = image_id
        self.password = password
        self.user_data = user_data
        self.check_param()

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据,需要以Base64方式编码
        """
        self.user_data = user_data

    def get_dic(self):
        obj_dict = dict()
        if self.id is not None:
            obj_dict["ID"] = self.id
        if self.image_id is not None:
            obj_dict["imageID"] = self.image_id
        if self.password is not None:
            obj_dict["password"] = self.password
        if self.user_data is not None:
            obj_dict["userData"] = self.user_data
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")
        if self.password is None:
            raise Exception("password can not None")


class EcsBatchRebuildRequestParam(object):

    def __init__(self, region_id, rebuild_info, az_name=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可以区名称，没有可用区时填default
        :param rebuild_info: 重装信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.az_name = az_name
        self.rebuild_info = rebuild_info

    def set_az_name(self, az_name):
        """
        :param az_name: 可以区名称，没有可用区时填default
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.rebuild_info is None:
            raise Exception("rebuild_info can not None")

