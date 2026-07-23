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


class ShowAccessControlRequest(CTYunRequest):
    """
    查询访问控制详情
    """

    def __init__(self, request_param):
        super(ShowAccessControlRequest, self).__init__("/v4/elb/show-access-control", "GET", "ctelb", "")
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
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        if self.parameters.access_control_id is not None:
            query_param["accessControlID"] = self.parameters.access_control_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowAccessControlRequestParam(object):

    def __init__(self, region_id, id=None, access_control_id=None):
        """
        :param region_id: 资源池ID
        :param id: 访问控制ID, 该字段后续废弃
        :param access_control_id: 访问控制ID, 推荐使用该字段, 当同时使用 id 和 accessControlID 时，优先使用 accessControlID
        """
        self.region_id = region_id
        self.id = id
        self.access_control_id = access_control_id

    def set_id(self, id):
        """
        :param id: 访问控制ID, 该字段后续废弃
        """
        self.id = id

    def set_access_control_id(self, access_control_id):
        """
        :param access_control_id: 访问控制ID, 推荐使用该字段, 当同时使用 id 和 accessControlID 时，优先使用 accessControlID
        """
        self.access_control_id = access_control_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

