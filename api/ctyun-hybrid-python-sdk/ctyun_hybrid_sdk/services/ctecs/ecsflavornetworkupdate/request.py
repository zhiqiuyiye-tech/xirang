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


class EcsFlavorNetworkUpdateRequest(CTYunRequest):
    """
    支持对一台已经关机中的云主机进行带宽或规格的变更   
       
    #### 接口约束   
    1. 目标云主机处于关机或节省关机状态，仅支持具有弹性公网IP的云主机进行带宽变更   
    2. 云主机已挂载的云硬盘状态不能处于“镜像制作中”   
    3. 当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用新版本接口，新版本接口更加规范，覆盖场景更全。
    """

    def __init__(self, request_param):
        super(EcsFlavorNetworkUpdateRequest, self).__init__("/v4/ecs/flavor-network-update", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.band_width is not None:
            body_param["bandWidth"] = self.parameters.band_width
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
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


class EcsFlavorNetworkUpdateRequestParam(object):

    def __init__(self, region_id, id, client_token, az_name=None, band_width=None, flavor_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param id: 云主机ID
        :param band_width: 单位为Mbit/s，取值范围:[1~2000]。bandWidth与flavorID不支持同时传入且两者必填其一。
        :param flavor_id: bandWidth与flavorID不支持同时传入且两者必填其一。
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        """
        self.region_id = region_id
        self.az_name = az_name
        self.id = id
        self.band_width = band_width
        self.flavor_id = flavor_id
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_band_width(self, band_width):
        """
        :param band_width: 单位为Mbit/s，取值范围:[1~2000]。bandWidth与flavorID不支持同时传入且两者必填其一。
        """
        self.band_width = band_width

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: bandWidth与flavorID不支持同时传入且两者必填其一。
        """
        self.flavor_id = flavor_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

