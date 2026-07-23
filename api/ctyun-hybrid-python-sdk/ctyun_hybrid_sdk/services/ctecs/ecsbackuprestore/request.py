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


class EcsBackupRestoreRequest(CTYunRequest):
    """
    恢复云主机备份到源云主机实例   
       
    底层暂时只支持返回：云主机备份恢复对应的异步任务uuid
    """

    def __init__(self, request_param):
        super(EcsBackupRestoreRequest, self).__init__("/v4/ecs/backup-restore", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_backup_id is not None:
            body_param["instanceBackupID"] = self.parameters.instance_backup_id
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


class EcsBackupRestoreRequestParam(object):

    def __init__(self, region_id, instance_backup_id, ):
        """
        :param region_id: 资源池ID
        :param instance_backup_id: 云主机备份实例ID
        """
        self.region_id = region_id
        self.instance_backup_id = instance_backup_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_backup_id is None:
            raise Exception("instance_backup_id can not None")

