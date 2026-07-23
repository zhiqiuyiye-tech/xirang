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


class ListImagesRequest(CTYunRequest):
    """
    根据镜像可见类型等，查询可以使用的镜像资源。
    """

    def __init__(self, request_param):
        super(ListImagesRequest, self).__init__("/v4/image/list", "GET", "ctimage", "")
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
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.visibility is not None:
            query_param["visibility"] = self.parameters.visibility
        if self.parameters.image_visibility_code is not None:
            query_param["imageVisibilityCode"] = self.parameters.image_visibility_code
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.flavor_name is not None:
            query_param["flavorName"] = self.parameters.flavor_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListImagesRequestParam(object):

    def __init__(self, region_id, az_name=None, visibility=None, image_visibility_code=None, query_content=None, page_no=None, page_size=None, project_id=None, flavor_name=None):
        """
        :param region_id: 区域ID
        :param az_name: 可用区
        :param visibility: 镜像可见类型：'private',私有镜像；默认为公有镜像'public'；共享镜像'shared'   
         兼容传值：0(private) 1(public) 2(shared)
        :param image_visibility_code: 镜像可见类型代码，取值：0 = 私有镜像；1 = 公有镜像 2 = 共享镜像   
         visibility参数不为空时优先用visibility
        :param query_content: 查询内容:支持【镜像名称】模糊查询
        :param page_no: 页码
        :param page_size: 每页记录数目
        :param project_id: 仅在 visibility=private（私有镜像）时生效
        :param flavor_name: 规格名称过滤(过滤同架构的镜像)
        """
        self.region_id = region_id
        self.az_name = az_name
        self.visibility = visibility
        self.image_visibility_code = image_visibility_code
        self.query_content = query_content
        self.page_no = page_no
        self.page_size = page_size
        self.project_id = project_id
        self.flavor_name = flavor_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_visibility(self, visibility):
        """
        :param visibility: 镜像可见类型：'private',私有镜像；默认为公有镜像'public'；共享镜像'shared'   
         兼容传值：0(private) 1(public) 2(shared)
        """
        self.visibility = visibility

    def set_image_visibility_code(self, image_visibility_code):
        """
        :param image_visibility_code: 镜像可见类型代码，取值：0 = 私有镜像；1 = 公有镜像 2 = 共享镜像   
         visibility参数不为空时优先用visibility
        """
        self.image_visibility_code = image_visibility_code

    def set_query_content(self, query_content):
        """
        :param query_content: 查询内容:支持【镜像名称】模糊查询
        """
        self.query_content = query_content

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目
        """
        self.page_size = page_size

    def set_project_id(self, project_id):
        """
        :param project_id: 仅在 visibility=private（私有镜像）时生效
        """
        self.project_id = project_id

    def set_flavor_name(self, flavor_name):
        """
        :param flavor_name: 规格名称过滤(过滤同架构的镜像)
        """
        self.flavor_name = flavor_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

