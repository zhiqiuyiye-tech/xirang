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


class BindVdcUsersToUserGourpRequest(CTYunRequest):
    """
    VDC用户组绑定用户
    """

    def __init__(self, request_param):
        super(BindVdcUsersToUserGourpRequest, self).__init__("/v1/vdc/bind-users-to-user-group", "POST", "iam", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.user_ids is not None:
            body_param["userIDs"] = self.parameters.user_ids
        if self.parameters.org_id is not None:
            body_param["orgID"] = self.parameters.org_id
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


class BindVdcUsersToUserGourpRequestParam(object):

    def __init__(self, group_id, org_id, user_ids=None):
        """
        :param group_id: 用户组id
        :param user_ids: 用户id 注意:此参数为数组
        :param org_id: 所属vdc的id
        """
        self.group_id = group_id
        self.user_ids = user_ids
        self.org_id = org_id

    def set_user_ids(self, user_ids):
        """
        :param user_ids: 用户id
        """
        self.user_ids = user_ids

    def check_param(self):
        """
        the param required check
        """
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.org_id is None:
            raise Exception("org_id can not None")

