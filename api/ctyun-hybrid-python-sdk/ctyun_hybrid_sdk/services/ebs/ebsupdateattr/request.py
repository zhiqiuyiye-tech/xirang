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


class EbsUpdateAttrRequest(CTYunRequest):
    """
    2.2.3及以上版本支持
    """

    def __init__(self, request_param):
        super(EbsUpdateAttrRequest, self).__init__("/v4/ebs/update-attr", "POST", "ebs", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.volume_uuid is not None:
            body_param["volumeUuid"] = self.parameters.volume_uuid
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
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


class EbsUpdateAttrRequestParam(object):

    def __init__(self, name, region_id=None, volume_uuid=None, description=None, resource_id=None):
        """
        :param region_id: 资源池id
        :param name: 新的云硬盘名称
        :param volume_uuid: volumeUuid和resourceID必填一个,同时存在以resourceID为准
        :param description: 云硬盘描述
        :param resource_id: volumeUuid和resourceID必填一个,同时存在以resourceID为准
        """
        self.region_id = region_id
        self.name = name
        self.volume_uuid = volume_uuid
        self.description = description
        self.resource_id = resource_id

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池id
        """
        self.region_id = region_id

    def set_volume_uuid(self, volume_uuid):
        """
        :param volume_uuid: volumeUuid和resourceID必填一个,同时存在以resourceID为准
        """
        self.volume_uuid = volume_uuid

    def set_description(self, description):
        """
        :param description: 云硬盘描述
        """
        self.description = description

    def set_resource_id(self, resource_id):
        """
        :param resource_id: volumeUuid和resourceID必填一个,同时存在以resourceID为准
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")

