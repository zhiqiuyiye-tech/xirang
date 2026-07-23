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


class ModifyBandwidthSpecRequest(CTYunRequest):
    """
    修改共享带宽的数值
    """

    def __init__(self, request_param):
        super(ModifyBandwidthSpecRequest, self).__init__("/v4/bandwidth/modify-spec", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
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


class ModifyBandwidthSpecRequestParam(object):

    def __init__(self, region_id, resource_id, bandwidth, client_token=None):
        """
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符，且不能超过64个字符（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池id
        :param resource_id: 资源id
        :param bandwidth: 带宽大小 (默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准)，如果不传参或者填0，都视为没有数据，为空。请填写有效数据。
        """
        self.client_token = client_token
        self.region_id = region_id
        self.resource_id = resource_id
        self.bandwidth = bandwidth

    def set_client_token(self, client_token):
        """
        :param client_token: 保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符，且不能超过64个字符（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.resource_id is None:
            raise Exception("resource_id can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")

