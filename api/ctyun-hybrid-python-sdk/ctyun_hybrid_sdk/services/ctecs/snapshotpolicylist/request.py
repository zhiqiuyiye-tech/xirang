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


class SnapshotPolicyListRequest(CTYunRequest):
    """
    查询云主机快照策略列表
    """

    def __init__(self, request_param):
        super(SnapshotPolicyListRequest, self).__init__("/v4/ecs/snapshot-policy/list", "POST", "ctecs", "application/json")
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


class SnapshotPolicyListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, snapshot_policy_status=None, query_content=None):
        """
        :param region_id: 资源池ID，您可以查看<a href="https://www.ctyun.cn/document/10026730/10028695">地域和可用区</a>来了解资源池 <br />获取：<br /><span style="background-color: rgb(73, 204, 144);color: rgb(255,255,255);padding: 2px; margin:2px">查</span> <a  href="https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=5851&data=87">资源池列表查询</a>
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param snapshot_policy_status: 快照策略状态，是否启用，取值范围：0（不启用），<br />1（启用）<br />注：默认值1（启用）
        :param query_content: 模糊匹配查询内容（匹配字段：snapshotPolicyID、snapshotPolicyName）
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.snapshot_policy_status = snapshot_policy_status
        self.query_content = query_content

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_snapshot_policy_status(self, snapshot_policy_status):
        """
        :param snapshot_policy_status: 快照策略状态，是否启用，取值范围：0（不启用），<br />1（启用）<br />注：默认值1（启用）
        """
        self.snapshot_policy_status = snapshot_policy_status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊匹配查询内容（匹配字段：snapshotPolicyID、snapshotPolicyName）
        """
        self.query_content = query_content

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

