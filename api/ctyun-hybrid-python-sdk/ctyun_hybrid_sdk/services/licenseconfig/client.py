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


class LicenseconfigClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('licenseconfig-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(LicenseconfigClient, self).__init__(credential, config, 'licenseconfig', '0.1.0', logger, signer)

    def open_api_query_license_info(self, open_api_query_license_info_request_param):
        """
        /v4/license/info
        查询许可证详情
        """
        return self.send(open_api_query_license_info_request_param)

    def open_api_renew_license(self, open_api_renew_license_request_param):
        """
        /v4/license/renew
        1. 许可证类型为正式时无法续期；   
    2. 单个许可证最大续期次数为2；   
    3. 每次续期时间固定为2个月。
        """
        return self.send(open_api_renew_license_request_param)

    def open_api_query_license_list(self, open_api_query_license_list_request_param):
        """
        /v4/license/list
        查询许可证列表
        """
        return self.send(open_api_query_license_list_request_param)

    def open_api_delete_license(self, open_api_delete_license_request_param):
        """
        /v4/license/delete
        仅允许删除状态为无效和已过期的许可证
        """
        return self.send(open_api_delete_license_request_param)
