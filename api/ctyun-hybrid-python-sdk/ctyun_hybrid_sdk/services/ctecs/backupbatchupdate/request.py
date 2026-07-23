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


class BackupBatchUpdateRequest(CTYunRequest):
    """
    批量更改云主机备份名称和描述
    """

    def __init__(self, request_param):
        super(BackupBatchUpdateRequest, self).__init__("/v4/ecs/backup/batch-update", "POST", "ctecs", "application/json")
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
        if self.parameters.update_info is not None:
            update_info = []
            if isinstance(self.parameters.update_info, list):
                for item in self.parameters.update_info:
                    if type(item) is dict:
                        update_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        update_info.append(item_dict_value)
            else:
                update_info.append(self.parameters.update_info.get_dic())
            body_param["updateInfo"] = update_info
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


class UpdateInfo(object):

    def __init__(self, instance_backup_id, instance_backup_name=None, instance_backup_description=None):
        """
        :param instance_backup_id: 备份id
        :param instance_backup_name: 云主机备份名称。满足以下规则：以大小写字母开头，可包含数字，‘_’或‘-’，长度为2-63字符 注：在所有资源池不可重复（instanceBackupName与instanceBackupDescription参数至少需要二选一）（空串视为没传）
        :param instance_backup_description: 云主机备份描述。长度不超过128字符。（instanceBackupName与instanceBackupDescription参数至少需要二选一）（空串视为没传）
        """
        self.instance_backup_id = instance_backup_id
        self.instance_backup_name = instance_backup_name
        self.instance_backup_description = instance_backup_description
        self.check_param()

    def set_instance_backup_name(self, instance_backup_name):
        """
        :param instance_backup_name: 云主机备份名称。满足以下规则：以大小写字母开头，可包含数字，‘_’或‘-’，长度为2-63字符 注：在所有资源池不可重复（instanceBackupName与instanceBackupDescription参数至少需要二选一）（空串视为没传）
        """
        self.instance_backup_name = instance_backup_name

    def set_instance_backup_description(self, instance_backup_description):
        """
        :param instance_backup_description: 云主机备份描述。长度不超过128字符。（instanceBackupName与instanceBackupDescription参数至少需要二选一）（空串视为没传）
        """
        self.instance_backup_description = instance_backup_description

    def get_dic(self):
        obj_dict = dict()
        if self.instance_backup_id is not None:
            obj_dict["instanceBackupID"] = self.instance_backup_id
        if self.instance_backup_name is not None:
            obj_dict["instanceBackupName"] = self.instance_backup_name
        if self.instance_backup_description is not None:
            obj_dict["instanceBackupDescription"] = self.instance_backup_description
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.instance_backup_id is None:
            raise Exception("instance_backup_id can not None")


class BackupBatchUpdateRequestParam(object):

    def __init__(self, region_id, update_info, ):
        """
        :param region_id: 资源池ID
        :param update_info: 更新信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.update_info = update_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.update_info is None:
            raise Exception("update_info can not None")

