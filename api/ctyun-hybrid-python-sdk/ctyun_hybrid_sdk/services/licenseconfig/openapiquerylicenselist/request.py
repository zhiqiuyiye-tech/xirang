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


class OpenAPIQueryLicenseListRequest(CTYunRequest):
    """
    查询许可证列表
    """

    def __init__(self, request_param):
        super(OpenAPIQueryLicenseListRequest, self).__init__("/v4/license/list", "GET", "licenseconfig", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.auth_type is not None:
            query_param["authType"] = self.parameters.auth_type
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
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


class OpenAPIQueryLicenseListRequestParam(object):

    def __init__(self, name=None, query_content=None, auth_type=None, status=None, sort=None, asc=None, page_no=None, page_size=None):
        """
        :param name: 许可证名称
        :param query_content: 模糊查找
        :param auth_type: 许可证类型, 1-正式, 2-测试, 3-试用，多个用逗号分隔
        :param status: 许可证状态, 1-有效, 2-无效, 3-已过期，多个用逗号分隔
        :param sort: 指定字段排序，支持"created_time"-创建时间, "release_time"-发布时间, "expire_time"-过期时间
        :param asc: 指定升序/降序,asc-升序,desc-降序
        :param page_no: 页码
        :param page_size: 分页大小
        """
        self.name = name
        self.query_content = query_content
        self.auth_type = auth_type
        self.status = status
        self.sort = sort
        self.asc = asc
        self.page_no = page_no
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 许可证名称
        """
        self.name = name

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查找
        """
        self.query_content = query_content

    def set_auth_type(self, auth_type):
        """
        :param auth_type: 许可证类型, 1-正式, 2-测试, 3-试用，多个用逗号分隔
        """
        self.auth_type = auth_type

    def set_status(self, status):
        """
        :param status: 许可证状态, 1-有效, 2-无效, 3-已过期，多个用逗号分隔
        """
        self.status = status

    def set_sort(self, sort):
        """
        :param sort: 指定字段排序，支持"created_time"-创建时间, "release_time"-发布时间, "expire_time"-过期时间
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: 指定升序/降序,asc-升序,desc-降序
        """
        self.asc = asc

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        pass

