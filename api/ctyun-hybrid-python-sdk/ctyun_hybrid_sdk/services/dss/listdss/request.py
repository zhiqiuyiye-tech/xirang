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


class ListDssRequest(CTYunRequest):
    """
    查询块存储专属集群
    """

    def __init__(self, request_param):
        super(ListDssRequest, self).__init__("/v4/dss/list", "GET", "dss", "")
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
        if self.parameters.az_id is not None:
            query_param["azID"] = self.parameters.az_id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.dss_id is not None:
            query_param["dssID"] = self.parameters.dss_id
        if self.parameters.cluster_type is not None:
            query_param["clusterType"] = self.parameters.cluster_type
        if self.parameters.cluster_status is not None:
            query_param["clusterStatus"] = self.parameters.cluster_status
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


class ListDssRequestParam(object):

    def __init__(self, region_id, az_id=None, name=None, dss_id=None, cluster_type=None, cluster_status=None, page=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param az_id: 可用区ID
        :param name: 集群名称
        :param dss_id: 集群ID
        :param cluster_type: 群类型. HDD/SSD， 多个用逗号分隔
        :param cluster_status: 集群状态. 1-未售罄，2-已售罄,多个用逗号分隔
        :param page: 页码
        :param page_size: 
        """
        self.region_id = region_id
        self.az_id = az_id
        self.name = name
        self.dss_id = dss_id
        self.cluster_type = cluster_type
        self.cluster_status = cluster_status
        self.page = page
        self.page_size = page_size

    def set_az_id(self, az_id):
        """
        :param az_id: 可用区ID
        """
        self.az_id = az_id

    def set_name(self, name):
        """
        :param name: 集群名称
        """
        self.name = name

    def set_dss_id(self, dss_id):
        """
        :param dss_id: 集群ID
        """
        self.dss_id = dss_id

    def set_cluster_type(self, cluster_type):
        """
        :param cluster_type: 群类型. HDD/SSD， 多个用逗号分隔
        """
        self.cluster_type = cluster_type

    def set_cluster_status(self, cluster_status):
        """
        :param cluster_status: 集群状态. 1-未售罄，2-已售罄,多个用逗号分隔
        """
        self.cluster_status = cluster_status

    def set_page(self, page):
        """
        :param page: 页码
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

