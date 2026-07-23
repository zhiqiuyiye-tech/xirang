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


class CreatePolicyEbsSnapRequest(CTYunRequest):
    """
    创建云硬盘自动快照策略
    """

    def __init__(self, request_param):
        super(CreatePolicyEbsSnapRequest, self).__init__("/v4/ebs_snapshot/create-policy-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_policy_name is not None:
            body_param["snapshotPolicyName"] = self.parameters.snapshot_policy_name
        if self.parameters.repeat_weekdays is not None:
            body_param["repeatWeekdays"] = self.parameters.repeat_weekdays
        if self.parameters.repeat_times is not None:
            body_param["repeatTimes"] = self.parameters.repeat_times
        if self.parameters.retention_time is not None:
            body_param["retentionTime"] = self.parameters.retention_time
        if self.parameters.is_enabled is not None:
            body_param["isEnabled"] = self.parameters.is_enabled
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


class CreatePolicyEbsSnapRequestParam(object):

    def __init__(self, region_id, snapshot_policy_name, repeat_weekdays, repeat_times, retention_time, is_enabled=None, project_id=None):
        """
        :param region_id: 资源池id
        :param snapshot_policy_name: 快照策略名称，只能由英文字母、数字、下划线、中划线组成，只能以英文字母开头，长度2-63字符。
        :param repeat_weekdays: 创建快照的重复日期，0-6分别代表周日-周六，多个日期用英文逗号隔开。
        :param repeat_times: 创建快照的重复时间，0-23分别代表零点-23点，多个时间用英文逗号隔开。
        :param retention_time: 创建快照的保留时间，输入范围为[-1，1-65535]，-1代表永久保留。
        :param is_enabled: 是否启用策略，默认启用。
        :param project_id: 项目id，暂不支持
        """
        self.region_id = region_id
        self.snapshot_policy_name = snapshot_policy_name
        self.repeat_weekdays = repeat_weekdays
        self.repeat_times = repeat_times
        self.retention_time = retention_time
        self.is_enabled = is_enabled
        self.project_id = project_id

    def set_is_enabled(self, is_enabled):
        """
        :param is_enabled: 是否启用策略，默认启用。
        """
        self.is_enabled = is_enabled

    def set_project_id(self, project_id):
        """
        :param project_id: 项目id，暂不支持
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_policy_name is None:
            raise Exception("snapshot_policy_name can not None")
        if self.repeat_weekdays is None:
            raise Exception("repeat_weekdays can not None")
        if self.repeat_times is None:
            raise Exception("repeat_times can not None")
        if self.retention_time is None:
            raise Exception("retention_time can not None")

