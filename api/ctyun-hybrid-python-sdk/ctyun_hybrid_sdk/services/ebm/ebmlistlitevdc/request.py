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


class EbmListLiteVdcRequest(CTYunRequest):
    """
    裸金属轻量信息列表-vdc
    """

    def __init__(self, request_param):
        super(EbmListLiteVdcRequest, self).__init__("/v4/ebm/list-lite-vdc", "GET", "ebm", "")
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
        if self.parameters.display_name is not None:
            query_param["displayName"] = self.parameters.display_name
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        if self.parameters.instance_uuid_list is not None:
            query_param["instanceUUIDList"] = self.parameters.instance_uuid_list
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EbmListLiteVdcRequestParam(object):

    def __init__(self, region_id, display_name=None, id=None, page_no=None, page_size=None, az_name=None, org_id=None, instance_uuid_list=None):
        """
        :param region_id: 区域ID 
        :param display_name: 实例名称
        :param id: 物理机id
        :param page_no: 页码，不传时默认第一页，无限制
        :param page_size: 每页展示条目, 不传时默认每页展示10条数据，取值范围1-1000
        :param az_name: 可用区
        :param org_id: 组织id，对齐v1，支持vdc下钻
        :param instance_uuid_list: 物理机id，多个用,分割(支持最多20个ID)
        """
        self.region_id = region_id
        self.display_name = display_name
        self.id = id
        self.page_no = page_no
        self.page_size = page_size
        self.az_name = az_name
        self.org_id = org_id
        self.instance_uuid_list = instance_uuid_list

    def set_display_name(self, display_name):
        """
        :param display_name: 实例名称
        """
        self.display_name = display_name

    def set_id(self, id):
        """
        :param id: 物理机id
        """
        self.id = id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，不传时默认第一页，无限制
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页展示条目, 不传时默认每页展示10条数据，取值范围1-1000
        """
        self.page_size = page_size

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id，对齐v1，支持vdc下钻
        """
        self.org_id = org_id

    def set_instance_uuid_list(self, instance_uuid_list):
        """
        :param instance_uuid_list: 物理机id，多个用,分割(支持最多20个ID)
        """
        self.instance_uuid_list = instance_uuid_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

