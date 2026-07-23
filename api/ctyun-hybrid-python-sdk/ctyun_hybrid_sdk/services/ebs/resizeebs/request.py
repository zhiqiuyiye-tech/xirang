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


class ResizeEbsRequest(CTYunRequest):
    """
    支持云硬盘变配。目前只支持增加磁盘容量。   
    支持云主机订购的系统盘及数据盘扩容。
    """

    def __init__(self, request_param):
        super(ResizeEbsRequest, self).__init__("/v4/ebs/resize-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
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


class ResizeEbsRequestParam(object):

    def __init__(self, disk_size, client_token=None, region_id=None, disk_id=None, resource_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云已支持
        :param region_id: 资源池id,如本地语境支持保存regionID，那么建议传递。
        :param disk_id: 参数resourceID或diskID二者必传其一
        :param disk_size: 变配后的磁盘大小。当前仅支持变更磁盘大小,单位为GB(数据盘范围10G-32768G, 系统盘范围10G-2048G)
        :param resource_id: 参数resourceID或diskID二者必传其一
        """
        self.client_token = client_token
        self.region_id = region_id
        self.disk_id = disk_id
        self.disk_size = disk_size
        self.resource_id = resource_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云已支持
        """
        self.client_token = client_token

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池id,如本地语境支持保存regionID，那么建议传递。
        """
        self.region_id = region_id

    def set_disk_id(self, disk_id):
        """
        :param disk_id: 参数resourceID或diskID二者必传其一
        """
        self.disk_id = disk_id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 参数resourceID或diskID二者必传其一
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.disk_size is None:
            raise Exception("disk_size can not None")

