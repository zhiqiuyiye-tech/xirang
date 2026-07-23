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


class CreateRepoRequest(CTYunRequest):
    """
    创建云硬盘备份存储库   
    1.目前不支持autoRenewStatus（是否自动续订）字段   
    2.底层size属性不支持默认，需要必传
    """

    def __init__(self, request_param):
        super(CreateRepoRequest, self).__init__("/v4/ebs-backup/repo/create", "POST", "ebsbackup", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.repository_name is not None:
            body_param["repositoryName"] = self.parameters.repository_name
        if self.parameters.size is not None:
            body_param["size"] = self.parameters.size
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.auto_renew_status is not None:
            body_param["autoRenewStatus"] = self.parameters.auto_renew_status
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreateRepoRequestParam(object):

    def __init__(self, region_id, repository_name, cycle_type, client_token=None, size=None, cycle_count=None, auto_renew_status=None, project_id=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池id
        :param repository_name: 长度限制2-63，支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param size: 云硬盘备份存储库容量，单位GB，取值10-1024000，默认100
        :param cycle_type: 本参数表示订购周期类型 ，取值范围： MONTH：按月 YEAR：按年   
         包年包月需必传cycleCount的属性   
         按需计费cycleType=onDemand
        :param cycle_count: 与cycleType配合，cycleType为Month时，单位为月，cycleType为YEAR时，单位为年;最长订购周期为5年
        :param auto_renew_status: 本参数表示是否自动续订 ，取值范围： 0：不续费 1：自动续费，默认不自动续费（暂不支持）
        :param project_id: 企业项目ID，默认“0”
        """
        self.client_token = client_token
        self.region_id = region_id
        self.repository_name = repository_name
        self.size = size
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.auto_renew_status = auto_renew_status
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_size(self, size):
        """
        :param size: 云硬盘备份存储库容量，单位GB，取值10-1024000，默认100
        """
        self.size = size

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 与cycleType配合，cycleType为Month时，单位为月，cycleType为YEAR时，单位为年;最长订购周期为5年
        """
        self.cycle_count = cycle_count

    def set_auto_renew_status(self, auto_renew_status):
        """
        :param auto_renew_status: 本参数表示是否自动续订 ，取值范围： 0：不续费 1：自动续费，默认不自动续费（暂不支持）
        """
        self.auto_renew_status = auto_renew_status

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认“0”
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.repository_name is None:
            raise Exception("repository_name can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

