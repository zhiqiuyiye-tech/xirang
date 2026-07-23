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


class GetVpcSharedProjectsOpenapiRequest(CTYunRequest):
    """
    查询vpc共享的企业项目列表
    """

    def __init__(self, request_param):
        super(GetVpcSharedProjectsOpenapiRequest, self).__init__("/v4/vpc/shared-project-list", "GET", "ctvpc", "")
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
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetVpcSharedProjectsOpenapiRequestParam(object):

    def __init__(self, vpc_id=None, region_id=None):
        """
        :param vpc_id: vpc id
        :param region_id: 资源池id
        """
        self.vpc_id = vpc_id
        self.region_id = region_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc id
        """
        self.vpc_id = vpc_id

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池id
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        pass

