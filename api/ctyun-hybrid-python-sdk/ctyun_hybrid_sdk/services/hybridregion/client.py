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


class HybridregionClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('hybridregion-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(HybridregionClient, self).__init__(credential, config, 'hybridregion', '0.1.0', logger, signer)

    def open_api_get_az_list(self, open_api_get_az_list_request_param):
        """
        /v1/azs/list
        查询可用区
        """
        return self.send(open_api_get_az_list_request_param)

    def sync_azs(self, sync_azs_request_param):
        """
        /v1/regions/azs/sync
        同步可用区信息
        """
        return self.send(sync_azs_request_param)

    def switch_az_status(self, switch_az_status_request_param):
        """
        /v1/azs/switch-status
        切换可用区状态
        """
        return self.send(switch_az_status_request_param)

    def get_region_type_list(self, get_region_type_list_request_param):
        """
        /v1/regions/region-type
        查询资源池类型列表
        """
        return self.send(get_region_type_list_request_param)

    def create_az(self, create_az_request_param):
        """
        /v1/azs/create
        创建可用区
        """
        return self.send(create_az_request_param)

    def switch_region_status(self, switch_region_status_request_param):
        """
        /v1/regions/switch-status
        切换资源池状态
        """
        return self.send(switch_region_status_request_param)

    def get_region_config(self, get_region_config_request_param):
        """
        /v1/regions/region-config
        获取资源池配置信息列表
        """
        return self.send(get_region_config_request_param)

    def edit_az(self, edit_az_request_param):
        """
        /v1/azs/edit-az
        编辑可用区
        """
        return self.send(edit_az_request_param)

    def get_region_detail(self, get_region_detail_request_param):
        """
        /v1/regions/detail
        查询资源池详情
        """
        return self.send(get_region_detail_request_param)
