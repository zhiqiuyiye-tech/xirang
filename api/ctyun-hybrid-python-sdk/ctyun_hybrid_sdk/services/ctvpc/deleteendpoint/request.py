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


class DeleteEndpointRequest(CTYunRequest):
    """
    删除终端节点
    """

    def __init__(self, request_param):
        super(DeleteEndpointRequest, self).__init__("/v4/vpce/delete-endpoint", "POST", "ctvpc", "application/json")
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
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.endpoint_id is not None:
            body_param["endpointID"] = self.parameters.endpoint_id
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


class DeleteEndpointRequestParam(object):

    def __init__(self, region_id, resource_id=None, endpoint_id=None):
        """
        :param region_id: 资源池ID
        :param resource_id: resourceID和endpointID必填其中一个
        :param endpoint_id: resourceID和endpointID必填其中一个
        """
        self.region_id = region_id
        self.resource_id = resource_id
        self.endpoint_id = endpoint_id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: resourceID和endpointID必填其中一个
        """
        self.resource_id = resource_id

    def set_endpoint_id(self, endpoint_id):
        """
        :param endpoint_id: resourceID和endpointID必填其中一个
        """
        self.endpoint_id = endpoint_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

