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


class EcsBackupListRequest(CTYunRequest):
    """
    查询云主机备份列表   
    - 推荐使用新接口：/v4/ecs/backup/list   
    
    """

    def __init__(self, request_param):
        super(EcsBackupListRequest, self).__init__("/v4/ecs/backup/list", "POST", "ctecs", "application/json")
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
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.repository_id is not None:
            body_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.instance_backup_id is not None:
            body_param["instanceBackupID"] = self.parameters.instance_backup_id
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.instance_backup_status is not None:
            body_param["instanceBackupStatus"] = self.parameters.instance_backup_status
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


class EcsBackupListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, instance_id=None, repository_id=None, instance_backup_id=None, query_content=None, instance_backup_status=None):
        """
        :param region_id: 资源池ID
        :param page_no: 页码，不传或传0默认为1
        :param page_size: 每页记录数目，取值范围：[1, 100],传0或者不传默认为10，超过100按100处理
        :param instance_id: 云主机id
        :param repository_id: 存储库id
        :param instance_backup_id: 云主机备份ID
        :param query_content: 查询内容：（匹配：云主机备份名称、云主机备份ID、云主机备份状态、云主机名称）
        :param instance_backup_status: 云主机备份状态
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.instance_id = instance_id
        self.repository_id = repository_id
        self.instance_backup_id = instance_backup_id
        self.query_content = query_content
        self.instance_backup_status = instance_backup_status

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，不传或传0默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100],传0或者不传默认为10，超过100按100处理
        """
        self.page_size = page_size

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 云主机id
        """
        self.instance_id = instance_id

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 存储库id
        """
        self.repository_id = repository_id

    def set_instance_backup_id(self, instance_backup_id):
        """
        :param instance_backup_id: 云主机备份ID
        """
        self.instance_backup_id = instance_backup_id

    def set_query_content(self, query_content):
        """
        :param query_content: 查询内容：（匹配：云主机备份名称、云主机备份ID、云主机备份状态、云主机名称）
        """
        self.query_content = query_content

    def set_instance_backup_status(self, instance_backup_status):
        """
        :param instance_backup_status: 云主机备份状态
        """
        self.instance_backup_status = instance_backup_status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

