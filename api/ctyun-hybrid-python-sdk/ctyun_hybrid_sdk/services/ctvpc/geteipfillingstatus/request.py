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


class GetEipFillingStatusRequest(CTYunRequest):
    """
    查询弹性ip是否开启端口备案
    """

    def __init__(self, request_param):
        super(GetEipFillingStatusRequest, self).__init__("/v4/eip/get-filing-status", "GET", "ctvpc", "")
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
        if self.parameters.eip_id is not None:
            query_param["eipID"] = self.parameters.eip_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetEipFillingStatusRequestParam(object):

    def __init__(self, region_id, eip_id, ):
        """
        :param region_id: 
        :param eip_id: 弹性ip的id
        """
        self.region_id = region_id
        self.eip_id = eip_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.eip_id is None:
            raise Exception("eip_id can not None")

