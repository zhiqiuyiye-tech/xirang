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


class NewACLListRequest(CTYunRequest):
    """
    查询acl列表
    """

    def __init__(self, request_param):
        super(NewACLListRequest, self).__init__("/v4/acl/new-list", "GET", "ctvpc", "")
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
        if self.parameters.acl_id is not None:
            query_param["aclID"] = self.parameters.acl_id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class NewACLListRequestParam(object):

    def __init__(self, region_id, acl_id=None, name=None, page_number=None, page_size=None):
        """
        :param region_id: 资源id
        :param acl_id: ACL ID
        :param name: ACL名称
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.region_id = region_id
        self.acl_id = acl_id
        self.name = name
        self.page_number = page_number
        self.page_size = page_size

    def set_acl_id(self, acl_id):
        """
        :param acl_id: ACL ID
        """
        self.acl_id = acl_id

    def set_name(self, name):
        """
        :param name: ACL名称
        """
        self.name = name

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

