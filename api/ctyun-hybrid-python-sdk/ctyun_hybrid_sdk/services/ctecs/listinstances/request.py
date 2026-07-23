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


class ListInstancesRequest(CTYunRequest):
    """
    该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机信息。   
    **注意**：混合云请求字段projectID不支持，返回字段projectID未对齐
    """

    def __init__(self, request_param):
        super(ListInstancesRequest, self).__init__("/v4/ecs/list-instances", "POST", "ctecs", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.state is not None:
            body_param["state"] = self.parameters.state
        if self.parameters.keyword is not None:
            body_param["keyword"] = self.parameters.keyword
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.vip_id is not None:
            body_param["vipID"] = self.parameters.vip_id
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.dec_id is not None:
            body_param["decID"] = self.parameters.dec_id
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


class ListInstancesRequestParam(object):

    def __init__(self, region_id, az_name=None, project_id=None, page_no=None, page_size=None, state=None, keyword=None, instance_id_list=None, instance_name=None, vip_id=None, resource_id=None, security_group_id=None, dec_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param project_id: 项目ID-暂未提供
        :param page_no: 页码
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param state: 云主机状态,取值范围：active（开机），shutoff（关机）注：该参数大小写不敏感（如active可填写为ACTIVE）
        :param keyword: 关键字name、displayName、ID、privateIP对这些字段模糊查询
        :param instance_id_list: ecs实例ID列表，多个ID以逗号分隔
        :param instance_name: 云主机名称
        :param vip_id: 虚拟网络ID
        :param resource_id: 资源ID 
        :param security_group_id: 安全组id
        :param dec_id: 专属云ID
        """
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.page_no = page_no
        self.page_size = page_size
        self.state = state
        self.keyword = keyword
        self.instance_id_list = instance_id_list
        self.instance_name = instance_name
        self.vip_id = vip_id
        self.resource_id = resource_id
        self.security_group_id = security_group_id
        self.dec_id = dec_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 项目ID-暂未提供
        """
        self.project_id = project_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_state(self, state):
        """
        :param state: 云主机状态,取值范围：active（开机），shutoff（关机）注：该参数大小写不敏感（如active可填写为ACTIVE）
        """
        self.state = state

    def set_keyword(self, keyword):
        """
        :param keyword: 关键字name、displayName、ID、privateIP对这些字段模糊查询
        """
        self.keyword = keyword

    def set_instance_id_list(self, instance_id_list):
        """
        :param instance_id_list: ecs实例ID列表，多个ID以逗号分隔
        """
        self.instance_id_list = instance_id_list

    def set_instance_name(self, instance_name):
        """
        :param instance_name: 云主机名称
        """
        self.instance_name = instance_name

    def set_vip_id(self, vip_id):
        """
        :param vip_id: 虚拟网络ID
        """
        self.vip_id = vip_id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源ID 
        """
        self.resource_id = resource_id

    def set_security_group_id(self, security_group_id):
        """
        :param security_group_id: 安全组id
        """
        self.security_group_id = security_group_id

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 专属云ID
        """
        self.dec_id = dec_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

