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


class RenewRepoRequest(CTYunRequest):
    """
    续订云硬盘备份存储库
    """

    def __init__(self, request_param):
        super(RenewRepoRequest, self).__init__("/v4/ebs-backup/repo/renew", "POST", "ebsbackup", "application/json")
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
        if self.parameters.repository_id is not None:
            body_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class RenewRepoRequestParam(object):

    def __init__(self, region_id, repository_id, cycle_type, cycle_count, client_token=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池id
        :param repository_id: 云硬盘备份存储库ID
        :param cycle_type: 本参数表示订购周期类型 ，取值范围： MONTH：按月 YEAR：按年
        :param cycle_count: 订购时长，与cycleType配合，cycleType为Month时，单位为月，cycleType为YEAR时，单位为年;最长订购周期为5年
        """
        self.client_token = client_token
        self.region_id = region_id
        self.repository_id = repository_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.repository_id is None:
            raise Exception("repository_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")

