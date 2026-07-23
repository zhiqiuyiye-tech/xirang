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


class IpsecVPNConnectionQueryRequest(CTYunRequest):
    """
    GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
    """

    def __init__(self, request_param):
        super(IpsecVPNConnectionQueryRequest, self).__init__("/v4/vpn/ipsec-vpn-connection/list", "GET", "ctvpn", "")
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
        if self.parameters.vpn_connection_id is not None:
            query_param["vpnConnectionID"] = self.parameters.vpn_connection_id
        if self.parameters.vpn_connection_name is not None:
            query_param["vpnConnectionName"] = self.parameters.vpn_connection_name
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IpsecVPNConnectionQueryRequestParam(object):

    def __init__(self, region_id, vpn_connection_id=None, vpn_connection_name=None, query_content=None, page_size=None, page_no=None):
        """
        :param region_id: 资源池id
        :param vpn_connection_id: vpn连接id
        :param vpn_connection_name: vpn连接名称
        :param query_content: 模糊搜索，支持名称和id
        :param page_size: 页面大小，输入0 或者-1默认为10处理
        :param page_no: 页码-公有云，输入0 或者-1默认为1处理
        """
        self.region_id = region_id
        self.vpn_connection_id = vpn_connection_id
        self.vpn_connection_name = vpn_connection_name
        self.query_content = query_content
        self.page_size = page_size
        self.page_no = page_no

    def set_vpn_connection_id(self, vpn_connection_id):
        """
        :param vpn_connection_id: vpn连接id
        """
        self.vpn_connection_id = vpn_connection_id

    def set_vpn_connection_name(self, vpn_connection_name):
        """
        :param vpn_connection_name: vpn连接名称
        """
        self.vpn_connection_name = vpn_connection_name

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索，支持名称和id
        """
        self.query_content = query_content

    def set_page_size(self, page_size):
        """
        :param page_size: 页面大小，输入0 或者-1默认为10处理
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码-公有云，输入0 或者-1默认为1处理
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

