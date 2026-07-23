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


class DssClusterAddPoolRequest(CTYunRequest):
    """
    添加存储池到块存储专属集群
    """

    def __init__(self, request_param):
        super(DssClusterAddPoolRequest, self).__init__("/v4/dss/add-pool", "POST", "dss", "application/json")
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
        if self.parameters.dss_id is not None:
            body_param["dssID"] = self.parameters.dss_id
        if self.parameters.pool_id is not None:
            body_param["poolID"] = self.parameters.pool_id
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


class DssClusterAddPoolRequestParam(object):

    def __init__(self, dss_id, pool_id, ):
        """
        :param dss_id: 专属云ID
        :param pool_id: 存储池ID
        """
        self.dss_id = dss_id
        self.pool_id = pool_id

    def check_param(self):
        """
        the param required check
        """
        if self.dss_id is None:
            raise Exception("dss_id can not None")
        if self.pool_id is None:
            raise Exception("pool_id can not None")

