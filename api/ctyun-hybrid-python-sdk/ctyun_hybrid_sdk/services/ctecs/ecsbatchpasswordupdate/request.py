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


class EcsBatchPasswordUpdateRequest(CTYunRequest):
    """
    更新多台云主机的密码
    """

    def __init__(self, request_param):
        super(EcsBatchPasswordUpdateRequest, self).__init__("/v4/ecs/batch-password-update", "POST", "ctecs", "application/json")
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
        if self.parameters.update_pwd_info is not None:
            update_pwd_info = []
            if isinstance(self.parameters.update_pwd_info, list):
                for item in self.parameters.update_pwd_info:
                    if type(item) is dict:
                        update_pwd_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        update_pwd_info.append(item_dict_value)
            else:
                update_pwd_info.append(self.parameters.update_pwd_info.get_dic())
            body_param["updatePwdInfo"] = update_pwd_info
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


class UpdatePwdInfo(object):

    def __init__(self, id, password, ):
        """
        :param id: 云主机ID
        :param password: 新密码，满足以下规则：    
         长度在8～30个字符;    
         必须包含大写字母、小写字母、数字以及特殊符号中的三项;    
         特殊符号可选：()`~!@#$%^&*_-+=\\|{}[]:;'<>,.?/ 且不能以斜线号/开头
        """
        self.id = id
        self.password = password
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.id is not None:
            obj_dict["ID"] = self.id
        if self.password is not None:
            obj_dict["password"] = self.password
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.password is None:
            raise Exception("password can not None")


class EcsBatchPasswordUpdateRequestParam(object):

    def __init__(self, region_id, update_pwd_info, az_name=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称，暂未提供 可不传
        :param update_pwd_info: 批量更新密码信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.az_name = az_name
        self.update_pwd_info = update_pwd_info

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，暂未提供 可不传
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.update_pwd_info is None:
            raise Exception("update_pwd_info can not None")

