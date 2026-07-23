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


class LocalDiskExtendRequest(CTYunRequest):
    """
    1 只支持单个本地盘扩容操作，不支持并发扩容，建议调用侧编排1个虚机上多块本地盘顺序扩容。   
    2 预占扩容：之前通过预占接口预占过空间，会校验传入localDiskSize是否等于原大小+预占大小。   
    3 直接扩容：之前未执行过预占，直接以传入localDiskSize为准，需大于原大小。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.CommonInternalError -- 内部错误
    """

    def __init__(self, request_param):
        super(LocalDiskExtendRequest, self).__init__("/v4/ecs/localdisk/extend", "POST", "ctecs", "application/json")
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
        if self.parameters.local_disk_id is not None:
            body_param["localDiskID"] = self.parameters.local_disk_id
        if self.parameters.local_disk_size is not None:
            body_param["localDiskSize"] = self.parameters.local_disk_size
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


class LocalDiskExtendRequestParam(object):

    def __init__(self, region_id, local_disk_id, local_disk_size, ):
        """
        :param region_id: 资源池ID
        :param local_disk_id: 本地盘ID
        :param local_disk_size: 初始为40GB，需扩容20GB，此处传60GB
        """
        self.region_id = region_id
        self.local_disk_id = local_disk_id
        self.local_disk_size = local_disk_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.local_disk_id is None:
            raise Exception("local_disk_id can not None")
        if self.local_disk_size is None:
            raise Exception("local_disk_size can not None")

