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


class EcsRecoverUnsubscribedRequest(CTYunRequest):
    """
    批量恢复云主机，要求：   
     1.云主机必须存在   
     2.批量恢复资源一次不能超过10个   
     3.云主机必须在回收站，处于退订状态
    """

    def __init__(self, request_param):
        super(EcsRecoverUnsubscribedRequest, self).__init__("/v4/ecs/recover-unsubscribed-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class EcsRecoverUnsubscribedRequestParam(object):

    def __init__(self, instance_id_list, region_id, cycle_type=None, cycle_count=None):
        """
        :param instance_id_list: 云主机ID列表 注意:此参数为数组
        :param region_id: 资源池ID
        :param cycle_type: 订购周期类型，取值范围：   
         MONTH：按月，   
         YEAR：按年   
         包周期计费类型必填
        :param cycle_count: 订购时长，该参数需要与cycleType一同使用，不超过5年   
         包周期计费类型必填
        """
        self.instance_id_list = instance_id_list
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 订购周期类型，取值范围：   
         MONTH：按月，   
         YEAR：按年   
         包周期计费类型必填
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，该参数需要与cycleType一同使用，不超过5年   
         包周期计费类型必填
        """
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id_list is None:
            raise Exception("instance_id_list can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

