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


class UpdateLbListenerEstablishTimeoutRequest(CTYunRequest):
    """
    设置监听器建立连接超时时间   
    #### 备注   
    * 3.0 无此能力   
    TCP协议的监听器设置连接超时时间，范围10-1800；UDP/IPRAW设置请求超时时间，范围0-300
    """

    def __init__(self, request_param):
        super(UpdateLbListenerEstablishTimeoutRequest, self).__init__("/v4/elb/update-listener-estab-timeout", "POST", "ctelb", "application/json")
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
        if self.parameters.establish_timeout is not None:
            body_param["establishTimeout"] = self.parameters.establish_timeout
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


class UpdateLbListenerEstablishTimeoutRequestParam(object):

    def __init__(self, region_id, listener_id, establish_timeout, ):
        """
        :param region_id: 区域ID
        :param listener_id: 监听器ID
        :param establish_timeout: TCP建立连接超时时间，单位秒，取值范围： 10 - 1800；UDP/IPRAW设置请求超时时间，范围0-300
        """
        self.region_id = region_id
        self.listener_id = listener_id
        self.establish_timeout = establish_timeout

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.listener_id is None:
            raise Exception("listener_id can not None")
        if self.establish_timeout is None:
            raise Exception("establish_timeout can not None")

