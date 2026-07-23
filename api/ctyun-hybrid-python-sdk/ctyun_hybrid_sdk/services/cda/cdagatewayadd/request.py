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


class CdaGatewayAddRequest(CTYunRequest):
    """
    专线网关创建
    """

    def __init__(self, request_param):
        super(CdaGatewayAddRequest, self).__init__("/v4/cda/gateway/add", "POST", "cda", "application/json")
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
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.account is not None:
            body_param["account"] = self.parameters.account
        if self.parameters.resource_pool is not None:
            body_param["resourcePool"] = self.parameters.resource_pool
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.resource_pool_name is not None:
            body_param["resourcePoolName"] = self.parameters.resource_pool_name
        if self.parameters.is_sw_config is not None:
            body_param["isSwConfig"] = self.parameters.is_sw_config
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.access_point is not None:
            body_param["accessPoint"] = self.parameters.access_point
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


class CdaGatewayAddRequestParam(object):

    def __init__(self, region_id, gateway_name, account, hostname, resource_pool=None, resource_pool_name=None, is_sw_config=None, description=None, access_point=None):
        """
        :param region_id: 资源池id
        :param gateway_name: 专线网关名称（唯一）（长度2-20，只能是字母和数字）
        :param account: 天翼云账号
        :param resource_pool: 此接口中无实际意义
        :param hostname: 交换机hostname（该参数为上层在绑定物理专线时将物理专线的hostname传入）
        :param resource_pool_name: 此接口中无实际意义
        :param is_sw_config: 默认为true，即下发配置给交换机，即在调用创建（删除）专线网关、绑定（解绑）物理专线、vpc的增删改、路由的增删改时，会调用控制器接口给交换机下发配置；如果为false，不会调用控制器接口给交换机下配置。
        :param description: 
        :param access_point: 接入点 AP1/AP2
        """
        self.region_id = region_id
        self.gateway_name = gateway_name
        self.account = account
        self.resource_pool = resource_pool
        self.hostname = hostname
        self.resource_pool_name = resource_pool_name
        self.is_sw_config = is_sw_config
        self.description = description
        self.access_point = access_point

    def set_resource_pool(self, resource_pool):
        """
        :param resource_pool: 此接口中无实际意义
        """
        self.resource_pool = resource_pool

    def set_resource_pool_name(self, resource_pool_name):
        """
        :param resource_pool_name: 此接口中无实际意义
        """
        self.resource_pool_name = resource_pool_name

    def set_is_sw_config(self, is_sw_config):
        """
        :param is_sw_config: 默认为true，即下发配置给交换机，即在调用创建（删除）专线网关、绑定（解绑）物理专线、vpc的增删改、路由的增删改时，会调用控制器接口给交换机下发配置；如果为false，不会调用控制器接口给交换机下配置。
        """
        self.is_sw_config = is_sw_config

    def set_description(self, description):
        """
        :param description: 
        """
        self.description = description

    def set_access_point(self, access_point):
        """
        :param access_point: 接入点 AP1/AP2
        """
        self.access_point = access_point

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")
        if self.account is None:
            raise Exception("account can not None")
        if self.hostname is None:
            raise Exception("hostname can not None")

