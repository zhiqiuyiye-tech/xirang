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


class DeleteHavipRequest(CTYunRequest):
    """
    删除高可用虚IP   
    虚拟ip如果绑定了实例或者弹性ip，该接口会自动进行解绑
    """

    def __init__(self, request_param):
        super(DeleteHavipRequest, self).__init__("/v4/vpc/havip/delete", "POST", "ctvpc", "application/json")
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
        if self.parameters.ha_vip_id is not None:
            body_param["haVipID"] = self.parameters.ha_vip_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class DeleteHavipRequestParam(object):

    def __init__(self, region_id, ha_vip_id, az_name=None, project_id=None, client_token=None):
        """
        :param region_id: 资源池id
        :param ha_vip_id: VIP ID
        :param az_name: 可用区名称（V2.0该参数无意义）
        :param project_id: 企业项目id（非必填）
        :param client_token: 客户端存根,可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.ha_vip_id = ha_vip_id
        self.az_name = az_name
        self.project_id = project_id
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（V2.0该参数无意义）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id（非必填）
        """
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根,可传但是不进行校验（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ha_vip_id is None:
            raise Exception("ha_vip_id can not None")

