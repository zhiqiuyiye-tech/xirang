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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class ResourcecenterClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('resourcecenter-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(ResourcecenterClient, self).__init__(credential, config, 'resourcecenter', '0.1.0', logger, signer)

    def create_public_label(self, create_public_label_request_param):
        """
        /v4/resource-center/label/create/public
        创建自定义（公共）标签
        """
        return self.send(create_public_label_request_param)

    def list_public_label(self, list_public_label_request_param):
        """
        /v4/resource-center/label/list/public
        查询自定义标签列表
        """
        return self.send(list_public_label_request_param)

    def list_preset_label(self, list_preset_label_request_param):
        """
        /v4/resource-center/label/list/preset
        查询预置标签列表
        """
        return self.send(list_preset_label_request_param)

    def label_un_bind_resource(self, label_un_bind_resource_request_param):
        """
        /v4/resource-center/label/unbind
        标签解绑资源
        """
        return self.send(label_un_bind_resource_request_param)

    def create_preset_label(self, create_preset_label_request_param):
        """
        /v4/resource-center/label/create/preset
        创建预置标签
        """
        return self.send(create_preset_label_request_param)

    def delete_preset_label(self, delete_preset_label_request_param):
        """
        /v4/resource-center/label/delete/preset
        删除标签同时`解绑`其关联的所有资源
        """
        return self.send(delete_preset_label_request_param)

    def list_label(self, list_label_request_param):
        """
        /v4/resource-center/label/list
        查询标签列表
        """
        return self.send(list_label_request_param)

    def delete_public_label(self, delete_public_label_request_param):
        """
        /v4/resource-center/label/delete/public
        删除标签同时`解绑`其关联的所有资源
        """
        return self.send(delete_public_label_request_param)

    def create_label(self, create_label_request_param):
        """
        /v4/resource-center/label/create
        创建标签
        """
        return self.send(create_label_request_param)

    def delete_label(self, delete_label_request_param):
        """
        /v4/resource-center/label/delete
        删除标签同时`解绑`其关联的所有资源
        """
        return self.send(delete_label_request_param)

    def label_bind_resource(self, label_bind_resource_request_param):
        """
        /v4/resource-center/label/bind
        标签绑定资源
        """
        return self.send(label_bind_resource_request_param)
