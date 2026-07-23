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


class CloudvpnUserUpdateRequest(CTYunRequest):
    """
    客户信息修改
    """

    def __init__(self, request_param):
        super(CloudvpnUserUpdateRequest, self).__init__("/v4/cloudvpn/user/update", "POST", "cda", "application/json")
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
        if self.parameters.customer_name is not None:
            body_param["customerName"] = self.parameters.customer_name
        if self.parameters.customer_contact is not None:
            body_param["customerContact"] = self.parameters.customer_contact
        if self.parameters.customer_manager_name is not None:
            body_param["customerManagerName"] = self.parameters.customer_manager_name
        if self.parameters.customer_manager_contact is not None:
            body_param["customerManagerContact"] = self.parameters.customer_manager_contact
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


class CloudvpnUserUpdateRequestParam(object):

    def __init__(self, region_id, customer_name, customer_contact, customer_manager_name, customer_manager_contact, ):
        """
        :param region_id: 资源池id
        :param customer_name: 长度2-63
        :param customer_contact: 客户联系方式
        :param customer_manager_name: 长度2-63
        :param customer_manager_contact: 客户经理联系方式
        """
        self.region_id = region_id
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.customer_manager_name = customer_manager_name
        self.customer_manager_contact = customer_manager_contact

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.customer_name is None:
            raise Exception("customer_name can not None")
        if self.customer_contact is None:
            raise Exception("customer_contact can not None")
        if self.customer_manager_name is None:
            raise Exception("customer_manager_name can not None")
        if self.customer_manager_contact is None:
            raise Exception("customer_manager_contact can not None")

