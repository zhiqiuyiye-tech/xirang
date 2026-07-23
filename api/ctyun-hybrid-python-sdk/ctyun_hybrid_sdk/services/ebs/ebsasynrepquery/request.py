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


class EbsAsynRepQueryRequest(CTYunRequest):
    """
    查询异步复制pair对，底层暂不支持
    """

    def __init__(self, request_param):
        super(EbsAsynRepQueryRequest, self).__init__("/v4/async_rep/query", "GET", "ebs", "")
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
        if self.parameters.replication_id is not None:
            query_param["replicationID"] = self.parameters.replication_id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EbsAsynRepQueryRequestParam(object):

    def __init__(self, region_id, replication_id=None, name=None, status=None):
        """
        :param region_id: 资源池ID
        :param replication_id: 异步复制pair对的ID
        :param name: 异步复制pair对的名称
        :param status: 异步复制pair对的状态
        """
        self.region_id = region_id
        self.replication_id = replication_id
        self.name = name
        self.status = status

    def set_replication_id(self, replication_id):
        """
        :param replication_id: 异步复制pair对的ID
        """
        self.replication_id = replication_id

    def set_name(self, name):
        """
        :param name: 异步复制pair对的名称
        """
        self.name = name

    def set_status(self, status):
        """
        :param status: 异步复制pair对的状态
        """
        self.status = status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

