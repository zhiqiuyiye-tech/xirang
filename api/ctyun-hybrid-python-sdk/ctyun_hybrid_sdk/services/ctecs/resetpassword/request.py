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


class ResetPasswordRequest(CTYunRequest):
    """
    更新云主机的密码,此接口为同步接口。   
       
    ### 接口约束   
       
    1. 云主机必须处于运行状态   
    
    """

    def __init__(self, request_param):
        super(ResetPasswordRequest, self).__init__("/v4/ecs/reset-password", "POST", "ctecs", "application/json")
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
        if self.parameters.new_password is not None:
            body_param["newPassword"] = self.parameters.new_password
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


class ResetPasswordRequestParam(object):

    def __init__(self, region_id, instance_id, new_password, ):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param new_password: 新密码，满足以下规则：长度在8～30个字符;必须包含大写字母、小写字母、数字以及特殊符号中的三项; 特殊符号可选：()`~!@#$%^&*_-+=\\｜{}[]:;'<>,.?/ 且不能以斜线号/开头
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.new_password = new_password

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.new_password is None:
            raise Exception("new_password can not None")

