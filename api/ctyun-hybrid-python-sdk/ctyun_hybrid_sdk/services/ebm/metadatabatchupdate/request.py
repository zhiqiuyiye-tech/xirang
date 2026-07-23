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


class MetadataBatchUpdateRequest(CTYunRequest):
    """
    只有弹性裸金属制成元数据
    """

    def __init__(self, request_param):
        super(MetadataBatchUpdateRequest, self).__init__("/v4/ebm/metadata/batch-update", "POST", "ebm", "application/json")
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
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.metadata is not None:
            body_param["metadata"] = self.parameters.metadata
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


class MetadataBatchUpdateRequestParam(object):

    def __init__(self, region_id, instance_uuid, metadata, az_name=None):
        """
        :param region_id: 区域ID
        :param az_name: 可用区
        :param instance_uuid: 实例uuid
        :param metadata: 元数据信息;结构为字典类型，其中key和value均为String类型参数，key的长度必须小于257
        """
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid = instance_uuid
        self.metadata = metadata

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
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.metadata is None:
            raise Exception("metadata can not None")

