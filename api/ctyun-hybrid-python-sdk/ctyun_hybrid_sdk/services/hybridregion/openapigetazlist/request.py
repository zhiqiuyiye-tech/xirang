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


class OpenApiGetAzListRequest(CTYunRequest):
    """
    查询可用区
    """

    def __init__(self, request_param):
        super(OpenApiGetAzListRequest, self).__init__("/v1/azs/list", "GET", "hybridregion", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.code is not None:
            query_param["code"] = self.parameters.code
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenApiGetAzListRequestParam(object):

    def __init__(self, region_id, page=None, page_size=None, name=None, code=None, status=None):
        """
        :param region_id: 要查询可用区的资源池ID
        :param page: 页码，默认值1
        :param page_size: 分页大小，默认值10
        :param name: 可用区名称
        :param code: 可用区code
        :param status: 1在线0离线
        """
        self.region_id = region_id
        self.page = page
        self.page_size = page_size
        self.name = name
        self.code = code
        self.status = status

    def set_page(self, page):
        """
        :param page: 页码，默认值1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小，默认值10
        """
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 可用区名称
        """
        self.name = name

    def set_code(self, code):
        """
        :param code: 可用区code
        """
        self.code = code

    def set_status(self, status):
        """
        :param status: 1在线0离线
        """
        self.status = status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

