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


class QueryPricesRequest(CTYunRequest):
    """
    通过资源池ID和续订文件系统相关参数、查询文件系统续订订单价格
    """

    def __init__(self, request_param):
        super(QueryPricesRequest, self).__init__("/v4/sfs/upgrade-order/query-prices", "POST", "sfs", "application/json")
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
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
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


class QueryPricesRequestParam(object):

    def __init__(self, region_id, sfs_size, sfs_uid, ):
        """
        :param region_id: 资源池ID
        :param sfs_size: 100-327680GB
        :param sfs_uid: 文件系统ID
        """
        self.region_id = region_id
        self.sfs_size = sfs_size
        self.sfs_uid = sfs_uid

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")

