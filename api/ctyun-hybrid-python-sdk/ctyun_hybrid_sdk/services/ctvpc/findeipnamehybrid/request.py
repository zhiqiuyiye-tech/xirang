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


class FindEIPNameHybridRequest(CTYunRequest):
    """
    EIP网关列表查询
    """

    def __init__(self, request_param):
        super(FindEIPNameHybridRequest, self).__init__("/v4/eip/EIPGroup/findEIPName", "GET", "ctvpc", "")
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
        if self.parameters.page_num is not None:
            query_param["pageNum"] = self.parameters.page_num
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.floating_name is not None:
            query_param["floatingName"] = self.parameters.floating_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class FindEIPNameHybridRequestParam(object):

    def __init__(self, region_id, page_num=None, page_size=None, floating_name=None):
        """
        :param region_id: 资源池ID
        :param page_num: 页码，0或不传为默认值:1
        :param page_size: 每页记录数目，取值范围:[1~100]，0或不传为默认值:10，超过100默认为100
        :param floating_name: EIP组名称
        """
        self.region_id = region_id
        self.page_num = page_num
        self.page_size = page_size
        self.floating_name = floating_name

    def set_page_num(self, page_num):
        """
        :param page_num: 页码，0或不传为默认值:1
        """
        self.page_num = page_num

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围:[1~100]，0或不传为默认值:10，超过100默认为100
        """
        self.page_size = page_size

    def set_floating_name(self, floating_name):
        """
        :param floating_name: EIP组名称
        """
        self.floating_name = floating_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

