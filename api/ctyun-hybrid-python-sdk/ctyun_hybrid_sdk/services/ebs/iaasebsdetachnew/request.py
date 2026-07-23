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


class IaasEbsDetachNewRequest(CTYunRequest):
    """
    支持将某一云硬盘从云主机卸载。   
       
    ### 接口约束   
    只有数据盘支持卸载操作，系统盘不支持卸载。
    """

    def __init__(self, request_param):
        super(IaasEbsDetachNewRequest, self).__init__("/v4/ebs/detach-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
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


class IaasEbsDetachNewRequestParam(object):

    def __init__(self, region_id, disk_id, instance_id=None, client_token=None):
        """
        :param region_id: 区域ID
        :param instance_id: 云主机ID(共享盘的时候必传)
        :param disk_id: 磁盘ID
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.disk_id = disk_id
        self.client_token = client_token

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 云主机ID(共享盘的时候必传)
        """
        self.instance_id = instance_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

