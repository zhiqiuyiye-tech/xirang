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


class CdaPhysicalLineAccessPointListRequest(CTYunRequest):
    """
    物理专线接入点查询,请求参数请用JSON格式
    """

    def __init__(self, request_param):
        super(CdaPhysicalLineAccessPointListRequest, self).__init__("/v4/cda/physical-line/access-point-list", "GET", "cda", "")
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
        if self.parameters.line_name is not None:
            query_param["lineName"] = self.parameters.line_name
        if self.parameters.account is not None:
            query_param["account"] = self.parameters.account
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CdaPhysicalLineAccessPointListRequestParam(object):

    def __init__(self, region_id, line_name=None, account=None):
        """
        :param line_name: 物理专线名字
        :param account: 无实际意义
        :param region_id: 资源池id
        """
        self.line_name = line_name
        self.account = account
        self.region_id = region_id

    def set_line_name(self, line_name):
        """
        :param line_name: 物理专线名字
        """
        self.line_name = line_name

    def set_account(self, account):
        """
        :param account: 无实际意义
        """
        self.account = account

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

