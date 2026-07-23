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


class AcceptSharedImageRequest(CTYunRequest):
    """
    无operationId
    """

    def __init__(self, request_param):
        super(AcceptSharedImageRequest, self).__init__("/v4/image/shared-image/accept", "POST", "ctimage", "application/json")
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
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.destination_project_id is not None:
            body_param["destinationProjectID"] = self.parameters.destination_project_id
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


class AcceptSharedImageRequestParam(object):

    def __init__(self, region_id, image_id, az_name=None, destination_project_id=None):
        """
        :param region_id: 资源池 ID
        :param az_name: 可用区 公有云字段，混合云暂不支持，忽略
        :param image_id: 用户的共享镜像 ID
        :param destination_project_id: 共享镜像的接受项目id, 混合云v2只支持项目维度
        """
        self.region_id = region_id
        self.az_name = az_name
        self.image_id = image_id
        self.destination_project_id = destination_project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区 公有云字段，混合云暂不支持，忽略
        """
        self.az_name = az_name

    def set_destination_project_id(self, destination_project_id):
        """
        :param destination_project_id: 共享镜像的接受项目id, 混合云v2只支持项目维度
        """
        self.destination_project_id = destination_project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")

