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


class CreateInstanceBackupRequest(CTYunRequest):
    """
    创建云主机备份   
    底层暂时支持返回：创建备份对应的异步任务uuid
    """

    def __init__(self, request_param):
        super(CreateInstanceBackupRequest, self).__init__("/v4/ecs/backup-create", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.repository_id is not None:
            body_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.force_consistency_backup is not None:
            body_param["forceConsistencyBackup"] = self.parameters.force_consistency_backup
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


class CreateInstanceBackupRequestParam(object):

    def __init__(self, region_id, id, name, repository_id, az_name=None, description=None, force_consistency_backup=None):
        """
        :param region_id: 资源id
        :param az_name: 可用区名称
        :param id: 云主机ID
        :param name: 备份名称。满足以下规则：以大小写字母开头，可包含数字，‘_’或‘-’，长度为2-63字符 注：在所有资源池不可重复。
        :param description: 云主机备份描述。长度不超过128字符。
        :param repository_id: 存储库ID
        :param force_consistency_backup: 是否强制创建一致性的备份-暂未提供，需确认调整
        """
        self.region_id = region_id
        self.az_name = az_name
        self.id = id
        self.name = name
        self.description = description
        self.repository_id = repository_id
        self.force_consistency_backup = force_consistency_backup

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_description(self, description):
        """
        :param description: 云主机备份描述。长度不超过128字符。
        """
        self.description = description

    def set_force_consistency_backup(self, force_consistency_backup):
        """
        :param force_consistency_backup: 是否强制创建一致性的备份-暂未提供，需确认调整
        """
        self.force_consistency_backup = force_consistency_backup

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.repository_id is None:
            raise Exception("repository_id can not None")

