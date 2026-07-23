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


class CreateContactGroupHybridRequest(CTYunRequest):
    """
    调用此接口可创建告警联系组。
    """

    def __init__(self, request_param):
        super(CreateContactGroupHybridRequest, self).__init__("/v4/monitor/create-contact-group", "POST", "monitor", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.desc is not None:
            body_param["desc"] = self.parameters.desc
        if self.parameters.contact_id_list is not None:
            body_param["contactIDList"] = self.parameters.contact_id_list
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


class CreateContactGroupHybridRequestParam(object):

    def __init__(self, name, region_id, desc=None, contact_id_list=None):
        """
        :param name: 告警联系人组名称。告警联系人组名称不可重复，可包含字母、中文、数字，2-50个字符。
        :param region_id: 资源池ID（混合云必须）
        :param desc: 组描述（混合云管无此参数）
        :param contact_id_list: 告警联系人ID列表 注意:此参数为数组
        """
        self.name = name
        self.region_id = region_id
        self.desc = desc
        self.contact_id_list = contact_id_list

    def set_desc(self, desc):
        """
        :param desc: 组描述（混合云管无此参数）
        """
        self.desc = desc

    def set_contact_id_list(self, contact_id_list):
        """
        :param contact_id_list: 告警联系人ID列表
        """
        self.contact_id_list = contact_id_list

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

