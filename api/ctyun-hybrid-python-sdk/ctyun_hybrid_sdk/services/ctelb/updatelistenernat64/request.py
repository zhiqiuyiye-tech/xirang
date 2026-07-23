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


class UpdateListenerNat64Request(CTYunRequest):
    """
    设置监听器NAT64   
       
    #### 备注   
    * 3.0 无此能力
    """

    def __init__(self, request_param):
        super(UpdateListenerNat64Request, self).__init__("/v4/elb/update-listener-nat64", "POST", "ctelb", "application/json")
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
        if self.parameters.listener_id is not None:
            body_param["listenerID"] = self.parameters.listener_id
        if self.parameters.enable_nat64 is not None:
            body_param["enableNat64"] = self.parameters.enable_nat64
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


class UpdateListenerNat64RequestParam(object):

    def __init__(self, region_id, listener_id, enable_nat64, ):
        """
        :param region_id: 区域ID
        :param listener_id: 监听器ID
        :param enable_nat64: 是否开启nat64
        """
        self.region_id = region_id
        self.listener_id = listener_id
        self.enable_nat64 = enable_nat64

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.listener_id is None:
            raise Exception("listener_id can not None")
        if self.enable_nat64 is None:
            raise Exception("enable_nat64 can not None")

