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


class ListTargetNewRequest(CTYunRequest):
    """
    查看后端服务列表，对齐公有云
    """

    def __init__(self, request_param):
        super(ListTargetNewRequest, self).__init__("/v4/elb/list-target-new", "GET", "ctelb", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.target_group_id is not None:
            query_param["targetGroupID"] = self.parameters.target_group_id
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListTargetNewRequestParam(object):

    def __init__(self, region_id, target_group_id=None, ids=None):
        """
        :param region_id: 区域ID
        :param target_group_id: 后端服务组ID
        :param ids: 后端服务ID列表，以","分隔
        """
        self.region_id = region_id
        self.target_group_id = target_group_id
        self.ids = ids

    def set_target_group_id(self, target_group_id):
        """
        :param target_group_id: 后端服务组ID
        """
        self.target_group_id = target_group_id

    def set_ids(self, ids):
        """
        :param ids: 后端服务ID列表，以","分隔
        """
        self.ids = ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

