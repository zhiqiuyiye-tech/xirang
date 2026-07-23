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


class EcsListByTypeFamiliesRequest(CTYunRequest):
    """
    该接口提供用户根据指定规格族查询云主机的名称、云主机ID及规格详情
    """

    def __init__(self, request_param):
        super(EcsListByTypeFamiliesRequest, self).__init__("/v4/ecs/list-by-typefamilies", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.type_family is not None:
            body_param["type_family"] = self.parameters.type_family
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class EcsListByTypeFamiliesRequestParam(object):

    def __init__(self, region_id, type_family, az_name=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param az_name: 您可以调用获取[资源池信息](https://app.apifox.com/link/project/4152543/apis/api-154988743)，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        :param type_family: 可根据查询云主机规格族列表进行查询
        :param page_no: 取值范围：大于等于1，默认值为1
        :param page_size: 取值范围:[1~50]，默认值:10，单页最大记录不超过50
        """
        self.region_id = region_id
        self.az_name = az_name
        self.type_family = type_family
        self.page_no = page_no
        self.page_size = page_size

    def set_az_name(self, az_name):
        """
        :param az_name: 您可以调用获取[资源池信息](https://app.apifox.com/link/project/4152543/apis/api-154988743)，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        """
        self.az_name = az_name

    def set_page_no(self, page_no):
        """
        :param page_no: 取值范围：大于等于1，默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 取值范围:[1~50]，默认值:10，单页最大记录不超过50
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.type_family is None:
            raise Exception("type_family can not None")

