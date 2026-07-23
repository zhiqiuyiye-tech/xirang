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


class QuerySharedImageHybridRequest(CTYunRequest):
    """
    开发未对齐原因：按照最初提供的Excel和混合云对接开发的，一直未找到公有云接口   
    
    """

    def __init__(self, request_param):
        super(QuerySharedImageHybridRequest, self).__init__("/v4/image/query-shared-images", "GET", "ctimage", "")
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
        if self.parameters.image_id is not None:
            query_param["imageID"] = self.parameters.image_id
        if self.parameters.is_provider is not None:
            query_param["isProvider"] = self.parameters.is_provider
        if self.parameters.status_list is not None:
            query_param["statusList"] = self.parameters.status_list
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QuerySharedImageHybridRequestParam(object):

    def __init__(self, region_id, image_id=None, is_provider=None, status_list=None, query_content=None, sort=None, asc=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param image_id: 镜像id
        :param is_provider: 是否查询提供出去的共享镜像 1是;0否,不传默认是0
        :param status_list: 镜像状态:逗号分隔, 0待接受;1已接受;2已拒绝
        :param query_content: 模糊搜索 支持镜像名称
        :param sort: 排序字段 目前支持 "created_time", "status"
        :param asc: 1 降序;0 升序
        :param page_no: 页码（默认1）
        :param page_size: 每页记录数目（0或者不传默认10）
        """
        self.region_id = region_id
        self.image_id = image_id
        self.is_provider = is_provider
        self.status_list = status_list
        self.query_content = query_content
        self.sort = sort
        self.asc = asc
        self.page_no = page_no
        self.page_size = page_size

    def set_image_id(self, image_id):
        """
        :param image_id: 镜像id
        """
        self.image_id = image_id

    def set_is_provider(self, is_provider):
        """
        :param is_provider: 是否查询提供出去的共享镜像 1是;0否,不传默认是0
        """
        self.is_provider = is_provider

    def set_status_list(self, status_list):
        """
        :param status_list: 镜像状态:逗号分隔, 0待接受;1已接受;2已拒绝
        """
        self.status_list = status_list

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索 支持镜像名称
        """
        self.query_content = query_content

    def set_sort(self, sort):
        """
        :param sort: 排序字段 目前支持 "created_time", "status"
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: 1 降序;0 升序
        """
        self.asc = asc

    def set_page_no(self, page_no):
        """
        :param page_no: 页码（默认1）
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目（0或者不传默认10）
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

