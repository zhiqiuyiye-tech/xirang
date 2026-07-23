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


class QueryEcsSnapshotPolicyListVdcRequest(CTYunRequest):
    """
    该接口1.16.06及以上云管版本支持。
    """

    def __init__(self, request_param):
        super(QueryEcsSnapshotPolicyListVdcRequest, self).__init__("/v4/ecs/snapshot-policy/list-vdc", "POST", "ctecs", "application/json")
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
        if self.parameters.snapshot_policy_status is not None:
            body_param["snapshotPolicyStatus"] = self.parameters.snapshot_policy_status
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.org_id is not None:
            body_param["orgId"] = self.parameters.org_id
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


class QueryEcsSnapshotPolicyListVdcRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, snapshot_policy_status=None, query_content=None, org_id=None):
        """
        :param region_id: 资源id
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        :param page_size: 每页记录数目，取值范围：[1, 50]，注：默认值为10
        :param snapshot_policy_status: 快照策略状态，是否启用，取值范围：0（不启用），1（启用）
        :param query_content: 模糊匹配查询内容（匹配字段：snapshotPolicyName）
        :param org_id: 组织id
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.snapshot_policy_status = snapshot_policy_status
        self.query_content = query_content
        self.org_id = org_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 50]，注：默认值为10
        """
        self.page_size = page_size

    def set_snapshot_policy_status(self, snapshot_policy_status):
        """
        :param snapshot_policy_status: 快照策略状态，是否启用，取值范围：0（不启用），1（启用）
        """
        self.snapshot_policy_status = snapshot_policy_status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊匹配查询内容（匹配字段：snapshotPolicyName）
        """
        self.query_content = query_content

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

