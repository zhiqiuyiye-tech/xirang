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


class UpdateQuotaLimitRequest(CTYunRequest):
    """
    修改配额上限接口
    """

    def __init__(self, request_param):
        super(UpdateQuotaLimitRequest, self).__init__("/v1/quota/updateQuotaLimit", "POST", "iam", "application/json")
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
        if self.parameters.user_id is not None:
            body_param["userId"] = self.parameters.user_id
        if self.parameters.account_id is not None:
            body_param["accountId"] = self.parameters.account_id
        if self.parameters.region_id is not None:
            body_param["regionId"] = self.parameters.region_id
        if self.parameters.project_id is not None:
            body_param["projectId"] = self.parameters.project_id
        if self.parameters.quota_id is not None:
            body_param["quotaId"] = self.parameters.quota_id
        if self.parameters.quota_total is not None:
            body_param["quotaTotal"] = self.parameters.quota_total
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


class UpdateQuotaLimitRequestParam(object):

    def __init__(self, account_id, region_id, quota_id, quota_total, user_id=None, project_id=None):
        """
        :param user_id: 用户ID，暂时不用，也不生效，可以不传入
        :param account_id: VDC的主账户ID
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        :param quota_id: 配额ID列表，配额ID定义产品的唯一一种配额类型
        :param quota_total: 配额上限设置   
         
        """
        self.user_id = user_id
        self.account_id = account_id
        self.region_id = region_id
        self.project_id = project_id
        self.quota_id = quota_id
        self.quota_total = quota_total

    def set_user_id(self, user_id):
        """
        :param user_id: 用户ID，暂时不用，也不生效，可以不传入
        """
        self.user_id = user_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.account_id is None:
            raise Exception("account_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.quota_id is None:
            raise Exception("quota_id can not None")
        if self.quota_total is None:
            raise Exception("quota_total can not None")

