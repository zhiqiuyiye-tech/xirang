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


class SnapshotPolicyUpdateRequest(CTYunRequest):
    """
    修改云主机快照策略
    """

    def __init__(self, request_param):
        super(SnapshotPolicyUpdateRequest, self).__init__("/v4/ecs/snapshot-policy/update", "POST", "ctecs", "application/json")
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
        if self.parameters.snapshot_policy_name is not None:
            body_param["snapshotPolicyName"] = self.parameters.snapshot_policy_name
        if self.parameters.snapshot_time is not None:
            body_param["snapshotTime"] = self.parameters.snapshot_time
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_day is not None:
            body_param["cycleDay"] = self.parameters.cycle_day
        if self.parameters.cycle_week is not None:
            body_param["cycleWeek"] = self.parameters.cycle_week
        if self.parameters.retention_type is not None:
            body_param["retentionType"] = self.parameters.retention_type
        if self.parameters.retention_day is not None:
            body_param["retentionDay"] = self.parameters.retention_day
        if self.parameters.retention_num is not None:
            body_param["retentionNum"] = self.parameters.retention_num
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


class SnapshotPolicyUpdateRequestParam(object):

    def __init__(self, region_id, snapshot_policy_id, snapshot_policy_name=None, snapshot_time=None, cycle_type=None, cycle_day=None, cycle_week=None, retention_type=None, retention_day=None, retention_num=None):
        """
        :param region_id: 资源池ID，您可以查看<a href="https://www.ctyun.cn/document/10026730/10028695">地域和可用区</a>来了解资源池 <br />获取：<br /><span style="background-color: rgb(73, 204, 144);color: rgb(255,255,255);padding: 2px; margin:2px">查</span> <a  href="https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=5851&data=87">资源池列表查询</a>
        :param snapshot_policy_id: 云主机快照策略ID，32字节<br />获取：<br /><span style="background-color: rgb(73, 204, 144);color: rgb(255,255,255);padding: 2px; margin:2px">查</span> <a href="https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=9600&data=87">查询云主机快照策略列表</a><br /><span style="background-color: rgb(97, 175, 254);color: rgb(255,255,255);padding: 2px; margin:2px">创</span> <a href="https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=9588&data=87">创建云主机快照策略</a>
        :param snapshot_policy_name: 云主机快照策略名称，满足以下规则：长度为2~63字符，由数字、字母、-组成，只能以字母开头，以数字和字母结尾
        :param snapshot_time: 快照整点时间，时间取值范围：0~23<br />注：如果一天内多个时间节点备份，以逗号隔开（如11点15点进行快照，则填写"11,15"），默认值0
        :param cycle_type: 云主机快照周期类型，取值范围：<br />day（天），<br />week（周）
        :param cycle_day: 类型：int16;快照周期（天），取值范围：[1, 10] <br />注：cycleType为day时需设置
        :param cycle_week: 快照周期（星期），星期取值范围：0~6（代表周几，其中0为周日）<br />注：只有cycleType为week时需设置；<br />如果一周有多天备份，以逗号隔开（如周日周三进行快照，则填写"0,3"）
        :param retention_type: 云主机快照保留类型，取值范围：<br />date（按时间保存），<br />num（按数量保存）
        :param retention_day: 云主机快照保留天数，单位为天，取值范围：[1, 365] <br />注：retentionType为date时必填
        :param retention_num: 云主机快照保留数量，取值范围：[1, 30]<br />注：retentionType为num时必填
        """
        self.region_id = region_id
        self.snapshot_policy_id = snapshot_policy_id
        self.snapshot_policy_name = snapshot_policy_name
        self.snapshot_time = snapshot_time
        self.cycle_type = cycle_type
        self.cycle_day = cycle_day
        self.cycle_week = cycle_week
        self.retention_type = retention_type
        self.retention_day = retention_day
        self.retention_num = retention_num

    def set_snapshot_policy_name(self, snapshot_policy_name):
        """
        :param snapshot_policy_name: 云主机快照策略名称，满足以下规则：长度为2~63字符，由数字、字母、-组成，只能以字母开头，以数字和字母结尾
        """
        self.snapshot_policy_name = snapshot_policy_name

    def set_snapshot_time(self, snapshot_time):
        """
        :param snapshot_time: 快照整点时间，时间取值范围：0~23<br />注：如果一天内多个时间节点备份，以逗号隔开（如11点15点进行快照，则填写"11,15"），默认值0
        """
        self.snapshot_time = snapshot_time

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 云主机快照周期类型，取值范围：<br />day（天），<br />week（周）
        """
        self.cycle_type = cycle_type

    def set_cycle_day(self, cycle_day):
        """
        :param cycle_day: 类型：int16;快照周期（天），取值范围：[1, 10] <br />注：cycleType为day时需设置
        """
        self.cycle_day = cycle_day

    def set_cycle_week(self, cycle_week):
        """
        :param cycle_week: 快照周期（星期），星期取值范围：0~6（代表周几，其中0为周日）<br />注：只有cycleType为week时需设置；<br />如果一周有多天备份，以逗号隔开（如周日周三进行快照，则填写"0,3"）
        """
        self.cycle_week = cycle_week

    def set_retention_type(self, retention_type):
        """
        :param retention_type: 云主机快照保留类型，取值范围：<br />date（按时间保存），<br />num（按数量保存）
        """
        self.retention_type = retention_type

    def set_retention_day(self, retention_day):
        """
        :param retention_day: 云主机快照保留天数，单位为天，取值范围：[1, 365] <br />注：retentionType为date时必填
        """
        self.retention_day = retention_day

    def set_retention_num(self, retention_num):
        """
        :param retention_num: 云主机快照保留数量，取值范围：[1, 30]<br />注：retentionType为num时必填
        """
        self.retention_num = retention_num

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_policy_id is None:
            raise Exception("snapshot_policy_id can not None")

