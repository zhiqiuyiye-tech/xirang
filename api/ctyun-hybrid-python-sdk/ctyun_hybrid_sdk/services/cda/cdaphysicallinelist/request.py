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


class CdaPhysicalLineListRequest(CTYunRequest):
    """
    请求参数需要使用JSON格式
    """

    def __init__(self, request_param):
        super(CdaPhysicalLineListRequest, self).__init__("/v4/cda/physical-line/list", "GET", "cda", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.account is not None:
            query_param["account"] = self.parameters.account
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CdaPhysicalLineListRequestParam(object):

    def __init__(self, page_no, page_size, region_id, account, type=None):
        """
        :param page_no: 页码
        :param page_size: 每页数量
        :param region_id: 资源池ID
        :param type: 专线类型(PON/IPRAN)
        :param account: 登录云管的账号
        """
        self.page_no = page_no
        self.page_size = page_size
        self.region_id = region_id
        self.type = type
        self.account = account

    def set_type(self, type):
        """
        :param type: 专线类型(PON/IPRAN)
        """
        self.type = type

    def check_param(self):
        """
        the param required check
        """
        if self.page_no is None:
            raise Exception("page_no can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.account is None:
            raise Exception("account can not None")

