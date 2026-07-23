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


class SfsResizeSfsRequest(CTYunRequest):
    """
    注意：   
    1. 只能进行扩容操作，容量需要大于现有文件系统容量大小，最大为327680GB
    """

    def __init__(self, request_param):
        super(SfsResizeSfsRequest, self).__init__("/v4/sfs/resize-sfs", "POST", "sfs", "application/json")
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
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
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


class SfsResizeSfsRequestParam(object):

    def __init__(self, sfs_uid, sfs_size, region_id, client_token=None):
        """
        :param sfs_uid: 弹性文件系统唯一ID，兼容ID和UUID
        :param sfs_size: 变配后的大小，单位 GB，容量需要大于现有文件系统容量大小，最大为327680GB
        :param region_id:  资源池 ID
        :param client_token: 客户端存根
        """
        self.sfs_uid = sfs_uid
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
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

