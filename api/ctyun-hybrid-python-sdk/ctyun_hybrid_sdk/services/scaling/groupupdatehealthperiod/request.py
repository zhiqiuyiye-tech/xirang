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


class GroupUpdateHealthPeriodRequest(CTYunRequest):
    """
    修改弹性伸缩组的健康检查间隔
    """

    def __init__(self, request_param):
        super(GroupUpdateHealthPeriodRequest, self).__init__("/v4/scaling/group/update-health-period", "POST", "scaling", "application/json")
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
        if self.parameters.health_period is not None:
            body_param["healthPeriod"] = self.parameters.health_period
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


class GroupUpdateHealthPeriodRequestParam(object):

    def __init__(self, region_id, group_id, health_period, ):
        """
        :param region_id: 资源池id
        :param group_id: 伸缩组id
        :param health_period: 健康检查时间间隔（周期），单位：秒，取值范围：[1,2147483647]
        """
        self.region_id = region_id
        self.group_id = group_id
        self.health_period = health_period

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.health_period is None:
            raise Exception("health_period can not None")

