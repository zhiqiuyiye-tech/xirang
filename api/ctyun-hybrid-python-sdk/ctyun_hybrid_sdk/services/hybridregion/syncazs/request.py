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


class SyncAzsRequest(CTYunRequest):
    """
    同步可用区信息
    """

    def __init__(self, request_param):
        super(SyncAzsRequest, self).__init__("/v1/regions/azs/sync", "POST", "hybridregion", "application/json")
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
        if self.parameters.region_ids is not None:
            body_param["regionIDs"] = self.parameters.region_ids
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


class SyncAzsRequestParam(object):

    def __init__(self, region_ids, ):
        """
        :param region_ids: 资源池ID集合 注意:此参数为数组
        """
        self.region_ids = region_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_ids is None:
            raise Exception("region_ids can not None")

