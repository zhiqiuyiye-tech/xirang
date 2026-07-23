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


class CreateEipWithIpAddressRequest(CTYunRequest):
    """
    创建指定地址的EIP，EIP的名称不允许重名！
    """

    def __init__(self, request_param):
        super(CreateEipWithIpAddressRequest, self).__init__("/v4/eip/create-with-ipaddress", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.ip_address is not None:
            body_param["ipAddress"] = self.parameters.ip_address
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreateEipWithIpAddressRequestParam(object):

    def __init__(self, region_id, cycle_type, ip_address, client_token=None, name=None, cycle_count=None, az_name=None, bandwidth=None, project_id=None):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池 ID
        :param name: 弹性 IP 名称（2-32长度，只允许中文、英文、数字和特殊字符-, _，只能以中文和英文开头）
        :param cycle_type: 订购类型：month / year / on_demand
        :param cycle_count: 订阅时长，当 cycleType = on_demand 时，可以不传;当 cycleType = month, 支持订购 1 - 11 个月; 当 cycleType = year, 支持订购 1 - 5 年
        :param az_name: 可用区名称（实际没用到）
        :param bandwidth: 弹性 IP 的带宽峰值，默认为 1 Mbps，不传或者传0当默认值处理，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        :param ip_address: 合法的公网 IP
        :param project_id: 企业项目 ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.name = name
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.az_name = az_name
        self.bandwidth = bandwidth
        self.ip_address = ip_address
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 弹性 IP 名称（2-32长度，只允许中文、英文、数字和特殊字符-, _，只能以中文和英文开头）
        """
        self.name = name

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订阅时长，当 cycleType = on_demand 时，可以不传;当 cycleType = month, 支持订购 1 - 11 个月; 当 cycleType = year, 支持订购 1 - 5 年
        """
        self.cycle_count = cycle_count

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（实际没用到）
        """
        self.az_name = az_name

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 弹性 IP 的带宽峰值，默认为 1 Mbps，不传或者传0当默认值处理，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        """
        self.bandwidth = bandwidth

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.ip_address is None:
            raise Exception("ip_address can not None")

