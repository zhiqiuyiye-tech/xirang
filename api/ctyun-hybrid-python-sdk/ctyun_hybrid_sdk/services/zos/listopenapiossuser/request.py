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


class ListOpenAPIOssUserRequest(CTYunRequest):
    """
    查询oss用户列表
    """

    def __init__(self, request_param):
        super(ListOpenAPIOssUserRequest, self).__init__("/v4/oss/list-user", "GET", "zos", "")
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
        if self.parameters.vdc_id is not None:
            query_param["vdcID"] = self.parameters.vdc_id
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListOpenAPIOssUserRequestParam(object):

    def __init__(self, region_id, page, page_size, vdc_id=None, query_content=None):
        """
        :param region_id: 资源池ID
        :param vdc_id: VDC ID 查询指定VDC下的所有对象存储用户，默认查询用户所在VDC下的对象存储用户
        :param query_content: 支持用户名模糊搜索
        :param page: 页码，默认值1
        :param page_size: 分页大小，默认值10
        """
        self.region_id = region_id
        self.vdc_id = vdc_id
        self.query_content = query_content
        self.page = page
        self.page_size = page_size

    def set_vdc_id(self, vdc_id):
        """
        :param vdc_id: VDC ID 查询指定VDC下的所有对象存储用户，默认查询用户所在VDC下的对象存储用户
        """
        self.vdc_id = vdc_id

    def set_query_content(self, query_content):
        """
        :param query_content: 支持用户名模糊搜索
        """
        self.query_content = query_content

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

