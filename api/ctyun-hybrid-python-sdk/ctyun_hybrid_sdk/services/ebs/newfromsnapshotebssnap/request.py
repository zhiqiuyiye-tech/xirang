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


class NewFromSnapshotEbsSnapRequest(CTYunRequest):
    """
    从快照创建云硬盘
    """

    def __init__(self, request_param):
        super(NewFromSnapshotEbsSnapRequest, self).__init__("/v4/ebs/new-from-snapshot-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.multi_attach is not None:
            body_param["multiAttach"] = self.parameters.multi_attach
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.disk_mode is not None:
            body_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.disk_name is not None:
            body_param["diskName"] = self.parameters.disk_name
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
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


class NewFromSnapshotEbsSnapRequestParam(object):

    def __init__(self, region_id, disk_mode, disk_name, disk_size, snapshot_id, client_token=None, multi_attach=None, project_id=None, on_demand=None, cycle_type=None, cycle_count=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云暂不支持，忽略
        :param region_id: 资源池Id
        :param multi_attach: 是否多云主机挂载，默认false
        :param project_id: 企业项目ID,默认为”0”。公有云字段，混合云暂不支持，忽略
        :param disk_mode: 磁盘模式:VBD/ISCSI
        :param disk_name: 磁盘命名，单账户单资源池下，命名需唯一。
        :param disk_size: 磁盘大小，单位GB，容量不小于快照容量。不超过32768
        :param on_demand: 是否按需下单。默认为true
        :param cycle_type: 包周期类型：year/month。onDemand为false时，必须指定
        :param cycle_count: 包周期数 onDemand为false时，必须指定，周期最大长度不能超过5年。
        :param snapshot_id: 快照id
        """
        self.client_token = client_token
        self.region_id = region_id
        self.multi_attach = multi_attach
        self.project_id = project_id
        self.disk_mode = disk_mode
        self.disk_name = disk_name
        self.disk_size = disk_size
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.snapshot_id = snapshot_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云暂不支持，忽略
        """
        self.client_token = client_token

    def set_multi_attach(self, multi_attach):
        """
        :param multi_attach: 是否多云主机挂载，默认false
        """
        self.multi_attach = multi_attach

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID,默认为”0”。公有云字段，混合云暂不支持，忽略
        """
        self.project_id = project_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需下单。默认为true
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期类型：year/month。onDemand为false时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数 onDemand为false时，必须指定，周期最大长度不能超过5年。
        """
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.disk_mode is None:
            raise Exception("disk_mode can not None")
        if self.disk_name is None:
            raise Exception("disk_name can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")

