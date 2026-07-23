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


class EcsHostPageListRequest(CTYunRequest):
    """
    查询宿主机列表
    """

    def __init__(self, request_param):
        super(EcsHostPageListRequest, self).__init__("/v4/hosts/by-page", "GET", "ctecs", "")
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
        if self.parameters.az_id is not None:
            query_param["azID"] = self.parameters.az_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.state is not None:
            query_param["state"] = self.parameters.state
        if self.parameters.ha_status is not None:
            query_param["haStatus"] = self.parameters.ha_status
        if self.parameters.region_name is not None:
            query_param["regionName"] = self.parameters.region_name
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.zone_name is not None:
            query_param["zoneName"] = self.parameters.zone_name
        if self.parameters.zone_param is not None:
            query_param["zoneParam"] = self.parameters.zone_param
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.uuid is not None:
            query_param["uuid"] = self.parameters.uuid
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EcsHostPageListRequestParam(object):

    def __init__(self, region_id, az_id=None, page=None, page_size=None, status=None, state=None, ha_status=None, region_name=None, az_name=None, sort=None, asc=None, zone_name=None, zone_param=None, query_content=None, name=None, uuid=None):
        """
        :param region_id: 资源池UUID
        :param az_id: 可用区id
        :param page: 当前页
        :param page_size: 每页数量
        :param status: 宿主机启用状态
        :param state: 宿主机健康状态，多个，分割
        :param ha_status: Ha状态，多个，分割
        :param region_name: 资源池名称，多个，分割
        :param az_name: 可用区名称，多个，分割
        :param sort: 排序相关字段（指定排序字段），updated_time,running_vms,cpu_ratio,cpu_used_rate,ram_ratio,mem_used_rate
        :param asc: 排序字段（排列方式），asc-升，desc-降
        :param zone_name: 集群名称搜索宿主机列表，精确查询
        :param zone_param: 集群名称搜索，模糊查询
        :param query_content: 支持名称或uuid
        :param name: 宿主机名称，模糊
        :param uuid: uuid，模糊
        """
        self.region_id = region_id
        self.az_id = az_id
        self.page = page
        self.page_size = page_size
        self.status = status
        self.state = state
        self.ha_status = ha_status
        self.region_name = region_name
        self.az_name = az_name
        self.sort = sort
        self.asc = asc
        self.zone_name = zone_name
        self.zone_param = zone_param
        self.query_content = query_content
        self.name = name
        self.uuid = uuid

    def set_az_id(self, az_id):
        """
        :param az_id: 可用区id
        """
        self.az_id = az_id

    def set_page(self, page):
        """
        :param page: 当前页
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页数量
        """
        self.page_size = page_size

    def set_status(self, status):
        """
        :param status: 宿主机启用状态
        """
        self.status = status

    def set_state(self, state):
        """
        :param state: 宿主机健康状态，多个，分割
        """
        self.state = state

    def set_ha_status(self, ha_status):
        """
        :param ha_status: Ha状态，多个，分割
        """
        self.ha_status = ha_status

    def set_region_name(self, region_name):
        """
        :param region_name: 资源池名称，多个，分割
        """
        self.region_name = region_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，多个，分割
        """
        self.az_name = az_name

    def set_sort(self, sort):
        """
        :param sort: 排序相关字段（指定排序字段），updated_time,running_vms,cpu_ratio,cpu_used_rate,ram_ratio,mem_used_rate
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: 排序字段（排列方式），asc-升，desc-降
        """
        self.asc = asc

    def set_zone_name(self, zone_name):
        """
        :param zone_name: 集群名称搜索宿主机列表，精确查询
        """
        self.zone_name = zone_name

    def set_zone_param(self, zone_param):
        """
        :param zone_param: 集群名称搜索，模糊查询
        """
        self.zone_param = zone_param

    def set_query_content(self, query_content):
        """
        :param query_content: 支持名称或uuid
        """
        self.query_content = query_content

    def set_name(self, name):
        """
        :param name: 宿主机名称，模糊
        """
        self.name = name

    def set_uuid(self, uuid):
        """
        :param uuid: uuid，模糊
        """
        self.uuid = uuid

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

