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


class QueryClusterListRequest(CTYunRequest):
    """
    查询集群列表
    """

    def __init__(self, request_param):
        super(QueryClusterListRequest, self).__init__("/v4/cthpc/list-cluster", "GET", "cthpc", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.cluster_uuid_list is not None:
            query_param["clusterUUIDList"] = self.parameters.cluster_uuid_list
        if self.parameters.cluster_name_list is not None:
            query_param["clusterNameList"] = self.parameters.cluster_name_list
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryClusterListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, cluster_uuid_list=None, cluster_name_list=None):
        """
        :param page_no: 页码，默认值:1，超过50按50处理
        :param page_size: 每页记录数目，默认值:10,超过100按100处理
        :param region_id: 资源池ID
        :param cluster_uuid_list: 集群UUID列表， 多个使用英文逗号分隔
        :param cluster_name_list: 集群名称，多个以逗号分隔
        """
        self.page_no = page_no
        self.page_size = page_size
        self.region_id = region_id
        self.cluster_uuid_list = cluster_uuid_list
        self.cluster_name_list = cluster_name_list

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值:1，超过50按50处理
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，默认值:10,超过100按100处理
        """
        self.page_size = page_size

    def set_cluster_uuid_list(self, cluster_uuid_list):
        """
        :param cluster_uuid_list: 集群UUID列表， 多个使用英文逗号分隔
        """
        self.cluster_uuid_list = cluster_uuid_list

    def set_cluster_name_list(self, cluster_name_list):
        """
        :param cluster_name_list: 集群名称，多个以逗号分隔
        """
        self.cluster_name_list = cluster_name_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

