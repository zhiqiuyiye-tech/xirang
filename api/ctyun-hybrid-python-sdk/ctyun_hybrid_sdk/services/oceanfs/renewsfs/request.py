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


class RenewSfsRequest(CTYunRequest):
    """
    只支持onDemand为false的资源进行续订，即付费方式为包年包月类型的文件系统才支持续订
    """

    def __init__(self, request_param):
        super(RenewSfsRequest, self).__init__("/v4/oceanfs/renew-sfs", "POST", "oceanfs", "application/json")
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
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
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


class RenewSfsRequestParam(object):

    def __init__(self, region_id, cycle_type, cycle_count, sfs_uid=None, resource_id=None):
        """
        :param region_id: 资源池 ID
        :param cycle_type: 计费类型
        :param cycle_count: 周期最大长度不能超过 5 年了；cycleType为year时取值1-5，cycleType为month时取值1-60
        :param sfs_uid: sfsUID和resourceID必填一个，同时存在以sfsUID为准
        :param resource_id: sfsUID和resourceID必填一个，同时存在以sfsUID为准
        """
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.sfs_uid = sfs_uid
        self.resource_id = resource_id

    def set_sfs_uid(self, sfs_uid):
        """
        :param sfs_uid: sfsUID和resourceID必填一个，同时存在以sfsUID为准
        """
        self.sfs_uid = sfs_uid

    def set_resource_id(self, resource_id):
        """
        :param resource_id: sfsUID和resourceID必填一个，同时存在以sfsUID为准
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")

