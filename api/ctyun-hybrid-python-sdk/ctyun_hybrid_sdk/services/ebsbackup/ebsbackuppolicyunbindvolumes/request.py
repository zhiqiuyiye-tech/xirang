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


class EbsBackupPolicyUnbindVolumesRequest(CTYunRequest):
    """
    云盘备份策略解绑云硬盘
    """

    def __init__(self, request_param):
        super(EbsBackupPolicyUnbindVolumesRequest, self).__init__("/v4/ebs-backup/policy/unbind-volumes", "POST", "ebsbackup", "application/json")
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
        if self.parameters.policy_id is not None:
            body_param["policyID"] = self.parameters.policy_id
        if self.parameters.volume_ids is not None:
            body_param["volumeIDs"] = self.parameters.volume_ids
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


class EbsBackupPolicyUnbindVolumesRequestParam(object):

    def __init__(self, region_id, policy_id, volume_ids, ):
        """
        :param region_id: 资源池id
        :param policy_id: 备份策略ID
        :param volume_ids: 云硬盘ID,如果绑定多个,请使用逗号隔开
        """
        self.region_id = region_id
        self.policy_id = policy_id
        self.volume_ids = volume_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.policy_id is None:
            raise Exception("policy_id can not None")
        if self.volume_ids is None:
            raise Exception("volume_ids can not None")

