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


class UnsharePrivateImageRequest(CTYunRequest):
    """
    公有云文档是传共享镜像的接受人的名称，混合云只支持共享镜像的接受项目的id
    """

    def __init__(self, request_param):
        super(UnsharePrivateImageRequest, self).__init__("/v4/image/shared-image/delete", "POST", "ctimage", "application/json")
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
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.destination_user is not None:
            body_param["destinationUser"] = self.parameters.destination_user
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


class UnsharePrivateImageRequestParam(object):

    def __init__(self, region_id, image_id, destination_user, destination_project_id, ):
        """
        :param region_id: 资源池 ID
        :param image_id: 要取消共享的私有镜像ID
        :param destination_user: 共享镜像的接受人id
        :param destination_project_id: 共享镜像的接受项目id, 混合云v2只支持项目维度
        """
        self.region_id = region_id
        self.image_id = image_id
        self.destination_user = destination_user
        self.destination_project_id = destination_project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")
        if self.destination_user is None:
            raise Exception("destination_user can not None")
        if self.destination_project_id is None:
            raise Exception("destination_project_id can not None")

