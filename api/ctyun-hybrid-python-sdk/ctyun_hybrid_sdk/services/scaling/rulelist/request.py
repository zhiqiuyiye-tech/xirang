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


class RuleListRequest(CTYunRequest):
    """
    查询弹性伸缩组内的策略列表
    """

    def __init__(self, request_param):
        super(RuleListRequest, self).__init__("/v4/scaling/rule/list", "POST", "scaling", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class RuleListRequestParam(object):

    def __init__(self, region_id, group_id, page=None, page_size=None, page_no=None):
        """
        :param region_id: 资源池ID 
        :param group_id: 伸缩组ID
        :param page: 页码,建议使用pageNo，该参数后续会下线 
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param page_no: 页码
        """
        self.region_id = region_id
        self.group_id = group_id
        self.page = page
        self.page_size = page_size
        self.page_no = page_no

    def set_page(self, page):
        """
        :param page: 页码,建议使用pageNo，该参数后续会下线 
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

