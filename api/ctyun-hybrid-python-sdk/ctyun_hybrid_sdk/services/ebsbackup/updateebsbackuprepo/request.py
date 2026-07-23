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


class UpdateEbsBackupRepoRequest(CTYunRequest):
    """
    更新云硬盘备份存储库信息
    """

    def __init__(self, request_param):
        super(UpdateEbsBackupRepoRequest, self).__init__("/v4/ebs-backup/repo/update", "POST", "ebsbackup", "application/json")
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
        if self.parameters.repository_id is not None:
            body_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.repository_name is not None:
            body_param["repositoryName"] = self.parameters.repository_name
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


class UpdateEbsBackupRepoRequestParam(object):

    def __init__(self, region_id, repository_id, repository_name, ):
        """
        :param region_id: 资源池id
        :param repository_id: 云硬盘备份存储库ID
        :param repository_name: 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        """
        self.region_id = region_id
        self.repository_id = repository_id
        self.repository_name = repository_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.repository_id is None:
            raise Exception("repository_id can not None")
        if self.repository_name is None:
            raise Exception("repository_name can not None")

