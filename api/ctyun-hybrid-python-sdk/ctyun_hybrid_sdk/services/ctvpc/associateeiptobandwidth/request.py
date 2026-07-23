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


class AssociateEipToBandwidthRequest(CTYunRequest):
    """
    ipv4调用方式：   
    1.通过/v4/eip/list_for_manage或者/v4/eip/list接口查询 eipId   
    2.通过/v4/bandwidth/list查询共享带宽列表获取共享带宽id   
    注意：eip需为按需计费模式的
    """

    def __init__(self, request_param):
        super(AssociateEipToBandwidthRequest, self).__init__("/v4/bandwidth/associate-eip", "POST", "ctvpc", "application/json")
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
        if self.parameters.bandwidth_id is not None:
            body_param["bandwidthID"] = self.parameters.bandwidth_id
        if self.parameters.eip_ids is not None:
            body_param["eipIDs"] = self.parameters.eip_ids
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class AssociateEipToBandwidthRequestParam(object):

    def __init__(self, region_id, bandwidth_id, eip_ids, client_token=None):
        """
        :param region_id: 资源池id
        :param bandwidth_id: 共享带宽id
        :param eip_ids: 绑定Ipv4地址时：传弹性ip id列表 注意:此参数为数组
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符，且不能超过64个字符。（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.bandwidth_id = bandwidth_id
        self.eip_ids = eip_ids
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符，且不能超过64个字符。（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bandwidth_id is None:
            raise Exception("bandwidth_id can not None")
        if self.eip_ids is None:
            raise Exception("eip_ids can not None")

