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


class BatchCheckPortStatusRequest(CTYunRequest):
    """
    网卡状态批量查询接口
    """

    def __init__(self, request_param):
        super(BatchCheckPortStatusRequest, self).__init__("/v4/ports/check-status-batch", "GET", "ctvpc", "")
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
        if self.parameters.port_ids is not None:
            query_param["portIDs"] = self.parameters.port_ids
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class BatchCheckPortStatusRequestParam(object):

    def __init__(self, region_id, port_ids, ):
        """
        :param region_id: 资源池id
        :param port_ids:  多个网卡用 , 拼接起来, port-id,port-id, 最多支持同时检查 10 个网卡
        """
        self.region_id = region_id
        self.port_ids = port_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.port_ids is None:
            raise Exception("port_ids can not None")

