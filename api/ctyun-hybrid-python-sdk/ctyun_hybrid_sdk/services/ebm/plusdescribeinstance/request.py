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


class PlusDescribeInstanceRequest(CTYunRequest):
    """
    通过参数查询单台物理机信息，私有云中返回字段regionID，privateIPv6 私有云不支持返回。
    """

    def __init__(self, request_param):
        super(PlusDescribeInstanceRequest, self).__init__("/v4/ebm/describe-instance", "GET", "ebm", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_uuid is not None:
            query_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class PlusDescribeInstanceRequestParam(object):

    def __init__(self, region_id, instance_uuid, az_name=None):
        """
        :param region_id: 区域ID
        :param instance_uuid: 实例UUID
        :param az_name: 可用区，517文档是必填的，python不需要传（公有云必传，v2兼容可选）
        """
        self.region_id = region_id
        self.instance_uuid = instance_uuid
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区，517文档是必填的，python不需要传（公有云必传，v2兼容可选）
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")

