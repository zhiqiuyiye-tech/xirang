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


class SfsResizeRequest(CTYunRequest):
    """
    弹性文件修改规格   
       
    1. 弹性文件只支持扩容，不支持缩容   
    2. 最小需要大于原始大小，最大为327680GB
    """

    def __init__(self, request_param):
        super(SfsResizeRequest, self).__init__("/v4/sfs/resize", "POST", "sfs", "application/json")
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
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
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


class SfsResizeRequestParam(object):

    def __init__(self, resource_id, sfs_size, region_id, client_token=None):
        """
        :param resource_id: 资源 ID
        :param sfs_size: 变配后的大小，单位 GB， 最小需要大于原始大小，最大为327680GB
        :param region_id:  资源池 ID
        :param client_token: 客户端存根
        """
        self.resource_id = resource_id
        self.sfs_size = sfs_size
        self.region_id = region_id
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.resource_id is None:
            raise Exception("resource_id can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

