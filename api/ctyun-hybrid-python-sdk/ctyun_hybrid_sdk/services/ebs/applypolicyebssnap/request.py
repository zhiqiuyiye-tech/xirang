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


class ApplyPolicyEbsSnapRequest(CTYunRequest):
    """
    关联云硬盘自动快照策略
    """

    def __init__(self, request_param):
        super(ApplyPolicyEbsSnapRequest, self).__init__("/v4/ebs_snapshot/apply-policy-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_policy_id is not None:
            body_param["snapshotPolicyID"] = self.parameters.snapshot_policy_id
        if self.parameters.target_disk_ids is not None:
            body_param["targetDiskIDs"] = self.parameters.target_disk_ids
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


class ApplyPolicyEbsSnapRequestParam(object):

    def __init__(self, region_id, snapshot_policy_id, target_disk_ids, ):
        """
        :param region_id: 资源池id
        :param snapshot_policy_id: 快照策略ID
        :param target_disk_ids: 要关联的云硬盘ID，多个用英文逗号隔开
        """
        self.region_id = region_id
        self.snapshot_policy_id = snapshot_policy_id
        self.target_disk_ids = target_disk_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_policy_id is None:
            raise Exception("snapshot_policy_id can not None")
        if self.target_disk_ids is None:
            raise Exception("target_disk_ids can not None")

