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


class UserPageListHybridRequest(CTYunRequest):
    """
    分页查询用户信息，需要注意v2 的openapi 子账号和主账号获取的资源是重复的，主账号有当前vdc下所有资源的权限，如果使用用户id获取资源只需要是用主账号即可，主子账号及企业账号使用请求返回值 userType 判断即可
    """

    def __init__(self, request_param):
        super(UserPageListHybridRequest, self).__init__("/v4/user/page-user-list", "GET", "user", "")
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
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_num is not None:
            query_param["pageNum"] = self.parameters.page_num
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class UserPageListHybridRequestParam(object):

    def __init__(self, page_size=None, page_num=None):
        """
        :param page_size: 页面内容个数，默认为10,单页最大记录不超过100
        :param page_num: 页码，默认为1
        """
        self.page_size = page_size
        self.page_num = page_num

    def set_page_size(self, page_size):
        """
        :param page_size: 页面内容个数，默认为10,单页最大记录不超过100
        """
        self.page_size = page_size

    def set_page_num(self, page_num):
        """
        :param page_num: 页码，默认为1
        """
        self.page_num = page_num

    def check_param(self):
        """
        the param required check
        """
        pass

