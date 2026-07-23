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


class BatchRenewEbsRequest(CTYunRequest):
    """
    批量续订多个云硬盘，支持部分成功模式。每个云硬盘独立处理，互不影响。   
    三元组: ebs:ebs:BatchRenewEbs   
    **业务校验规则（按顺序）：**   
    1. 数量限制：最多10个.`Storage.Ebs.BatchRenewExceedLimit`   
    2. RegionID一致性：所有云硬盘必须在同一RegionID `Storage.Ebs.BatchRenewRegionNotMatch`   
    3. 云硬盘ID为空 → `Storage.Ebs.BatchRenewEmptySelection`   
    4. 状态不支持 → `Storage.Ebs.CreatingStatusNotSupportRenew`   
    
    """

    def __init__(self, request_param):
        super(BatchRenewEbsRequest, self).__init__("/v4/ebs/batch-renew-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.disk_ids is not None:
            body_param["diskIDs"] = self.parameters.disk_ids
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.cycle_cnt is not None:
            body_param["cycleCnt"] = self.parameters.cycle_cnt
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


class BatchRenewEbsRequestParam(object):

    def __init__(self, disk_ids, cycle_cnt, region_id=None):
        """
        :param disk_ids: 最多10个 注意:此参数为数组
        :param region_id: 资源池ID
        :param cycle_cnt: 单位:月
        """
        self.disk_ids = disk_ids
        self.region_id = region_id
        self.cycle_cnt = cycle_cnt

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.disk_ids is None:
            raise Exception("disk_ids can not None")
        if self.cycle_cnt is None:
            raise Exception("cycle_cnt can not None")

