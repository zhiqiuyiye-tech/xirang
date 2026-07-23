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


class ListHpfsByClusterRequest(CTYunRequest):
    """
    查询指定集群的并行文件列表
    """

    def __init__(self, request_param):
        super(ListHpfsByClusterRequest, self).__init__("/v4/hpfs/list-sfs-by-cluster", "GET", "hpfs", "")
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
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.cluster_name is not None:
            query_param["clusterName"] = self.parameters.cluster_name
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListHpfsByClusterRequestParam(object):

    def __init__(self, region_id, cluster_name, az_name=None, project_id=None, page_size=None, page_no=None):
        """
        :param region_id: 资源池 ID	
        :param az_name: 可用区名称，多可用区下必填	
        :param cluster_name: 集群名称	
        :param project_id: 资源所属企业项目 ID，默认为"0"	
        :param page_size: 每页包含的元素个数范围(1-100)，默认值为10，大于100取100，不传、传0取10
        :param page_no: 列表的分页页码，默认值为1	
        """
        self.region_id = region_id
        self.az_name = az_name
        self.cluster_name = cluster_name
        self.project_id = project_id
        self.page_size = page_size
        self.page_no = page_no

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，多可用区下必填	
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目 ID，默认为"0"	
        """
        self.project_id = project_id

    def set_page_size(self, page_size):
        """
        :param page_size: 每页包含的元素个数范围(1-100)，默认值为10，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的分页页码，默认值为1	
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cluster_name is None:
            raise Exception("cluster_name can not None")

