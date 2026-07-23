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


class GroupUpdateRecoveryModeRequest(CTYunRequest):
    """
    修改弹性伸缩组的云主机回收方式
    """

    def __init__(self, request_param):
        super(GroupUpdateRecoveryModeRequest, self).__init__("/v4/scaling/group/update-recovery-mode", "POST", "scaling", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.recovery_mode is not None:
            body_param["recoveryMode"] = self.parameters.recovery_mode
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


class GroupUpdateRecoveryModeRequestParam(object):

    def __init__(self, region_id, group_id, recovery_mode, ):
        """
        :param region_id: 资源池id
        :param group_id: 伸缩组ID
        :param recovery_mode: 云主机回收方式：1代表释放模式，2代表停机回收模式
        """
        self.region_id = region_id
        self.group_id = group_id
        self.recovery_mode = recovery_mode

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.recovery_mode is None:
            raise Exception("recovery_mode can not None")

