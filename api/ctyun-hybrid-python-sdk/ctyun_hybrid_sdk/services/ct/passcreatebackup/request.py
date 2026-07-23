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


class PassCreateBackupRequest(CTYunRequest):
    """
    开发未对齐原因：混合云返回异步任务ID，公有云返回云硬盘备份对象
    """

    def __init__(self, request_param):
        super(PassCreateBackupRequest, self).__init__("/v4/paas/ebs-backup/create-backup", "POST", "ct", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.repository_id is not None:
            body_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.backup_name is not None:
            body_param["backupName"] = self.parameters.backup_name
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class PassCreateBackupRequestParam(object):

    def __init__(self, region_id, disk_id, repository_id, backup_name, description=None):
        """
        :param region_id: 资源池id
        :param disk_id: 云硬盘ID
        :param description: 云硬盘备份描述
        :param repository_id: 备份存储库ID
        :param backup_name: 备份名称，长度为 2~63个字符，只能由数字、字母、-、_ 组成，不能以数字、-、_ 开头
        """
        self.region_id = region_id
        self.disk_id = disk_id
        self.description = description
        self.repository_id = repository_id
        self.backup_name = backup_name

    def set_description(self, description):
        """
        :param description: 云硬盘备份描述
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")
        if self.repository_id is None:
            raise Exception("repository_id can not None")
        if self.backup_name is None:
            raise Exception("backup_name can not None")

