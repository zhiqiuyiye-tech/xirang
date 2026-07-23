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


class ShowHavipRequest(CTYunRequest):
    """
    1.14.27将返回中的instanceInfo字段从对象改为了集合(改动原因：vip下可以绑定多个云主机，符合业务逻辑)，同时新增了networkInfo集合
    """

    def __init__(self, request_param):
        super(ShowHavipRequest, self).__init__("/v4/vpc/havip/show", "GET", "ctvpc", "")
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
        if self.parameters.ha_vip_id is not None:
            query_param["haVipID"] = self.parameters.ha_vip_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowHavipRequestParam(object):

    def __init__(self, region_id, ha_vip_id, ):
        """
        :param region_id: 资源池ID
        :param ha_vip_id: 高可用虚IP的ID
        """
        self.region_id = region_id
        self.ha_vip_id = ha_vip_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ha_vip_id is None:
            raise Exception("ha_vip_id can not None")

