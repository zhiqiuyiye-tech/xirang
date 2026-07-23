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


class ResizeInstanceRequest(CTYunRequest):
    """
    支持对一台已经关机中的云主机进行规格变更   
       
    ### 接口约束   
       
    1. 目标云主机处于关机中   
    2. 仅支持规格向高配变更
    """

    def __init__(self, request_param):
        super(ResizeInstanceRequest, self).__init__("/v4/ecs/resize", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
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


class ResizeInstanceRequestParam(object):

    def __init__(self, client_token, region_id, flavor_id, id, az_name=None):
        """
        :param az_name: 可用区名称
        :param client_token: 混合云非必传
        :param region_id: 资源池ID 
        :param flavor_id: 目标规格ID或名称
        :param id: 云主机ID(资源id也兼容)
        """
        self.az_name = az_name
        self.client_token = client_token
        self.region_id = region_id
        self.flavor_id = flavor_id
        self.id = id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")
        if self.id is None:
            raise Exception("id can not None")

