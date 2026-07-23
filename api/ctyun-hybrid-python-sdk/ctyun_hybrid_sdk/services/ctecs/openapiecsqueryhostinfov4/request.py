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


class OpenapiEcsQueryHostInfoV4Request(CTYunRequest):
    """
    该接口通过云主机ID查询云主机所在宿主机信息。**注意**:ID或instanceID必传其中一个，公有云为ID   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.AvailableZoneNotFound -- 非法的可用区   
    Compute.Param.Error -- 参数错误   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.Host.NotFoundError -- 非法的宿主机   
    Compute.CommonInternalError -- 内部错误
    """

    def __init__(self, request_param):
        super(OpenapiEcsQueryHostInfoV4Request, self).__init__("/v4/ecs/query-host-info", "GET", "ctecs", "")
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
        if self.parameters.id is not None:
            query_param["ID"] = self.parameters.id
        if self.parameters.only_name is not None:
            query_param["onlyName"] = self.parameters.only_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenapiEcsQueryHostInfoV4RequestParam(object):

    def __init__(self, region_id, id, only_name=None):
        """
        :param region_id: 资源池id
        :param id: 云主机id (ID或instanceID必传其中一个)
        :param only_name: 取值范围：["true", "false"], 其他值无效，默认值："true"，注：该参数只在3.0资源池有效，在3.0资源池如果选择"false"，则会因为查询其他信息增加接口耗时
        """
        self.region_id = region_id
        self.id = id
        self.only_name = only_name

    def set_only_name(self, only_name):
        """
        :param only_name: 取值范围：["true", "false"], 其他值无效，默认值："true"，注：该参数只在3.0资源池有效，在3.0资源池如果选择"false"，则会因为查询其他信息增加接口耗时
        """
        self.only_name = only_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

