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


class QueryPolicyEbsSnapVdcRequest(CTYunRequest):
    """
    查询云硬盘自动快照策略-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
    """

    def __init__(self, request_param):
        super(QueryPolicyEbsSnapVdcRequest, self).__init__("/v4/ebs_snapshot/query-policy-ebs-snap-vdc", "GET", "ebs", "")
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
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.snapshot_policy_id is not None:
            query_param["snapshotPolicyID"] = self.parameters.snapshot_policy_id
        if self.parameters.snapshot_policy_name is not None:
            query_param["snapshotPolicyName"] = self.parameters.snapshot_policy_name
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryPolicyEbsSnapVdcRequestParam(object):

    def __init__(self, region_id, snapshot_policy_id=None, snapshot_policy_name=None, org_id=None):
        """
        :param region_id: 资源池ID
        :param snapshot_policy_id: 快照策略ID，模糊匹配
        :param snapshot_policy_name: 快照策略名称，模糊匹配
        :param org_id: 组织ID
        """
        self.region_id = region_id
        self.snapshot_policy_id = snapshot_policy_id
        self.snapshot_policy_name = snapshot_policy_name
        self.org_id = org_id

    def set_snapshot_policy_id(self, snapshot_policy_id):
        """
        :param snapshot_policy_id: 快照策略ID，模糊匹配
        """
        self.snapshot_policy_id = snapshot_policy_id

    def set_snapshot_policy_name(self, snapshot_policy_name):
        """
        :param snapshot_policy_name: 快照策略名称，模糊匹配
        """
        self.snapshot_policy_name = snapshot_policy_name

    def set_org_id(self, org_id):
        """
        :param org_id: 组织ID
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

