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


class GetClusterThresholdHybridRequest(CTYunRequest):
    """
    查询集群容量阈值
    """

    def __init__(self, request_param):
        super(GetClusterThresholdHybridRequest, self).__init__("/v4/monitor/get-cluster-threshold", "GET", "monitor", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.item_name is not None:
            query_param["itemName"] = self.parameters.item_name
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetClusterThresholdHybridRequestParam(object):

    def __init__(self, region_id, name=None, item_name=None, type=None, page=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param name: 集群名称
        :param item_name: 集群指标 cpu_allocated_rate：CPU分配率，memory_allocated_rate内存分配率，alloc_rate存储分配率。查询多个逗号分隔
        :param type: 集群类型 compute_cluster：计算集群，storage_cluster：存储集群
        :param page: 页码，默认为1
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.region_id = region_id
        self.name = name
        self.item_name = item_name
        self.type = type
        self.page = page
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 集群名称
        """
        self.name = name

    def set_item_name(self, item_name):
        """
        :param item_name: 集群指标 cpu_allocated_rate：CPU分配率，memory_allocated_rate内存分配率，alloc_rate存储分配率。查询多个逗号分隔
        """
        self.item_name = item_name

    def set_type(self, type):
        """
        :param type: 集群类型 compute_cluster：计算集群，storage_cluster：存储集群
        """
        self.type = type

    def set_page(self, page):
        """
        :param page: 页码，默认为1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

