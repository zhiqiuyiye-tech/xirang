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


class OpenapiDeleteServiceRequest(CTYunRequest):
    """
    服务管理删除
    """

    def __init__(self, request_param):
        super(OpenapiDeleteServiceRequest, self).__init__("/v1/service/deleteService", "GET", "iam", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.service_id is not None:
            query_param["serviceID"] = self.parameters.service_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenapiDeleteServiceRequestParam(object):

    def __init__(self, service_id=None):
        """
        :param service_id: 服务ID
        """
        self.service_id = service_id

    def set_service_id(self, service_id):
        """
        :param service_id: 服务ID
        """
        self.service_id = service_id

    def check_param(self):
        """
        the param required check
        """
        pass

