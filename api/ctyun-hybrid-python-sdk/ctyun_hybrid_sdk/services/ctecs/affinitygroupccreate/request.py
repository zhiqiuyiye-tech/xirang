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


class AffinityGroupCcreateRequest(CTYunRequest):
    """
    创建云主机组。
    """

    def __init__(self, request_param):
        super(AffinityGroupCcreateRequest, self).__init__("/v4/ecs/affinity-group/create", "POST", "ctecs", "application/json")
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
        if self.parameters.affinity_group_name is not None:
            body_param["affinityGroupName"] = self.parameters.affinity_group_name
        if self.parameters.policy_type is not None:
            body_param["policyType"] = self.parameters.policy_type
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


class AffinityGroupCcreateRequestParam(object):

    def __init__(self, region_id, affinity_group_name, policy_type=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param affinity_group_name: 主机亲和组名称,长度为1-64字符 支持使用中文、英文字母、数字、下划线(_)、中划线(-)、点号(.),不可重复
        :param policy_type: 主机亲和组策略ID，如：0(反亲和ANTI-AFFINITY)、1(亲和AFFINITY)、2(软反亲和SOFT-ANTI-AFFINITY)、3(软亲和SOFT-AFFINITY),默认值：2
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.affinity_group_name = affinity_group_name
        self.policy_type = policy_type
        self.project_id = project_id

    def set_policy_type(self, policy_type):
        """
        :param policy_type: 主机亲和组策略ID，如：0(反亲和ANTI-AFFINITY)、1(亲和AFFINITY)、2(软反亲和SOFT-ANTI-AFFINITY)、3(软亲和SOFT-AFFINITY),默认值：2
        """
        self.policy_type = policy_type

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.affinity_group_name is None:
            raise Exception("affinity_group_name can not None")

