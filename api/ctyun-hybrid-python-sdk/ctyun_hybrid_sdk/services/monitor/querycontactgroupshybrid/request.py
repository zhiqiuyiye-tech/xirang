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


class QueryContactGroupsHybridRequest(CTYunRequest):
    """
    调用此接口可查询告警联系人组的列表。
    """

    def __init__(self, request_param):
        super(QueryContactGroupsHybridRequest, self).__init__("/v4.1/monitor/query-contact-groups", "POST", "monitor", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.search is not None:
            body_param["search"] = self.parameters.search
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class QueryContactGroupsHybridRequestParam(object):

    def __init__(self, region_id, name=None, search=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID（混合云必须）
        :param name: 组名
        :param search: 模糊搜索，可搜索字段为联系人的：告警联系组组名（name）、告警联系人姓名（name）、告警联系人手机号（phone）、告警联系人邮箱（email）	
        :param page_no: 页码，0或不传默认值:1，小于0时报错
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.region_id = region_id
        self.name = name
        self.search = search
        self.page_no = page_no
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 组名
        """
        self.name = name

    def set_search(self, search):
        """
        :param search: 模糊搜索，可搜索字段为联系人的：告警联系组组名（name）、告警联系人姓名（name）、告警联系人手机号（phone）、告警联系人邮箱（email）	
        """
        self.search = search

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，0或不传默认值:1，小于0时报错
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

