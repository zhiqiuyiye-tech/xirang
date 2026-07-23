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


class ListEbsBackupVdcRequest(CTYunRequest):
    """
    查询云硬盘备份列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
    """

    def __init__(self, request_param):
        super(ListEbsBackupVdcRequest, self).__init__("/v4/ebs-backup/list-vdc", "GET", "ebsbackup", "")
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
        if self.parameters.volume_id is not None:
            query_param["volumeID"] = self.parameters.volume_id
        if self.parameters.volume_name is not None:
            query_param["volumeName"] = self.parameters.volume_name
        if self.parameters.backup_name is not None:
            query_param["backupName"] = self.parameters.backup_name
        if self.parameters.repository_id is not None:
            query_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEbsBackupVdcRequestParam(object):

    def __init__(self, region_id, volume_id=None, volume_name=None, backup_name=None, repository_id=None, status=None, query_content=None, org_id=None):
        """
        :param region_id: 资源池id
        :param volume_id: 云硬盘ID，模糊查询
        :param volume_name: 云硬盘名称，模糊查询
        :param backup_name: 云硬盘备份名称，模糊查询
        :param repository_id: 存储库id，模糊查询
        :param status: 云硬盘备份状态，根据备份状态进行筛选，creating-创建中, available-可用, deleting-删除中，error-异常, restoring-恢复中, error_deleting-删除异常
        :param query_content: 模糊查找内容，根据云硬盘ID/云硬盘名称/备份ID/备份名称进行筛选
        :param org_id: 组织id   
         
        """
        self.region_id = region_id
        self.volume_id = volume_id
        self.volume_name = volume_name
        self.backup_name = backup_name
        self.repository_id = repository_id
        self.status = status
        self.query_content = query_content
        self.org_id = org_id

    def set_volume_id(self, volume_id):
        """
        :param volume_id: 云硬盘ID，模糊查询
        """
        self.volume_id = volume_id

    def set_volume_name(self, volume_name):
        """
        :param volume_name: 云硬盘名称，模糊查询
        """
        self.volume_name = volume_name

    def set_backup_name(self, backup_name):
        """
        :param backup_name: 云硬盘备份名称，模糊查询
        """
        self.backup_name = backup_name

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 存储库id，模糊查询
        """
        self.repository_id = repository_id

    def set_status(self, status):
        """
        :param status: 云硬盘备份状态，根据备份状态进行筛选，creating-创建中, available-可用, deleting-删除中，error-异常, restoring-恢复中, error_deleting-删除异常
        """
        self.status = status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查找内容，根据云硬盘ID/云硬盘名称/备份ID/备份名称进行筛选
        """
        self.query_content = query_content

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

