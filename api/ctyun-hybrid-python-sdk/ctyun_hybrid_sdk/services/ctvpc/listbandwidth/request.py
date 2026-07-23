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


class ListBandwidthRequest(CTYunRequest):
    """
    返回体中的creator已废弃勿用，值为空
    """

    def __init__(self, request_param):
        super(ListBandwidthRequest, self).__init__("/v4/bandwidth/list", "GET", "ctvpc", "")
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
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.resource_id is not None:
            query_param["resourceId"] = self.parameters.resource_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListBandwidthRequestParam(object):

    def __init__(self, region_id, query_content=None, page_number=None, page_size=None, resource_id=None):
        """
        :param region_id: 资源池id
        :param query_content: 模糊搜索，支持的字段包含uuid、name
        :param page_number: 页码，默认值1。不填/输入0，按照1查询，小于0报参数错误
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询，小于0报参数错误
        :param resource_id: 资源id（差异点说明：2.0与公有云保持一致，在云管相当于带宽ID）
        """
        self.region_id = region_id
        self.query_content = query_content
        self.page_number = page_number
        self.page_size = page_size
        self.resource_id = resource_id

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索，支持的字段包含uuid、name
        """
        self.query_content = query_content

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询，小于0报参数错误
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询，小于0报参数错误
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id（差异点说明：2.0与公有云保持一致，在云管相当于带宽ID）
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

