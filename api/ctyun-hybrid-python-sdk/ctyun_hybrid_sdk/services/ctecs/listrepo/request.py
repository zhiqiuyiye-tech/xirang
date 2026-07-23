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


class ListRepoRequest(CTYunRequest):
    """
    查询云主机备份详情   
    
    """

    def __init__(self, request_param):
        super(ListRepoRequest, self).__init__("/v4/ecs/backup-repo/list", "GET", "ctecs", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.repository_name is not None:
            query_param["repositoryName"] = self.parameters.repository_name
        if self.parameters.repository_id is not None:
            query_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.resource_id is not None:
            query_param["resourceId"] = self.parameters.resource_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListRepoRequestParam(object):

    def __init__(self, region_id, project_id=None, repository_name=None, repository_id=None, status=None, page_no=None, page_size=None, resource_id=None):
        """
        :param region_id: 资源id
        :param project_id: 企业项目ID，暂不支持
        :param repository_name: 存储库名称
        :param repository_id: 存储库ID
        :param status: 存储库状态
        :param page_no: 页码，取值范围：大于等于1，默认值为1
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param resource_id: 资源id
        """
        self.region_id = region_id
        self.project_id = project_id
        self.repository_name = repository_name
        self.repository_id = repository_id
        self.status = status
        self.page_no = page_no
        self.page_size = page_size
        self.resource_id = resource_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，暂不支持
        """
        self.project_id = project_id

    def set_repository_name(self, repository_name):
        """
        :param repository_name: 存储库名称
        """
        self.repository_name = repository_name

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 存储库ID
        """
        self.repository_id = repository_id

    def set_status(self, status):
        """
        :param status: 存储库状态
        """
        self.status = status

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：大于等于1，默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

