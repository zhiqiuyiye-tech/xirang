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


class OpenapiGetServiceListRequest(CTYunRequest):
    """
    服务管理列表
    """

    def __init__(self, request_param):
        super(OpenapiGetServiceListRequest, self).__init__("/v1/service/getServiceList", "GET", "iam", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.cloud_type is not None:
            query_param["cloudType"] = self.parameters.cloud_type
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.code is not None:
            query_param["code"] = self.parameters.code
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenapiGetServiceListRequestParam(object):

    def __init__(self, page=None, page_size=None, name=None, cloud_type=None, type=None, code=None):
        """
        :param page: 页码, 需大于0,缺省时为1 ,需为整形 注意:此参数为数组
        :param page_size: 页大小,需大于0,缺省时为10 ,需为整形 注意:此参数为数组
        :param name: 服务名称, 模糊匹配
        :param cloud_type: 云类型 3- 天翼云自研池子 11-VMWARE 50-ZSTACK
        :param type: 授权范围 1 资源池级 2 全局级
        :param code: 服务编码, 模糊匹配
        """
        self.page = page
        self.page_size = page_size
        self.name = name
        self.cloud_type = cloud_type
        self.type = type
        self.code = code

    def set_page(self, page):
        """
        :param page: 页码, 需大于0,缺省时为1 ,需为整形
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小,需大于0,缺省时为10 ,需为整形
        """
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 服务名称, 模糊匹配
        """
        self.name = name

    def set_cloud_type(self, cloud_type):
        """
        :param cloud_type: 云类型 3- 天翼云自研池子 11-VMWARE 50-ZSTACK
        """
        self.cloud_type = cloud_type

    def set_type(self, type):
        """
        :param type: 授权范围 1 资源池级 2 全局级
        """
        self.type = type

    def set_code(self, code):
        """
        :param code: 服务编码, 模糊匹配
        """
        self.code = code

    def check_param(self):
        """
        the param required check
        """
        pass

