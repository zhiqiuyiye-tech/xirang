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


class UpdateContactsHybridRequest(CTYunRequest):
    """
    调用此接口可修改告警联系人配置，支持全量字段修改。
    """

    def __init__(self, request_param):
        super(UpdateContactsHybridRequest, self).__init__("/v4/monitor/update-contacts", "POST", "monitor", "application/json")
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
        if self.parameters.contact_id is not None:
            body_param["contactID"] = self.parameters.contact_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.phone is not None:
            body_param["phone"] = self.parameters.phone
        if self.parameters.email is not None:
            body_param["email"] = self.parameters.email
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


class UpdateContactsHybridRequestParam(object):

    def __init__(self, contact_id, name, phone=None, email=None):
        """
        :param contact_id: 告警联系人ID
        :param name: 告警联系人名称不可重复，可包含字母、中文、数字，2-50个字符。
        :param phone: 手机号和邮箱二选一必填，手机号填了，邮箱可不填，反之一样，二者不能全为空。
        :param email:  手机号和邮箱二选一必填，邮箱填了，手机号可不填，反之一样，二者不能全为空。
        """
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def set_phone(self, phone):
        """
        :param phone: 手机号和邮箱二选一必填，手机号填了，邮箱可不填，反之一样，二者不能全为空。
        """
        self.phone = phone

    def set_email(self, email):
        """
        :param email:  手机号和邮箱二选一必填，邮箱填了，手机号可不填，反之一样，二者不能全为空。
        """
        self.email = email

    def check_param(self):
        """
        the param required check
        """
        if self.contact_id is None:
            raise Exception("contact_id can not None")
        if self.name is None:
            raise Exception("name can not None")

