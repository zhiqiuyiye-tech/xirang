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


class GetCloudPlatformTopRequest(CTYunRequest):
    """
    多云资源池实例数目Top(云主机和云硬盘)
    """

    def __init__(self, request_param):
        super(GetCloudPlatformTopRequest, self).__init__("/v4/stats/cloudPlatform-top", "GET", "monitor", "")
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
        if self.parameters.all_pools is not None:
            query_param["allPools"] = self.parameters.all_pools
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetCloudPlatformTopRequestParam(object):

    def __init__(self, region_id, all_pools=None):
        """
        :param region_id: 资源池id
        :param all_pools: 是否查询所有资源池，取值：true或1，false或0，多云查询时取true或1
        """
        self.region_id = region_id
        self.all_pools = all_pools

    def set_all_pools(self, all_pools):
        """
        :param all_pools: 是否查询所有资源池，取值：true或1，false或0，多云查询时取true或1
        """
        self.all_pools = all_pools

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

