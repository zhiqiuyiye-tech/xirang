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


class GetInstanceListLiteVdcRequest(CTYunRequest):
    """
    v2.2.5版本支持
    """

    def __init__(self, request_param):
        super(GetInstanceListLiteVdcRequest, self).__init__("/v4/ecs/instance-list-lite-vdc", "GET", "ctecs", "")
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
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        if self.parameters.instance_id is not None:
            query_param["instanceID"] = self.parameters.instance_id
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.keyword is not None:
            query_param["keyword"] = self.parameters.keyword
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetInstanceListLiteVdcRequestParam(object):

    def __init__(self, region_id, org_id=None, instance_id=None, page_size=None, page_no=None, keyword=None, az_name=None):
        """
        :param region_id: 资源池ID
        :param org_id: 组织id
        :param instance_id: 主机uuid，多个用,分割(支持最多20个ID)
        :param page_size: 每页记录数目 最大50   
         
        :param page_no: 页码
        :param keyword: 模糊搜索参数(uuid,name,displayName,privateIp)
        :param az_name: 可用区id
        """
        self.region_id = region_id
        self.org_id = org_id
        self.instance_id = instance_id
        self.page_size = page_size
        self.page_no = page_no
        self.keyword = keyword
        self.az_name = az_name

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 主机uuid，多个用,分割(支持最多20个ID)
        """
        self.instance_id = instance_id

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目 最大50   
         
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_keyword(self, keyword):
        """
        :param keyword: 模糊搜索参数(uuid,name,displayName,privateIp)
        """
        self.keyword = keyword

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区id
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

