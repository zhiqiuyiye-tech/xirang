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


class CreateBackupPolicyRequest(CTYunRequest):
    """
    创建云主机备份策略
    """

    def __init__(self, request_param):
        super(CreateBackupPolicyRequest, self).__init__("/v4/ecs/backup-policy/create", "POST", "ctecs", "application/json")
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
        if self.parameters.policy_name is not None:
            body_param["policyName"] = self.parameters.policy_name
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_day is not None:
            body_param["cycleDay"] = self.parameters.cycle_day
        if self.parameters.cycle_week is not None:
            body_param["cycleWeek"] = self.parameters.cycle_week
        if self.parameters.time is not None:
            body_param["time"] = self.parameters.time
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
        if self.parameters.retention_type is not None:
            body_param["retentionType"] = self.parameters.retention_type
        if self.parameters.retention_day is not None:
            body_param["retentionDay"] = self.parameters.retention_day
        if self.parameters.retention_num is not None:
            body_param["retentionNum"] = self.parameters.retention_num
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


class CreateBackupPolicyRequestParam(object):

    def __init__(self, region_id, policy_name, cycle_type, retention_type, cycle_day=None, cycle_week=None, time=None, status=None, retention_day=None, retention_num=None, project_id=None):
        """
        :param region_id: 资源id
        :param policy_name: 云主机备份策略名称，满足以下规则：长度为2～64字符 支持使用中文、字母、数字、下划线（_）、中划线（-）
        :param cycle_type: 云主机备份周期类型，取值范围：day（按天备份）week（按星期备份）
        :param cycle_day: 备份周期，只有cycleType为day时需设置,取值范围：1-30，默认值为1
        :param cycle_week:  备份周期，只有cycleType为week时需设置，取值范围：0-6代表星期日-星期六，如果一周有多天备份，以逗号隔开,默认值是0
        :param time: 备份整点时间，取值范围：0-23，如果一天内多个时间节点备份，以逗号隔开,默认值12
        :param status: 是否启用策略，取值范围：<br />0：停用，<br />1：启用，<br />默认值为0
        :param retention_type: 云主机备份保留类型，取值范围：<br />date：按时间保留，<br />num：按数量保留，<br />all：永久保留
        :param retention_day: 保留天数，只有retentionType为date时需设置，取值范围：1-99999，默认值1
        :param retention_num: 保留数量，只有retentionType为num时需设置,取值范围：1-99999，默认值1
        :param project_id: 企业项目ID,暂不支持
        """
        self.region_id = region_id
        self.policy_name = policy_name
        self.cycle_type = cycle_type
        self.cycle_day = cycle_day
        self.cycle_week = cycle_week
        self.time = time
        self.status = status
        self.retention_type = retention_type
        self.retention_day = retention_day
        self.retention_num = retention_num
        self.project_id = project_id

    def set_cycle_day(self, cycle_day):
        """
        :param cycle_day: 备份周期，只有cycleType为day时需设置,取值范围：1-30，默认值为1
        """
        self.cycle_day = cycle_day

    def set_cycle_week(self, cycle_week):
        """
        :param cycle_week:  备份周期，只有cycleType为week时需设置，取值范围：0-6代表星期日-星期六，如果一周有多天备份，以逗号隔开,默认值是0
        """
        self.cycle_week = cycle_week

    def set_time(self, time):
        """
        :param time: 备份整点时间，取值范围：0-23，如果一天内多个时间节点备份，以逗号隔开,默认值12
        """
        self.time = time

    def set_status(self, status):
        """
        :param status: 是否启用策略，取值范围：<br />0：停用，<br />1：启用，<br />默认值为0
        """
        self.status = status

    def set_retention_day(self, retention_day):
        """
        :param retention_day: 保留天数，只有retentionType为date时需设置，取值范围：1-99999，默认值1
        """
        self.retention_day = retention_day

    def set_retention_num(self, retention_num):
        """
        :param retention_num: 保留数量，只有retentionType为num时需设置,取值范围：1-99999，默认值1
        """
        self.retention_num = retention_num

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID,暂不支持
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.policy_name is None:
            raise Exception("policy_name can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.retention_type is None:
            raise Exception("retention_type can not None")

