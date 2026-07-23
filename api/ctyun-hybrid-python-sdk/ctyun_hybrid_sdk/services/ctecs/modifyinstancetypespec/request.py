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


class ModifyInstanceTypeSpecRequest(CTYunRequest):
    """
    设置云主机实例规格额外属性
    """

    def __init__(self, request_param):
        super(ModifyInstanceTypeSpecRequest, self).__init__("/v4/ecs/flavor/spec-update", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.extra_specs is not None:
            body_param["extraSpecs"] = self.parameters.extra_specs
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


class ModifyInstanceTypeSpecRequestParam(object):

    def __init__(self, region_id, flavor_id, extra_specs, az_name=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区
        :param flavor_id: 云主机规格ID
        :param extra_specs: 规格额外配置map[string]string 
        """
        self.region_id = region_id
        self.az_name = az_name
        self.flavor_id = flavor_id
        self.extra_specs = extra_specs

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")
        if self.extra_specs is None:
            raise Exception("extra_specs can not None")

