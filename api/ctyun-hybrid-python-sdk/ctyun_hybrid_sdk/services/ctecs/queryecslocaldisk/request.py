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


class QueryEcsLocalDiskRequest(CTYunRequest):
    """
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.CommonInternalError -- 内部错误
    """

    def __init__(self, request_param):
        super(QueryEcsLocalDiskRequest, self).__init__("/v4/ecs/localdisk", "GET", "ctecs", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_id is not None:
            query_param["instanceID"] = self.parameters.instance_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryEcsLocalDiskRequestParam(object):

    def __init__(self, region_id, instance_id, ):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        """
        self.region_id = region_id
        self.instance_id = instance_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")

