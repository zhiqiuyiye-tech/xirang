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


class ListBlockClusterNodesRequest(CTYunRequest):
    """
    查询块存储集群存储节点列表
    """

    def __init__(self, request_param):
        super(ListBlockClusterNodesRequest, self).__init__("/v4/block-storage/list-node", "GET", "ebs", "")
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
        if self.parameters.cluster_id is not None:
            query_param["clusterID"] = self.parameters.cluster_id
        if self.parameters.pool_id is not None:
            query_param["poolID"] = self.parameters.pool_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListBlockClusterNodesRequestParam(object):

    def __init__(self, region_id, cluster_id=None, pool_id=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param cluster_id: 集群ID, 多个用逗号分隔。
        :param pool_id: 存储池ID, 多个用逗号分隔。
        :param page_no: 页码
        :param page_size: 分页大小，默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.region_id = region_id
        self.cluster_id = cluster_id
        self.pool_id = pool_id
        self.page_no = page_no
        self.page_size = page_size

    def set_cluster_id(self, cluster_id):
        """
        :param cluster_id: 集群ID, 多个用逗号分隔。
        """
        self.cluster_id = cluster_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 存储池ID, 多个用逗号分隔。
        """
        self.pool_id = pool_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小，默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

