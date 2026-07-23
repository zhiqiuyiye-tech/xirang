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


class LocalDiskExtendCancelRequest(CTYunRequest):
    """
    1 支持一次取消多个AZ下多个虚机的多个本地盘的预占。   
    2 本地盘状态为 allocated 时自动跳过，视为成功。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.LocalDisk.CancelFailed -- 取消预占失败   
    Compute.CommonInternalError -- 内部错误
    """

    def __init__(self, request_param):
        super(LocalDiskExtendCancelRequest, self).__init__("/v4/ecs/localdisk/extend-cancel", "POST", "ctecs", "application/json")
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
        if self.parameters.local_disk_ids is not None:
            body_param["localDiskIDs"] = self.parameters.local_disk_ids
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


class LocalDiskExtendCancelRequestParam(object):

    def __init__(self, region_id, local_disk_ids, ):
        """
        :param region_id: 资源池ID
        :param local_disk_ids: 本地盘ID集合 注意:此参数为数组
        """
        self.region_id = region_id
        self.local_disk_ids = local_disk_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.local_disk_ids is None:
            raise Exception("local_disk_ids can not None")

