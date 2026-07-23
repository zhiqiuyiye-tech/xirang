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


class EcsKeypairDescribeRequest(CTYunRequest):
    """
    此接口提供用户查询SSH密钥对功能。系统会接收用户输入的查询条件，并返回符合条件的密钥对详细信息。用户可根据此接口的返回值了解对应条件下的密钥对信息。
    """

    def __init__(self, request_param):
        super(EcsKeypairDescribeRequest, self).__init__("/v4/ecs/keypair/describe", "POST", "ctecs", "application/json")
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
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class EcsKeypairDescribeRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, name=None, project_id=None):
        """
        :param region_id: 资源池id
        :param page_no: 页码，默认值:1
        :param page_size: 最大为100
        :param name: 名称
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.name = name
        self.project_id = project_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值:1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 最大为100
        """
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

