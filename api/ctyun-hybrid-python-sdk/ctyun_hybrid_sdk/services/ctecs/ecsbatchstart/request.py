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


class EcsBatchStartRequest(CTYunRequest):
    """
    启动一台或多台实例
    """

    def __init__(self, request_param):
        super(EcsBatchStartRequest, self).__init__("/v4/ecs/batch-start", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class EcsBatchStartRequestParam(object):

    def __init__(self, region_id, instance_id_list, az_name=None):
        """
        :param region_id: 资源池ID
        :param instance_id_list: ecs实例ID列表，字符串，英文逗号分割
        :param az_name: 可用区名称 -未提供 可不传
        """
        self.region_id = region_id
        self.instance_id_list = instance_id_list
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称 -未提供 可不传
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id_list is None:
            raise Exception("instance_id_list can not None")

