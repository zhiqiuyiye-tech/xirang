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


class UserAttachUserToGroupHubRequest(CTYunRequest):
    """
    用户批量加入用户组,传入什么用户组id，用户就只拥有这些用户组id，用户不能加入的用户组会过滤掉
    """

    def __init__(self, request_param):
        super(UserAttachUserToGroupHubRequest, self).__init__("/v1/user/hub/userSetGroup", "POST", "iam", "application/json")
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
        if self.parameters.user_id is not None:
            body_param["userId"] = self.parameters.user_id
        if self.parameters.group_ids is not None:
            body_param["groupIds"] = self.parameters.group_ids
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


class UserAttachUserToGroupHubRequestParam(object):

    def __init__(self, user_id, group_ids, ):
        """
        :param user_id: 用户id
        :param group_ids: 用户组id列表 注意:此参数为数组
        """
        self.user_id = user_id
        self.group_ids = group_ids

    def check_param(self):
        """
        the param required check
        """
        if self.user_id is None:
            raise Exception("user_id can not None")
        if self.group_ids is None:
            raise Exception("group_ids can not None")

