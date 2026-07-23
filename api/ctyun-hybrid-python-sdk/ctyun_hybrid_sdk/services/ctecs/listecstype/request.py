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


class ListEcsTypeRequest(CTYunRequest):
    """
    该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息，并允许用户根据云主机规格的特殊字段进行筛选。用户可以根据此接口的返回值了解自己可使用的云主机规格有哪些。
    """

    def __init__(self, request_param):
        super(ListEcsTypeRequest, self).__init__("/v4/ecs/type-list", "POST", "ctecs", "application/json")
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
        if self.parameters.flavor_type is not None:
            body_param["flavorType"] = self.parameters.flavor_type
        if self.parameters.flavor_name is not None:
            body_param["flavorName"] = self.parameters.flavor_name
        if self.parameters.flavor_cpu is not None:
            body_param["flavorCPU"] = self.parameters.flavor_cpu
        if self.parameters.flavor_ram is not None:
            body_param["flavorRAM"] = self.parameters.flavor_ram
        if self.parameters.flavor_arch is not None:
            body_param["flavorArch"] = self.parameters.flavor_arch
        if self.parameters.flavor_series is not None:
            body_param["flavorSeries"] = self.parameters.flavor_series
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
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


class ListEcsTypeRequestParam(object):

    def __init__(self, region_id, az_name=None, flavor_type=None, flavor_name=None, flavor_cpu=None, flavor_ram=None, flavor_arch=None, flavor_series=None, flavor_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param flavor_type: 规格类型 取值范围：[CPU、CPU_S6、CPU_C6、CPU_M6、CPU_S3、CPU_C3、CPU_M3、CPU_IP3、GPU_N_T4_V、GPU_N_V100、GPU_N_V100_V、GPU_N_P2V_RENMIN、GPU_N_PI7、GPU_N_G7_V、GPU_N_V100、GPU_N_T4_JX]，支持类型会随着功能升级增加
        :param flavor_name: 规格名称 
        :param flavor_cpu: VCPU个数
        :param flavor_ram: 存大小，单位为G
        :param flavor_arch: 指令集架构 -不支持
        :param flavor_series: 规格系列  取值范围：s：通用型，c：计算增强型，m：内存优化型，hs：海光通用型，hc：海光计算增强型，hm：海光内存型，fs：飞腾通用型，fc：飞腾计算增强型，fm：飞腾内存优化型，ks：鲲鹏通用型，kc：鲲鹏计算增强型，km：鲲鹏内存优化型，g：GPU图形加速基础型，p：GPU计算加速型，ip3：超高IO型
        :param flavor_id: 规格ID  
        """
        self.region_id = region_id
        self.az_name = az_name
        self.flavor_type = flavor_type
        self.flavor_name = flavor_name
        self.flavor_cpu = flavor_cpu
        self.flavor_ram = flavor_ram
        self.flavor_arch = flavor_arch
        self.flavor_series = flavor_series
        self.flavor_id = flavor_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_flavor_type(self, flavor_type):
        """
        :param flavor_type: 规格类型 取值范围：[CPU、CPU_S6、CPU_C6、CPU_M6、CPU_S3、CPU_C3、CPU_M3、CPU_IP3、GPU_N_T4_V、GPU_N_V100、GPU_N_V100_V、GPU_N_P2V_RENMIN、GPU_N_PI7、GPU_N_G7_V、GPU_N_V100、GPU_N_T4_JX]，支持类型会随着功能升级增加
        """
        self.flavor_type = flavor_type

    def set_flavor_name(self, flavor_name):
        """
        :param flavor_name: 规格名称 
        """
        self.flavor_name = flavor_name

    def set_flavor_cpu(self, flavor_cpu):
        """
        :param flavor_cpu: VCPU个数
        """
        self.flavor_cpu = flavor_cpu

    def set_flavor_ram(self, flavor_ram):
        """
        :param flavor_ram: 存大小，单位为G
        """
        self.flavor_ram = flavor_ram

    def set_flavor_arch(self, flavor_arch):
        """
        :param flavor_arch: 指令集架构 -不支持
        """
        self.flavor_arch = flavor_arch

    def set_flavor_series(self, flavor_series):
        """
        :param flavor_series: 规格系列  取值范围：s：通用型，c：计算增强型，m：内存优化型，hs：海光通用型，hc：海光计算增强型，hm：海光内存型，fs：飞腾通用型，fc：飞腾计算增强型，fm：飞腾内存优化型，ks：鲲鹏通用型，kc：鲲鹏计算增强型，km：鲲鹏内存优化型，g：GPU图形加速基础型，p：GPU计算加速型，ip3：超高IO型
        """
        self.flavor_series = flavor_series

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: 规格ID  
        """
        self.flavor_id = flavor_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

