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


class ListCertificateRequest(CTYunRequest):
    """
    获取证书列表
    """

    def __init__(self, request_param):
        super(ListCertificateRequest, self).__init__("/v4/elb/list-certificate", "GET", "ctelb", "")
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
        if self.parameters.client_token is not None:
            query_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListCertificateRequestParam(object):

    def __init__(self, region_id, client_token=None, az_name=None, project_id=None, ids=None, name=None, type=None):
        """
        :param client_token: 需要暂无功能（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param project_id: 需要暂无功能
        :param ids: 证书ID列表，以","分隔
        :param name: 证书名称
        :param type: 证书类型。取值：Ca或Server
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.ids = ids
        self.name = name
        self.type = type

    def set_client_token(self, client_token):
        """
        :param client_token: 需要暂无功能（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 需要暂无功能
        """
        self.project_id = project_id

    def set_ids(self, ids):
        """
        :param ids: 证书ID列表，以","分隔
        """
        self.ids = ids

    def set_name(self, name):
        """
        :param name: 证书名称
        """
        self.name = name

    def set_type(self, type):
        """
        :param type: 证书类型。取值：Ca或Server
        """
        self.type = type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

