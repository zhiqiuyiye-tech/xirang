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


class DeleteEbsSnapRequest(CTYunRequest):
    """
    开发未对齐原因：混合云直接删除(非异步任务)，公有云走工单删除   
    **删除云硬盘快照**：该接口现在为同步接口，不返回jobid
    """

    def __init__(self, request_param):
        super(DeleteEbsSnapRequest, self).__init__("/v4/ebs_snapshot/delete-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_ids is not None:
            body_param["snapshotIDs"] = self.parameters.snapshot_ids
        if self.parameters.refund_order is not None:
            body_param["refundOrder"] = self.parameters.refund_order
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
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


class DeleteEbsSnapRequestParam(object):

    def __init__(self, region_id, snapshot_ids, disk_id, refund_order=None):
        """
        :param region_id: 资源池ID
        :param snapshot_ids: 云硬盘快照ID，字符串数组 注意:此参数为数组
        :param refund_order: 是否退订该硬盘下的所有的快照，True时将删除所有的快照并删除订单，False时只删除快照不删除订单 (公有云字段，混合云暂不匹配，忽略)
        :param disk_id: 云硬盘ID 
        """
        self.region_id = region_id
        self.snapshot_ids = snapshot_ids
        self.refund_order = refund_order
        self.disk_id = disk_id

    def set_refund_order(self, refund_order):
        """
        :param refund_order: 是否退订该硬盘下的所有的快照，True时将删除所有的快照并删除订单，False时只删除快照不删除订单 (公有云字段，混合云暂不匹配，忽略)
        """
        self.refund_order = refund_order

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_ids is None:
            raise Exception("snapshot_ids can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

