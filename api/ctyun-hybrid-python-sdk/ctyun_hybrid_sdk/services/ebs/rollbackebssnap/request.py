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


class RollbackEbsSnapRequest(CTYunRequest):
    """
    混合云v1 azName为非必填且不需要传传参；v2兼容公有云和v1，azName为非必填，当资源池为4.0且传了azName则对azName进行参数校验   
    接口约束：1.快照状态为可用且快照源云硬盘为可用（云硬盘处于未挂载状态或已挂载但云主机关机）； 2.只支持回滚至源云硬盘，不支持回滚至其他云硬盘
    """

    def __init__(self, request_param):
        super(RollbackEbsSnapRequest, self).__init__("/v4/ebs_snapshot/rollback-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class RollbackEbsSnapRequestParam(object):

    def __init__(self, region_id, snapshot_id, disk_id, az_name=None):
        """
        :param region_id: 资源池ID
        :param snapshot_id: 快照ID
        :param disk_id: 快照的所属云硬盘ID
        :param az_name: 快照所属可用区(混合云不传)
        """
        self.region_id = region_id
        self.snapshot_id = snapshot_id
        self.disk_id = disk_id
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 快照所属可用区(混合云不传)
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

