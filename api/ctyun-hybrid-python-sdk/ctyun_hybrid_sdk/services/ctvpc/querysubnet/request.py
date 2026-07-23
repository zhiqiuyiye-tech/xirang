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


class QuerySubnetRequest(CTYunRequest):
    """
    查询用户专有网络 VPC 下子网详情。   
    ## 接口约束   
    * 公有云没有azName字段，非必填字段，暂不做调整
    """

    def __init__(self, request_param):
        super(QuerySubnetRequest, self).__init__("/v4/vpc/query-subnet", "GET", "ctvpc", "")
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
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QuerySubnetRequestParam(object):

    def __init__(self, region_id, subnet_id, az_name=None):
        """
        :param region_id: 资源池 ID   
         
        :param subnet_id: 子网id
        :param az_name: 可用区名称（差异点说明：2.0对齐公有云文档，无此参数）
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（差异点说明：2.0对齐公有云文档，无此参数）
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

