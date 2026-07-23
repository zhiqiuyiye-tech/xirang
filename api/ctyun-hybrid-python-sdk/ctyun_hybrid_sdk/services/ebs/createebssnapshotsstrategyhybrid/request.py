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


class CreateEbsSnapshotsStrategyHybridRequest(CTYunRequest):
    """
    快照策略 创建。**注意**开发未对齐原因：公有云无此接口，按照py接口开发
    """

    def __init__(self, request_param):
        super(CreateEbsSnapshotsStrategyHybridRequest, self).__init__("/v4/ebs/snapshots_strategy/create", "POST", "ebs", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.frequency is not None:
            body_param["frequency"] = self.parameters.frequency
        if self.parameters.is_enable is not None:
            body_param["isEnable"] = self.parameters.is_enable
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.obj_type is not None:
            body_param["objType"] = self.parameters.obj_type
        if self.parameters.remain_first_backup_of_cur_month is not None:
            body_param["remainFirstBackupOfCurMonth"] = self.parameters.remain_first_backup_of_cur_month
        if self.parameters.rentention_num is not None:
            body_param["rententionNum"] = self.parameters.rentention_num
        if self.parameters.rentention_type is not None:
            body_param["rententionType"] = self.parameters.rentention_type
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


class CreateEbsSnapshotsStrategyHybridRequestParam(object):

    def __init__(self, region_id, cycle_type, frequency, is_enable, name, obj_type, remain_first_backup_of_cur_month, rentention_num, rentention_type, ):
        """
        :param region_id: 资源池id
        :param cycle_type: 备份周期类型 day or week
        :param frequency: cycle_type 等于 week 时，表示周几执 行，多个用逗号分割，0-6:星期日-星期一；cycle_type 等于 day 时，表示每隔多少天执行。
        :param is_enable: 1：开启，0：关闭
        :param name: 只能由英文字母、数字、下划线、中划线组成，只能以英文字母开头，长度2-64字符。
        :param obj_type: 策略类型。”EBS“:云硬盘快照策略。
        :param remain_first_backup_of_cur_month: 策略执行时间（0~23），多个时间用逗号分割。
        :param rentention_num: 保留规则值 大于0
        :param rentention_type: 保留规则类型。 ‘time’- ‘按时间’, ‘quantity’- ‘按数量’。
        """
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.frequency = frequency
        self.is_enable = is_enable
        self.name = name
        self.obj_type = obj_type
        self.remain_first_backup_of_cur_month = remain_first_backup_of_cur_month
        self.rentention_num = rentention_num
        self.rentention_type = rentention_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.frequency is None:
            raise Exception("frequency can not None")
        if self.is_enable is None:
            raise Exception("is_enable can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.obj_type is None:
            raise Exception("obj_type can not None")
        if self.remain_first_backup_of_cur_month is None:
            raise Exception("remain_first_backup_of_cur_month can not None")
        if self.rentention_num is None:
            raise Exception("rentention_num can not None")
        if self.rentention_type is None:
            raise Exception("rentention_type can not None")

