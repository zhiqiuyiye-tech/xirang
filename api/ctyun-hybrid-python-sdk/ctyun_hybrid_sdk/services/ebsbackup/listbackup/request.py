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


class ListBackupRequest(CTYunRequest):
    """
    目前 diskType(云硬盘类型) 底层返回和公有云文档对不齐   
    encrypted（云硬盘是否加密）底层没有该字段无法对齐
    """

    def __init__(self, request_param):
        super(ListBackupRequest, self).__init__("/v4/ebs-backup/list-backups", "GET", "ebsbackup", "")
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
        if self.parameters.disk_id is not None:
            query_param["diskID"] = self.parameters.disk_id
        if self.parameters.disk_name is not None:
            query_param["diskName"] = self.parameters.disk_name
        if self.parameters.backup_name is not None:
            query_param["backupName"] = self.parameters.backup_name
        if self.parameters.repository_id is not None:
            query_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.backup_status is not None:
            query_param["backupStatus"] = self.parameters.backup_status
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.backup_id is not None:
            query_param["backupID"] = self.parameters.backup_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListBackupRequestParam(object):

    def __init__(self, region_id, disk_id=None, disk_name=None, backup_name=None, repository_id=None, backup_status=None, query_content=None, page_no=None, page_size=None, project_id=None, backup_id=None):
        """
        :param region_id: 资源池id
        :param disk_id: 云硬盘ID,支持模糊过滤
        :param disk_name: 云硬盘名称,支持模糊过滤
        :param backup_name: 云硬盘备份名称,支持模糊过滤
        :param repository_id: 根据存储库id进行筛选,支持模糊过滤
        :param backup_status: 根据备份状态进行筛选，creating-创建中, available-可用, deleting-删除中，error-异常, restoring-恢复中, error_deleting-删除异常
        :param query_content: 模糊查找，该参数可用于模糊过滤 云硬盘ID/云硬盘名称/备份ID/备份名称，即上述4个字段如果包含该参数的值，则会被过滤出来
        :param page_no: 页码，默认1
        :param page_size: 每页记录数目 ,默认10，范围[1-100]，大于100取100，不传、传0取10
        :param project_id: 企业项目ID
        :param backup_id: 云硬盘备份ID，精确查找
        """
        self.region_id = region_id
        self.disk_id = disk_id
        self.disk_name = disk_name
        self.backup_name = backup_name
        self.repository_id = repository_id
        self.backup_status = backup_status
        self.query_content = query_content
        self.page_no = page_no
        self.page_size = page_size
        self.project_id = project_id
        self.backup_id = backup_id

    def set_disk_id(self, disk_id):
        """
        :param disk_id: 云硬盘ID,支持模糊过滤
        """
        self.disk_id = disk_id

    def set_disk_name(self, disk_name):
        """
        :param disk_name: 云硬盘名称,支持模糊过滤
        """
        self.disk_name = disk_name

    def set_backup_name(self, backup_name):
        """
        :param backup_name: 云硬盘备份名称,支持模糊过滤
        """
        self.backup_name = backup_name

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 根据存储库id进行筛选,支持模糊过滤
        """
        self.repository_id = repository_id

    def set_backup_status(self, backup_status):
        """
        :param backup_status: 根据备份状态进行筛选，creating-创建中, available-可用, deleting-删除中，error-异常, restoring-恢复中, error_deleting-删除异常
        """
        self.backup_status = backup_status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查找，该参数可用于模糊过滤 云硬盘ID/云硬盘名称/备份ID/备份名称，即上述4个字段如果包含该参数的值，则会被过滤出来
        """
        self.query_content = query_content

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

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_backup_id(self, backup_id):
        """
        :param backup_id: 云硬盘备份ID，精确查找
        """
        self.backup_id = backup_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

