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


class ListShieldRuleHybridRequest(CTYunRequest):
    """
    查询告警屏蔽规则列表
    """

    def __init__(self, request_param):
        super(ListShieldRuleHybridRequest, self).__init__("/v4/monitor/list-shield-rule", "GET", "monitor", "")
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
        if self.parameters.creator is not None:
            query_param["creator"] = self.parameters.creator
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListShieldRuleHybridRequestParam(object):

    def __init__(self, region_id, page=None, page_size=None, name=None, creator=None):
        """
        :param region_id: 资源池ID
        :param page: 页码，默认为1
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        :param name: 告警屏蔽规则名称（模糊匹配）
        :param creator: 告警屏蔽规则创建人（模糊匹配）
        """
        self.region_id = region_id
        self.page = page
        self.page_size = page_size
        self.name = name
        self.creator = creator

    def set_page(self, page):
        """
        :param page: 页码，默认为1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 告警屏蔽规则名称（模糊匹配）
        """
        self.name = name

    def set_creator(self, creator):
        """
        :param creator: 告警屏蔽规则创建人（模糊匹配）
        """
        self.creator = creator

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

