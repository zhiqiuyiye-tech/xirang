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


class EipListForManageRequest(CTYunRequest):
    """
    获取弹性IP列表管理用。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。
    """

    def __init__(self, request_param):
        super(EipListForManageRequest, self).__init__("/v4/eip/list_for_manage", "GET", "ctvpc", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.ids is not None:
            query_param["ids"] = self.parameters.ids
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.ip_type is not None:
            query_param["ipType"] = self.parameters.ip_type
        if self.parameters.eip_type is not None:
            query_param["eipType"] = self.parameters.eip_type
        if self.parameters.resource_id is not None:
            query_param["resourceId"] = self.parameters.resource_id
        if self.parameters.ignore_channel is not None:
            query_param["ignoreChannel"] = self.parameters.ignore_channel
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EipListForManageRequestParam(object):

    def __init__(self, region_id, client_token=None, project_id=None, page=None, page_size=None, ids=None, status=None, ip_type=None, eip_type=None, resource_id=None, ignore_channel=None):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        :param page: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param ids: 字符串，多个资源以逗号隔开。当resourceId与ids同时传时，取并集
        :param status: eip状态， ACTIVE（已绑定）/ DOWN（未绑定）/ FREEZING（已冻结）/ EXPIRED（已过期），不传是查询所有状态的 EIP(差异点说明，2.0不支持FREEZING) 大小写适配
        :param ip_type: ip类型支持 ipv4 / ipv6
        :param eip_type: eip类型:xinchuang/internet/cn2/bgp-3/chinamobile/chinaunicom   
         3.0 ext-net
        :param resource_id: 资源id（当resourceId与ids同时传时，取并集）
        :param ignore_channel: 渠道信息，默认不传查全部，false仅查渠道创建，true仅查界面创建
        """
        self.client_token = client_token
        self.region_id = region_id
        self.project_id = project_id
        self.page = page
        self.page_size = page_size
        self.ids = ids
        self.status = status
        self.ip_type = ip_type
        self.eip_type = eip_type
        self.resource_id = resource_id
        self.ignore_channel = ignore_channel

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_page(self, page):
        """
        :param page: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_ids(self, ids):
        """
        :param ids: 字符串，多个资源以逗号隔开。当resourceId与ids同时传时，取并集
        """
        self.ids = ids

    def set_status(self, status):
        """
        :param status: eip状态， ACTIVE（已绑定）/ DOWN（未绑定）/ FREEZING（已冻结）/ EXPIRED（已过期），不传是查询所有状态的 EIP(差异点说明，2.0不支持FREEZING) 大小写适配
        """
        self.status = status

    def set_ip_type(self, ip_type):
        """
        :param ip_type: ip类型支持 ipv4 / ipv6
        """
        self.ip_type = ip_type

    def set_eip_type(self, eip_type):
        """
        :param eip_type: eip类型:xinchuang/internet/cn2/bgp-3/chinamobile/chinaunicom   
         3.0 ext-net
        """
        self.eip_type = eip_type

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id（当resourceId与ids同时传时，取并集）
        """
        self.resource_id = resource_id

    def set_ignore_channel(self, ignore_channel):
        """
        :param ignore_channel: 渠道信息，默认不传查全部，false仅查渠道创建，true仅查界面创建
        """
        self.ignore_channel = ignore_channel

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

