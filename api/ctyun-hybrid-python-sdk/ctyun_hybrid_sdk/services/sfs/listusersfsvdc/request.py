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


class ListUserSfsVdcRequest(CTYunRequest):
    """
    可用区账户弹性文件列表查询-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
    """

    def __init__(self, request_param):
        super(ListUserSfsVdcRequest, self).__init__("/v4/sfs/list-sfs-vdc", "GET", "sfs", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListUserSfsVdcRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, project_id=None, org_id=None):
        """
        :param region_id: 资源池ID
        :param page_no: 当前页码，默认1
        :param page_size: 每页条数，默认10，取值范围[1-100]，大于100取100，不传、传0取10
        :param project_id: 资源所属企业项目ID
        :param org_id: 组织id   
         
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.project_id = project_id
        self.org_id = org_id

    def set_page_no(self, page_no):
        """
        :param page_no: 当前页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页条数，默认10，取值范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目ID
        """
        self.project_id = project_id

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

