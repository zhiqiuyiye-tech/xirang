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


class AssociateEipRequest(CTYunRequest):
    """
    调用此接口可将弹性公网IP（Elastic IP Address，简称EIP）与相关云产品上绑定。   
    绑定之前必须确定EIP没有绑定别的实例，并且云主机也不能已经绑定EIP   
    ### 接口约束   
    - EIP 需为可用状态。   
    - EIP 可绑定到同区域的云主机、裸金属和高可用虚拟IP上。   
    
    """

    def __init__(self, request_param):
        super(AssociateEipRequest, self).__init__("/v4/eip/associate", "POST", "ctvpc", "application/json")
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
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.association_id is not None:
            body_param["associationID"] = self.parameters.association_id
        if self.parameters.association_type is not None:
            body_param["associationType"] = self.parameters.association_type
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class AssociateEipRequestParam(object):

    def __init__(self, region_id, eip_id, association_id, association_type, client_token=None, az_name=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一(实际用不到)
        :param eip_id: EIP ID
        :param association_id: 绑定实例ID
        :param association_type: （公有云必传，实际底层不需要）绑定的实例类型：1 ECS 云主机 VM，2 VIP,3 裸金属
        :param az_name: 可用区名称（实际用不到）
        :param project_id: 企业项目 ID，默认为用户所在默认企业项目
        """
        self.region_id = region_id
        self.client_token = client_token
        self.eip_id = eip_id
        self.association_id = association_id
        self.association_type = association_type
        self.az_name = az_name
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一(实际用不到)
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（实际用不到）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为用户所在默认企业项目
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.eip_id is None:
            raise Exception("eip_id can not None")
        if self.association_id is None:
            raise Exception("association_id can not None")
        if self.association_type is None:
            raise Exception("association_type can not None")

