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


class GroupInstanceMonitorRequest(CTYunRequest):
    """
    获取弹性伸缩实例数量监控数据
    """

    def __init__(self, request_param):
        super(GroupInstanceMonitorRequest, self).__init__("/v4/scaling/group/instance-monitor", "POST", "scaling", "application/json")
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
        if self.parameters.time_range is not None:
            body_param["timeRange"] = self.parameters.time_range
        if self.parameters.time_from is not None:
            body_param["timeFrom"] = self.parameters.time_from
        if self.parameters.time_till is not None:
            body_param["timeTill"] = self.parameters.time_till
        if self.parameters.period is not None:
            body_param["period"] = self.parameters.period
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


class GroupInstanceMonitorRequestParam(object):

    def __init__(self, region_id, group_id, time_range=None, time_from=None, time_till=None, period=None):
        """
        :param region_id: 资源池id
        :param group_id: 伸缩组ID
        :param time_range: 单位：分钟；时间范围，默认值为60；若时间戳无效，当前时间向前倒推
        :param time_from: 开始时间,时间戳；优先
        :param time_till: 结束时间,时间戳; 优先
        :param period: 单位：秒；时间间隔，默认为60
        """
        self.region_id = region_id
        self.group_id = group_id
        self.time_range = time_range
        self.time_from = time_from
        self.time_till = time_till
        self.period = period

    def set_time_range(self, time_range):
        """
        :param time_range: 单位：分钟；时间范围，默认值为60；若时间戳无效，当前时间向前倒推
        """
        self.time_range = time_range

    def set_time_from(self, time_from):
        """
        :param time_from: 开始时间,时间戳；优先
        """
        self.time_from = time_from

    def set_time_till(self, time_till):
        """
        :param time_till: 结束时间,时间戳; 优先
        """
        self.time_till = time_till

    def set_period(self, period):
        """
        :param period: 单位：秒；时间间隔，默认为60
        """
        self.period = period

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

