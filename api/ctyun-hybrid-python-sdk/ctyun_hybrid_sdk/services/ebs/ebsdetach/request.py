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


class EbsDetachRequest(CTYunRequest):
    """
    云硬盘解绑
    """

    def __init__(self, request_param):
        super(EbsDetachRequest, self).__init__("/v4/ebs/detach", "POST", "ebs", "application/json")
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
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
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


class EbsDetachRequestParam(object):

    def __init__(self, resource_id, region_id=None, instance_uuid=None):
        """
        :param region_id: 区域ID,如本地语境支持保存regionID，那么建议传递。
        :param instance_uuid: 虚机id(共享盘的时候必传)
        :param resource_id: 资源ID
        """
        self.region_id = region_id
        self.instance_uuid = instance_uuid
        self.resource_id = resource_id

    def set_region_id(self, region_id):
        """
        :param region_id: 区域ID,如本地语境支持保存regionID，那么建议传递。
        """
        self.region_id = region_id

    def set_instance_uuid(self, instance_uuid):
        """
        :param instance_uuid: 虚机id(共享盘的时候必传)
        """
        self.instance_uuid = instance_uuid

    def check_param(self):
        """
        the param required check
        """
        if self.resource_id is None:
            raise Exception("resource_id can not None")

