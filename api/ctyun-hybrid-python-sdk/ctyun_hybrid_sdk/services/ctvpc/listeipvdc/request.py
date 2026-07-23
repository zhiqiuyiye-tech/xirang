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


class ListEipVdcRequest(CTYunRequest):
    """
    查询指定地域已创建的EIP。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。混合云入参缺失ipType和eipType两个字段，非必填字段，暂不做调整
    """

    def __init__(self, request_param):
        super(ListEipVdcRequest, self).__init__("/v4/eip/list-vdc", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.ids is not None:
            body_param["ids"] = self.parameters.ids
        if self.parameters.ip_type is not None:
            body_param["ipType"] = self.parameters.ip_type
        if self.parameters.eip_type is not None:
            body_param["eipType"] = self.parameters.eip_type
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
        if self.parameters.resource_id is not None:
            body_param["resourceId"] = self.parameters.resource_id
        if self.parameters.org_id is not None:
            body_param["orgId"] = self.parameters.org_id
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


class ListEipVdcRequestParam(object):

    def __init__(self, region_id, client_token=None, project_id=None, page=None, page_size=None, ids=None, ip_type=None, eip_type=None, status=None, resource_id=None, org_id=None):
        """
        :param region_id: 资源池ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际用不到）
        :param project_id: 企业项目 ID
        :param page: 分页参数，小于0默认为1
        :param page_size: 每页数据量大小，取值 1-50，超过50默认为50，不填默认10
        :param ids: 是 Array 类型，里面的内容是 String（当resourceId与ids同时传时取并集） 注意:此参数为数组
        :param ip_type: ip类型  ipv4 / ipv6 
        :param eip_type: eip类型:xinchuang/internet/cn2/bgp-3/chinamobile/chinaunicom;   
         3.0 ext-net
        :param status: 绑定网卡状态 DOWN 未绑定, ACTIVE 绑定
        :param resource_id: 资源id（当resourceId与ids同时传时取并集）
        :param org_id: 组织id，若传了projectID，则以projectID优先
        """
        self.region_id = region_id
        self.client_token = client_token
        self.project_id = project_id
        self.page = page
        self.page_size = page_size
        self.ids = ids
        self.ip_type = ip_type
        self.eip_type = eip_type
        self.status = status
        self.resource_id = resource_id
        self.org_id = org_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际用不到）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID
        """
        self.project_id = project_id

    def set_page(self, page):
        """
        :param page: 分页参数，小于0默认为1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页数据量大小，取值 1-50，超过50默认为50，不填默认10
        """
        self.page_size = page_size

    def set_ids(self, ids):
        """
        :param ids: 是 Array 类型，里面的内容是 String（当resourceId与ids同时传时取并集）
        """
        self.ids = ids

    def set_ip_type(self, ip_type):
        """
        :param ip_type: ip类型  ipv4 / ipv6 
        """
        self.ip_type = ip_type

    def set_eip_type(self, eip_type):
        """
        :param eip_type: eip类型:xinchuang/internet/cn2/bgp-3/chinamobile/chinaunicom;   
         3.0 ext-net
        """
        self.eip_type = eip_type

    def set_status(self, status):
        """
        :param status: 绑定网卡状态 DOWN 未绑定, ACTIVE 绑定
        """
        self.status = status

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id（当resourceId与ids同时传时取并集）
        """
        self.resource_id = resource_id

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id，若传了projectID，则以projectID优先
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

