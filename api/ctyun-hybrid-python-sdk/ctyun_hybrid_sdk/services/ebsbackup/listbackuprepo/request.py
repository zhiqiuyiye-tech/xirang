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


class ListBackupRepoRequest(CTYunRequest):
    """
    v2版本混合云管对过期状态存储库支持继续使用，故active对应可用状态存储库，expired对应禁用状态存储库   
    2.2.6版本新增支持返回容量告警阈值capacityAlertThreshold
    """

    def __init__(self, request_param):
        super(ListBackupRepoRequest, self).__init__("/v4/ebs-backup/repo/list-repos", "GET", "ebsbackup", "")
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
        if self.parameters.repository_id is not None:
            query_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.repository_name is not None:
            query_param["repositoryName"] = self.parameters.repository_name
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.hide_expire is not None:
            query_param["hideExpire"] = self.parameters.hide_expire
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListBackupRepoRequestParam(object):

    def __init__(self, region_id, repository_id=None, repository_name=None, status=None, query_content=None, hide_expire=None, asc=None, sort=None, project_id=None, page_no=None, page_size=None, resource_id=None):
        """
        :param region_id: 资源池id
        :param repository_id: 云硬盘备份存储库ID，支持模糊匹配
        :param repository_name: 云硬盘备份存储库名称，支持模糊匹配
        :param status: 云硬盘备份存储库状态 active-可用 expired-禁用 暂时只支持两种状态
        :param query_content: 模糊查询，筛选存储库名称或id等于此参数值的存储库
        :param hide_expire: 是否隐藏过期的云硬盘备份库，true-隐藏，false-不隐藏
        :param asc: 和sort配合使用，是否升序排列 true-升序，false-降序，默认为false
        :param sort: 和asc配合使用，指定用于排序的字段 可选字段：createdTime/expiredTime/size/freeSize/repositoryName，默认为createdTime
        :param project_id: 企业项目ID
        :param page_no: 页码，默认1
        :param page_size: 每页记录数目 ,默认10，范围[1-100]，大于100取100，不传、传0取10
        :param resource_id: 资源id,兼容v1,该参数和repositoryID二选一,同时存在时以repositoryID优先
        """
        self.region_id = region_id
        self.repository_id = repository_id
        self.repository_name = repository_name
        self.status = status
        self.query_content = query_content
        self.hide_expire = hide_expire
        self.asc = asc
        self.sort = sort
        self.project_id = project_id
        self.page_no = page_no
        self.page_size = page_size
        self.resource_id = resource_id

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 云硬盘备份存储库ID，支持模糊匹配
        """
        self.repository_id = repository_id

    def set_repository_name(self, repository_name):
        """
        :param repository_name: 云硬盘备份存储库名称，支持模糊匹配
        """
        self.repository_name = repository_name

    def set_status(self, status):
        """
        :param status: 云硬盘备份存储库状态 active-可用 expired-禁用 暂时只支持两种状态
        """
        self.status = status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查询，筛选存储库名称或id等于此参数值的存储库
        """
        self.query_content = query_content

    def set_hide_expire(self, hide_expire):
        """
        :param hide_expire: 是否隐藏过期的云硬盘备份库，true-隐藏，false-不隐藏
        """
        self.hide_expire = hide_expire

    def set_asc(self, asc):
        """
        :param asc: 和sort配合使用，是否升序排列 true-升序，false-降序，默认为false
        """
        self.asc = asc

    def set_sort(self, sort):
        """
        :param sort: 和asc配合使用，指定用于排序的字段 可选字段：createdTime/expiredTime/size/freeSize/repositoryName，默认为createdTime
        """
        self.sort = sort

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目 ,默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id,兼容v1,该参数和repositoryID二选一,同时存在时以repositoryID优先
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

