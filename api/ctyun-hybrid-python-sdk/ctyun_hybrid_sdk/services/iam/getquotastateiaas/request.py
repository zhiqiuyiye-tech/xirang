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


class GetQuotaStateIaaSRequest(CTYunRequest):
    """
    根据主账号ID、VDCID、企业项目ID，获取所有配额的已用量   
    
    """

    def __init__(self, request_param):
        super(GetQuotaStateIaaSRequest, self).__init__("/v1/quota/queryQuotaUsedIaaS", "GET", "iam", "")
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
        if self.parameters.account_id is not None:
            query_param["accountId"] = self.parameters.account_id
        if self.parameters.vdc_id is not None:
            query_param["vdcId"] = self.parameters.vdc_id
        if self.parameters.region_id is not None:
            query_param["regionId"] = self.parameters.region_id
        if self.parameters.project_id is not None:
            query_param["projectId"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetQuotaStateIaaSRequestParam(object):

    def __init__(self, region_id, project_id, account_id=None, vdc_id=None):
        """
        :param account_id: 主账号ID，主账号、VDC必选填一个
        :param vdc_id: VDCID，主账号、VDC必选填一个
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        """
        self.account_id = account_id
        self.vdc_id = vdc_id
        self.region_id = region_id
        self.project_id = project_id

    def set_account_id(self, account_id):
        """
        :param account_id: 主账号ID，主账号、VDC必选填一个
        """
        self.account_id = account_id

    def set_vdc_id(self, vdc_id):
        """
        :param vdc_id: VDCID，主账号、VDC必选填一个
        """
        self.vdc_id = vdc_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.project_id is None:
            raise Exception("project_id can not None")

