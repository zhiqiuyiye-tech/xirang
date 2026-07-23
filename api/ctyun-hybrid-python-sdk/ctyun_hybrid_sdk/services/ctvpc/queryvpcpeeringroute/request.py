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


class QueryVpcPeeringRouteRequest(CTYunRequest):
    """
    1.16.01版本以后支持该接口
    """

    def __init__(self, request_param):
        super(QueryVpcPeeringRouteRequest, self).__init__("/v4/vpc/vpcpeer/query-peering-route", "POST", "ctvpc", "application/json")
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
        if self.parameters.peering_id is not None:
            body_param["peeringId"] = self.parameters.peering_id
        if self.parameters.network_id is not None:
            body_param["networkId"] = self.parameters.network_id
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.sort is not None:
            body_param["sort"] = self.parameters.sort
        if self.parameters.asc is not None:
            body_param["asc"] = self.parameters.asc
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


class QueryVpcPeeringRouteRequestParam(object):

    def __init__(self, region_id, peering_id, network_id, query_content=None, sort=None, asc=None):
        """
        :param region_id: 资源池id
        :param peering_id: 对等连接ID
        :param network_id: vpc的ID
        :param query_content: 对目的地址进行模糊搜索
        :param sort: 排序字段，使用逗号分隔 只允许【"dstCidr", "nextHop", "orgName", "systemUserCode", "systemUserName", "uuid" 】的字段排序
        :param asc: 排序是否倒序， 1 (升序)or 0(降序)，默认降序
        """
        self.region_id = region_id
        self.peering_id = peering_id
        self.network_id = network_id
        self.query_content = query_content
        self.sort = sort
        self.asc = asc

    def set_query_content(self, query_content):
        """
        :param query_content: 对目的地址进行模糊搜索
        """
        self.query_content = query_content

    def set_sort(self, sort):
        """
        :param sort: 排序字段，使用逗号分隔 只允许【"dstCidr", "nextHop", "orgName", "systemUserCode", "systemUserName", "uuid" 】的字段排序
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: 排序是否倒序， 1 (升序)or 0(降序)，默认降序
        """
        self.asc = asc

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.peering_id is None:
            raise Exception("peering_id can not None")
        if self.network_id is None:
            raise Exception("network_id can not None")

