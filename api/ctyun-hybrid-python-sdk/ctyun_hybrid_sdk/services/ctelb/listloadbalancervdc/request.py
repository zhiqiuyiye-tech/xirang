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


class ListLoadBalancerVdcRequest(CTYunRequest):
    """
    查看负载均衡实例列表
    """

    def __init__(self, request_param):
        super(ListLoadBalancerVdcRequest, self).__init__("/v4/elb/list-loadbalancer-vdc", "GET", "ctelb", "")
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
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        if self.parameters.resource_type is not None:
            query_param["resourceType"] = self.parameters.resource_type
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.ignore_channel is not None:
            query_param["ignoreChannel"] = self.parameters.ignore_channel
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListLoadBalancerVdcRequestParam(object):

    def __init__(self, region_id, ids=None, resource_type=None, name=None, subnet_id=None, ignore_channel=None, org_id=None):
        """
        :param region_id: 区域ID
        :param ids: 负载均衡ID列表，以","分隔
        :param resource_type: 资源类型。internal：内网负载均衡，external：公网负载均衡
        :param name: 名称
        :param subnet_id: 子网id
        :param ignore_channel: 默认不传：查全渠道资源；false：仅查询paas创建;  true:仅查界面创建，私有扩展
        :param org_id: 组织id
        """
        self.region_id = region_id
        self.ids = ids
        self.resource_type = resource_type
        self.name = name
        self.subnet_id = subnet_id
        self.ignore_channel = ignore_channel
        self.org_id = org_id

    def set_ids(self, ids):
        """
        :param ids: 负载均衡ID列表，以","分隔
        """
        self.ids = ids

    def set_resource_type(self, resource_type):
        """
        :param resource_type: 资源类型。internal：内网负载均衡，external：公网负载均衡
        """
        self.resource_type = resource_type

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网id
        """
        self.subnet_id = subnet_id

    def set_ignore_channel(self, ignore_channel):
        """
        :param ignore_channel: 默认不传：查全渠道资源；false：仅查询paas创建;  true:仅查界面创建，私有扩展
        """
        self.ignore_channel = ignore_channel

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

