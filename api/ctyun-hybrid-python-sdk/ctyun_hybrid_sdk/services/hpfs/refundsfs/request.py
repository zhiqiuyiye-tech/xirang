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


class RefundSfsRequest(CTYunRequest):
    """
    资源id和并行文件id输入一个即可（必填一个）   
    并行文件系统已绑定VPC时，无法退订；
    """

    def __init__(self, request_param):
        super(RefundSfsRequest, self).__init__("/v4/hpfs/refund-sfs", "POST", "hpfs", "application/json")
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
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
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


class RefundSfsRequestParam(object):

    def __init__(self, region_id, client_token=None, sfs_uid=None, resource_id=None):
        """
        :param client_token: 客户端存根
        :param sfs_uid: sfsUID和resourceID必填一个
        :param region_id: 资源池ID
        :param resource_id: sfsUID和resourceID必填一个
        """
        self.client_token = client_token
        self.sfs_uid = sfs_uid
        self.region_id = region_id
        self.resource_id = resource_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_sfs_uid(self, sfs_uid):
        """
        :param sfs_uid: sfsUID和resourceID必填一个
        """
        self.sfs_uid = sfs_uid

    def set_resource_id(self, resource_id):
        """
        :param resource_id: sfsUID和resourceID必填一个
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

