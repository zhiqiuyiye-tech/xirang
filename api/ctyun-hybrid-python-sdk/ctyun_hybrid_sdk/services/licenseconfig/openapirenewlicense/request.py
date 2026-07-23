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


class OpenAPIRenewLicenseRequest(CTYunRequest):
    """
    1. 许可证类型为正式时无法续期；   
    2. 单个许可证最大续期次数为2；   
    3. 每次续期时间固定为2个月。
    """

    def __init__(self, request_param):
        super(OpenAPIRenewLicenseRequest, self).__init__("/v4/license/renew", "POST", "licenseconfig", "application/json")
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
        if self.parameters.license_id is not None:
            body_param["licenseID"] = self.parameters.license_id
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


class OpenAPIRenewLicenseRequestParam(object):

    def __init__(self, license_id, ):
        """
        :param license_id: 许可证唯一ID
        """
        self.license_id = license_id

    def check_param(self):
        """
        the param required check
        """
        if self.license_id is None:
            raise Exception("license_id can not None")

