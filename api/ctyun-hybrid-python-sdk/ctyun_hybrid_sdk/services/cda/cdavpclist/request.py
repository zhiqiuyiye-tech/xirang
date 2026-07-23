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


class CdaVpcListRequest(CTYunRequest):
    """
    专线网关VPC查询,请求参数需要使用JSON格式
    """

    def __init__(self, request_param):
        super(CdaVpcListRequest, self).__init__("/v4/cda/vpc/list", "GET", "cda", "")
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
        if self.parameters.account is not None:
            query_param["account"] = self.parameters.account
        if self.parameters.gateway_name is not None:
            query_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CdaVpcListRequestParam(object):

    def __init__(self, gateway_name, region_id, account=None):
        """
        :param account: 无实际意义
        :param gateway_name: 网关名称
        :param region_id: 资源池ID
        """
        self.account = account
        self.gateway_name = gateway_name
        self.region_id = region_id

    def set_account(self, account):
        """
        :param account: 无实际意义
        """
        self.account = account

    def check_param(self):
        """
        the param required check
        """
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

