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


class DetachEbmVolumeRequest(CTYunRequest):
    """
    物理机卸载卷   
       
    注意：当资源池为3.0时，azName字段需填写default
    """

    def __init__(self, request_param):
        super(DetachEbmVolumeRequest, self).__init__("/v4/ebm/detach-volume", "POST", "ebm", "application/json")
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
        if self.parameters.volume_id is not None:
            body_param["volumeID"] = self.parameters.volume_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class DetachEbmVolumeRequestParam(object):

    def __init__(self, region_id, instance_uuid, volume_id, az_name=None, client_token=None):
        """
        :param region_id: 区域ID
        :param az_name: 可用区
        :param instance_uuid: 裸机id（裸机开机可以进行绑定，裸机关机状态下才能进行解绑）
        :param volume_id: 卷id（status为"ROOT"为系统盘无法进行绑定、解绑）
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid = instance_uuid
        self.volume_id = volume_id
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.volume_id is None:
            raise Exception("volume_id can not None")

