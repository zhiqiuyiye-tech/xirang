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


class DeleteEipRequest(CTYunRequest):
    """
    调用此接口可删除 EIP。   
       
    ### 接口约束   
    待删除的EIP需未绑定任何云产品实例。   
    涉及订单计费，当前用户只能操作归属自己的EIP资源，不可跨VDC操作
    """

    def __init__(self, request_param):
        super(DeleteEipRequest, self).__init__("/v4/eip/delete", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
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


class DeleteEipRequestParam(object):

    def __init__(self, region_id, client_token=None, resource_id=None, az_name=None, project_id=None, eip_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池 ID
        :param resource_id: 资源ID(即与eipID含义相同),1.14版本前为必传值,1.14版本后若传入eipID则不传（与eipID至少传一项，eipID未传时该参数生效，eipID有值时，该参数失效）
        :param az_name: 可用区名称（实际用不到）
        :param project_id: 企业项目 ID，默认为用户所在的默认企业项目
        :param eip_id: 弹性IP的id,1.14版本起支持,若传入resourceID则不传（与resourceID至少传一项，若该参数有值，则忽略resourceID，该参数生效）
        """
        self.client_token = client_token
        self.region_id = region_id
        self.resource_id = resource_id
        self.az_name = az_name
        self.project_id = project_id
        self.eip_id = eip_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.client_token = client_token

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源ID(即与eipID含义相同),1.14版本前为必传值,1.14版本后若传入eipID则不传（与eipID至少传一项，eipID未传时该参数生效，eipID有值时，该参数失效）
        """
        self.resource_id = resource_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（实际用不到）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为用户所在的默认企业项目
        """
        self.project_id = project_id

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性IP的id,1.14版本起支持,若传入resourceID则不传（与resourceID至少传一项，若该参数有值，则忽略resourceID，该参数生效）
        """
        self.eip_id = eip_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

