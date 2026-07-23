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


class V4SfsRestoreRequest(CTYunRequest):
    """
    恢复文件系统
    """

    def __init__(self, request_param):
        super(V4SfsRestoreRequest, self).__init__("/v4/sfs/restore", "POST", "sfs", "application/json")
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
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
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


class V4SfsRestoreRequestParam(object):

    def __init__(self, region_id, on_demand, resource_id=None, sfs_uid=None, cycle_type=None, cycle_count=None):
        """
        :param resource_id: 参数resourceID或sfsUID二者必传其一
        :param sfs_uid: 参数resourceID或sfsUID二者必传其一
        :param region_id: 资源池ID
        :param on_demand: 是否按需下单。true/false，默认为 false
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定。
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定,长度不能超过5年
        """
        self.resource_id = resource_id
        self.sfs_uid = sfs_uid
        self.region_id = region_id
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 参数resourceID或sfsUID二者必传其一
        """
        self.resource_id = resource_id

    def set_sfs_uid(self, sfs_uid):
        """
        :param sfs_uid: 参数resourceID或sfsUID二者必传其一
        """
        self.sfs_uid = sfs_uid

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定。
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定,长度不能超过5年
        """
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.on_demand is None:
            raise Exception("on_demand can not None")

