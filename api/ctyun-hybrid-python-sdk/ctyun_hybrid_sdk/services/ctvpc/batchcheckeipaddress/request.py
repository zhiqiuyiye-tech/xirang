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


class BatchCheckEipAddressRequest(CTYunRequest):
    """
    批量检查EIP地址是否被使用
    """

    def __init__(self, request_param):
        super(BatchCheckEipAddressRequest, self).__init__("/v4/eip/check-addresses", "POST", "ctvpc", "application/json")
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
        if self.parameters.eip_addresses is not None:
            body_param["eipAddresses"] = self.parameters.eip_addresses
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class BatchCheckEipAddressRequestParam(object):

    def __init__(self, region_id, eip_addresses, project_id=None):
        """
        :param region_id: 地域id
        :param eip_addresses: 弹性公网IP地址列表 注意:此参数为数组
        :param project_id: 企业项目 ID，默认为用户所在的默认企业项目
        """
        self.region_id = region_id
        self.eip_addresses = eip_addresses
        self.project_id = project_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为用户所在的默认企业项目
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.eip_addresses is None:
            raise Exception("eip_addresses can not None")

