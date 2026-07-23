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


class CtvpnConnectionListRequest(CTYunRequest):
    """
    GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
    """

    def __init__(self, request_param):
        super(CtvpnConnectionListRequest, self).__init__("/v4/vpn/connection/list", "GET", "ctvpn", "")
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
        if self.parameters.id is not None:
            query_param["ID"] = self.parameters.id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.customer_id is not None:
            query_param["customerID"] = self.parameters.customer_id
        if self.parameters.ct_user_id is not None:
            query_param["ctUserId"] = self.parameters.ct_user_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CtvpnConnectionListRequestParam(object):

    def __init__(self, region_id, id=None, name=None, query_content=None, page=None, page_size=None, customer_id=None, ct_user_id=None):
        """
        :param region_id: 资源池id
        :param id: vpn连接id
        :param name: vpn连接名称
        :param query_content: 模糊搜索，支持名称和id
        :param page: 页码
        :param page_size: 页面大小
        :param customer_id: 租户id，1.0入参，无实际作用
        :param ct_user_id: 用户id，1.0入参，无实际作用
        """
        self.region_id = region_id
        self.id = id
        self.name = name
        self.query_content = query_content
        self.page = page
        self.page_size = page_size
        self.customer_id = customer_id
        self.ct_user_id = ct_user_id

    def set_id(self, id):
        """
        :param id: vpn连接id
        """
        self.id = id

    def set_name(self, name):
        """
        :param name: vpn连接名称
        """
        self.name = name

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索，支持名称和id
        """
        self.query_content = query_content

    def set_page(self, page):
        """
        :param page: 页码
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页面大小
        """
        self.page_size = page_size

    def set_customer_id(self, customer_id):
        """
        :param customer_id: 租户id，1.0入参，无实际作用
        """
        self.customer_id = customer_id

    def set_ct_user_id(self, ct_user_id):
        """
        :param ct_user_id: 用户id，1.0入参，无实际作用
        """
        self.ct_user_id = ct_user_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

