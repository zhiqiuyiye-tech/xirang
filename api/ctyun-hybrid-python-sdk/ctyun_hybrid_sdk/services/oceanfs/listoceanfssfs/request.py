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


class ListOceanfsSfsRequest(CTYunRequest):
    """
    海量文件列表查询
    """

    def __init__(self, request_param):
        super(ListOceanfsSfsRequest, self).__init__("/v4/oceanfs/list-sfs", "GET", "oceanfs", "")
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
        if self.parameters.sfs_status is not None:
            query_param["sfsStatus"] = self.parameters.sfs_status
        if self.parameters.sfs_protocol is not None:
            query_param["sfsProtocol"] = self.parameters.sfs_protocol
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListOceanfsSfsRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, sfs_status=None, sfs_protocol=None, project_id=None, resource_id=None):
        """
        :param page_no: 列表的分页页码,默认1
        :param page_size: 每页包含的元素个数范围(1-100)，大于100取100，不传、传0取10
        :param region_id: 资源池id
        :param sfs_status: 海量文件状态。creating/available/unusable，不传为查询全部
        :param sfs_protocol: 挂载协议。3 种，nfs/cifs/oceanfs ，不传为查询全部
        :param project_id: 资源所属企业项目 ID
        :param resource_id: 资源id(支持id和uuid)
        """
        self.page_no = page_no
        self.page_size = page_size
        self.region_id = region_id
        self.sfs_status = sfs_status
        self.sfs_protocol = sfs_protocol
        self.project_id = project_id
        self.resource_id = resource_id

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的分页页码,默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页包含的元素个数范围(1-100)，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_sfs_status(self, sfs_status):
        """
        :param sfs_status: 海量文件状态。creating/available/unusable，不传为查询全部
        """
        self.sfs_status = sfs_status

    def set_sfs_protocol(self, sfs_protocol):
        """
        :param sfs_protocol: 挂载协议。3 种，nfs/cifs/oceanfs ，不传为查询全部
        """
        self.sfs_protocol = sfs_protocol

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目 ID
        """
        self.project_id = project_id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id(支持id和uuid)
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

