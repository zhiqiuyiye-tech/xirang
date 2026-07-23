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


class UpdateEbsBackupPolicyRequest(CTYunRequest):
    """
    修改云盘备份策略   
    resourceCount代码暂未支持该属性
    """

    def __init__(self, request_param):
        super(UpdateEbsBackupPolicyRequest, self).__init__("/v4/ebs-backup/policy/update", "POST", "ebsbackup", "application/json")
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
        if self.parameters.retention_type is not None:
            body_param["retentionType"] = self.parameters.retention_type
        if self.parameters.retention_num is not None:
            body_param["retentionNum"] = self.parameters.retention_num
        if self.parameters.retention_day is not None:
            body_param["retentionDay"] = self.parameters.retention_day
        if self.parameters.remain_first_of_cur_month is not None:
            body_param["remainFirstOfCurMonth"] = self.parameters.remain_first_of_cur_month
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


class UpdateEbsBackupPolicyRequestParam(object):

    def __init__(self, region_id, policy_id, policy_name=None, cycle_type=None, cycle_day=None, cycle_week=None, time=None, retention_type=None, retention_num=None, retention_day=None, remain_first_of_cur_month=None):
        """
        :param region_id: 资源池id
        :param policy_id: 策略ID
        :param policy_name: 策略名，唯一，不可重复，策略名，唯一，不可重复，长度为 2~64 个字符，只能由中文字符、英文字母、数字、下划线、中划线组成
        :param cycle_type: 备份周期类型，day-按天备份，week-按星期备份
        :param cycle_day: 备份周期，只有cycleType为day时需设置
        :param cycle_week: 备份周期，只有cycleType为week时需设置，则取值范围0-6代表星期日-星期六，如果一周有多天备份，以逗号隔开
        :param time: 备份整点时间，取值范围0-23，如果一天内多个时间节点备份，以逗号隔开
        :param retention_type: 备份保留类型，num-按数量保留，date-按时间保留
        :param retention_num: 保留数量，只有retentionType为num时需设置,取值范围1-65535
        :param retention_day: 保留天数，只有retentionType为date时需设置，取值1-65535
        :param remain_first_of_cur_month: 是否保留每个月第一个备份，在retentionType为num时可设置，默认false（暂不支持该功能）
        """
        self.region_id = region_id
        self.policy_id = policy_id
        self.policy_name = policy_name
        self.cycle_type = cycle_type
        self.cycle_day = cycle_day
        self.cycle_week = cycle_week
        self.time = time
        self.retention_type = retention_type
        self.retention_num = retention_num
        self.retention_day = retention_day
        self.remain_first_of_cur_month = remain_first_of_cur_month

    def set_policy_name(self, policy_name):
        """
        :param policy_name: 策略名，唯一，不可重复，策略名，唯一，不可重复，长度为 2~64 个字符，只能由中文字符、英文字母、数字、下划线、中划线组成
        """
        self.policy_name = policy_name

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 备份周期类型，day-按天备份，week-按星期备份
        """
        self.cycle_type = cycle_type

    def set_cycle_day(self, cycle_day):
        """
        :param cycle_day: 备份周期，只有cycleType为day时需设置
        """
        self.cycle_day = cycle_day

    def set_cycle_week(self, cycle_week):
        """
        :param cycle_week: 备份周期，只有cycleType为week时需设置，则取值范围0-6代表星期日-星期六，如果一周有多天备份，以逗号隔开
        """
        self.cycle_week = cycle_week

    def set_time(self, time):
        """
        :param time: 备份整点时间，取值范围0-23，如果一天内多个时间节点备份，以逗号隔开
        """
        self.time = time

    def set_retention_type(self, retention_type):
        """
        :param retention_type: 备份保留类型，num-按数量保留，date-按时间保留
        """
        self.retention_type = retention_type

    def set_retention_num(self, retention_num):
        """
        :param retention_num: 保留数量，只有retentionType为num时需设置,取值范围1-65535
        """
        self.retention_num = retention_num

    def set_retention_day(self, retention_day):
        """
        :param retention_day: 保留天数，只有retentionType为date时需设置，取值1-65535
        """
        self.retention_day = retention_day

    def set_remain_first_of_cur_month(self, remain_first_of_cur_month):
        """
        :param remain_first_of_cur_month: 是否保留每个月第一个备份，在retentionType为num时可设置，默认false（暂不支持该功能）
        """
        self.remain_first_of_cur_month = remain_first_of_cur_month

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.policy_id is None:
            raise Exception("policy_id can not None")

