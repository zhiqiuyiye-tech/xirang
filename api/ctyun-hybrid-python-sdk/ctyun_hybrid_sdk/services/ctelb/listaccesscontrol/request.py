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


class ListAccessControlRequest(CTYunRequest):
    """
    查询策略地址组，访问控制采用黑、白名单方式实现，此接口为查询黑、白名单的地址组。   
    
    """

    def __init__(self, request_param):
        super(ListAccessControlRequest, self).__init__("/v4/elb/list-access-control", "GET", "ctelb", "")
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
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListAccessControlRequestParam(object):

    def __init__(self, region_id, ids=None, name=None):
        """
        :param region_id: 区域ID
        :param ids: 访问控制ID列表 多个用,号分割
        :param name: 访问控制名称,只能由数字，字母，-组成不能以数字和-开头，最大长度32
        """
        self.region_id = region_id
        self.ids = ids
        self.name = name

    def set_ids(self, ids):
        """
        :param ids: 访问控制ID列表 多个用,号分割
        """
        self.ids = ids

    def set_name(self, name):
        """
        :param name: 访问控制名称,只能由数字，字母，-组成不能以数字和-开头，最大长度32
        """
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

