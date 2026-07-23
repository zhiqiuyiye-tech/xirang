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


class CdaVpcDeleteRequest(CTYunRequest):
    """
    专线网关删除VPC
    """

    def __init__(self, request_param):
        super(CdaVpcDeleteRequest, self).__init__("/v4/cda/vpc/delete", "POST", "cda", "application/json")
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
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
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


class CdaVpcDeleteRequestParam(object):

    def __init__(self, vpc_id, gateway_name, region_id=None, account=None, resource_pool=None):
        """
        :param region_id: 资源池ID,无实际意义
        :param vpc_id: VPC ID
        :param account: 云管账号，无实际意义
        :param resource_pool: 资源池信息ID无实际意义
        :param gateway_name: 专线网关名称
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.account = account
        self.resource_pool = resource_pool
        self.gateway_name = gateway_name

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID,无实际意义
        """
        self.region_id = region_id

    def set_account(self, account):
        """
        :param account: 云管账号，无实际意义
        """
        self.account = account

    def set_resource_pool(self, resource_pool):
        """
        :param resource_pool: 资源池信息ID无实际意义
        """
        self.resource_pool = resource_pool

    def check_param(self):
        """
        the param required check
        """
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")

