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


class CloneVdcUserGroupRequest(CTYunRequest):
    """
    克隆VDC用户组
    """

    def __init__(self, request_param):
        super(CloneVdcUserGroupRequest, self).__init__("/v1/vdc/clone-user-group", "POST", "iam", "application/json")
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
        if self.parameters.ori_group_id is not None:
            body_param["oriGroupID"] = self.parameters.ori_group_id
        if self.parameters.vdc_id is not None:
            body_param["vdcID"] = self.parameters.vdc_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class CloneVdcUserGroupRequestParam(object):

    def __init__(self, name, ori_group_id, vdc_id=None, description=None):
        """
        :param name: 用户组名称
        :param ori_group_id: 被克隆的用户组id
        :param vdc_id: 被克隆用户组所属vdc的id
        :param description: 描述
        """
        self.name = name
        self.ori_group_id = ori_group_id
        self.vdc_id = vdc_id
        self.description = description

    def set_vdc_id(self, vdc_id):
        """
        :param vdc_id: 被克隆用户组所属vdc的id
        """
        self.vdc_id = vdc_id

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.ori_group_id is None:
            raise Exception("ori_group_id can not None")

