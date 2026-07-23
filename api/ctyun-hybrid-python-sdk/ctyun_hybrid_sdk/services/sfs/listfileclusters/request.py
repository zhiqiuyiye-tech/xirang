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


class ListFileClustersRequest(CTYunRequest):
    """
    查询文件存储集群列表
    """

    def __init__(self, request_param):
        super(ListFileClustersRequest, self).__init__("/v4/file-storage/list-cluster", "GET", "sfs", "")
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
        if self.parameters.storage_type is not None:
            query_param["storageType"] = self.parameters.storage_type
        if self.parameters.cluster_id is not None:
            query_param["clusterID"] = self.parameters.cluster_id
        if self.parameters.cluster_name is not None:
            query_param["clusterName"] = self.parameters.cluster_name
        if self.parameters.cluster_status is not None:
            query_param["clusterStatus"] = self.parameters.cluster_status
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


class ListFileClustersRequestParam(object):

    def __init__(self, region_id, storage_type=None, cluster_id=None, cluster_name=None, cluster_status=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param storage_type: 查询特定文件存储类型集群
        :param cluster_id: 集群ID, 模糊匹配
        :param cluster_name: 集群名称, 模糊匹配
        :param cluster_status: 集群状态，多个用逗号分隔，1=未售罄，2=已售罄
        :param page_no: 页码，默认值1
        :param page_size: 分页大小，默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.region_id = region_id
        self.storage_type = storage_type
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.cluster_status = cluster_status
        self.page_no = page_no
        self.page_size = page_size

    def set_storage_type(self, storage_type):
        """
        :param storage_type: 查询特定文件存储类型集群
        """
        self.storage_type = storage_type

    def set_cluster_id(self, cluster_id):
        """
        :param cluster_id: 集群ID, 模糊匹配
        """
        self.cluster_id = cluster_id

    def set_cluster_name(self, cluster_name):
        """
        :param cluster_name: 集群名称, 模糊匹配
        """
        self.cluster_name = cluster_name

    def set_cluster_status(self, cluster_status):
        """
        :param cluster_status: 集群状态，多个用逗号分隔，1=未售罄，2=已售罄
        """
        self.cluster_status = cluster_status

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1
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

