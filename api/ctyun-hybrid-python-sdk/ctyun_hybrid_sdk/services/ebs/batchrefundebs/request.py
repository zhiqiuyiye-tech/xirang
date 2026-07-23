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


class BatchRefundEbsRequest(CTYunRequest):
    """
    批量退订多个云硬盘，支持部分成功模式。每个云硬盘独立处理，互不影响。   
       
    **业务校验规则（按顺序）：**   
    1. 数量限制：最多10个（接口级错误）   
    2. RegionID一致性：所有云硬盘必须在同一RegionID（接口级错误）   
    3. 云硬盘不存在 → `Storage.Ebs.NotFound`   
    4. 状态非available → `Storage.Ebs.NotAvailableStatus`   
    5. 已在回收站(freezed=true) → `Storage.Ebs.AlreadyInRecycleBin`   
    6. 绑定快照/备份策略 → `Storage.Ebs.BindPolicy`   
    7. 包年包月已到期 → `Storage.Ebs.YearMonthExpired`   
    
    """

    def __init__(self, request_param):
        super(BatchRefundEbsRequest, self).__init__("/v4/ebs/batch-refund-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class BatchRefundEbsRequestParam(object):

    def __init__(self, disk_ids, region_id=None, client_token=None):
        """
        :param disk_ids: 最多10个 注意:此参数为数组
        :param region_id: 资源池ID
        :param client_token: 用于保证订单幂等性
        """
        self.disk_ids = disk_ids
        self.region_id = region_id
        self.client_token = client_token

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID
        """
        self.region_id = region_id

    def set_client_token(self, client_token):
        """
        :param client_token: 用于保证订单幂等性
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.disk_ids is None:
            raise Exception("disk_ids can not None")

