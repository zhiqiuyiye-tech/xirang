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


class QueryResourceGroupsRequest(CTYunRequest):
    """
    调用此接口可查询用户资源分组列表。
    """

    def __init__(self, request_param):
        super(QueryResourceGroupsRequest, self).__init__("/v4.1/monitor/query-resource-groups", "GET", "monitor", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.res_group_id is not None:
            query_param["resGroupID"] = self.parameters.res_group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryResourceGroupsRequestParam(object):

    def __init__(self, region_id, name=None, page_no=None, page_size=None, res_group_id=None):
        """
        :param region_id: 资源池ID
        :param name: 名称模糊搜索
        :param page_no: 页码，默认为1
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        :param res_group_id: 资源分组ID搜索
        """
        self.region_id = region_id
        self.name = name
        self.page_no = page_no
        self.page_size = page_size
        self.res_group_id = res_group_id

    def set_name(self, name):
        """
        :param name: 名称模糊搜索
        """
        self.name = name

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def set_res_group_id(self, res_group_id):
        """
        :param res_group_id: 资源分组ID搜索
        """
        self.res_group_id = res_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

