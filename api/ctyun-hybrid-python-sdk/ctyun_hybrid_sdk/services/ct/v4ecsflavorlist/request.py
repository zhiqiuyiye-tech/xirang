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


class V4EcsFlavorListRequest(CTYunRequest):
    """
    查询一个或多个云主机规格资源_PAAS
    该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息,并允许用户根据云主机规格的特殊字段进行筛选。
    注意：如果传了flavorID，则azName为必填；如果只传regionID，则可查询所有数据，azName不是必填的。
    """

    def __init__(self, request_param):
        super(V4EcsFlavorListRequest, self).__init__("/v4/ecs/flavor/list", "POST", "ct", "application/json")
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
        if self.parameters.nic_count is not None:
            body_param["nicCount"] = self.parameters.nic_count
        if self.parameters.dec_id is not None:
            body_param["decID"] = self.parameters.dec_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
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


class V4EcsFlavorListRequestParam(object):

    def __init__(self, region_id, az_name=None, flavor_type=None, flavor_name=None, flavor_cpu=None,
                 flavor_ram=None, flavor_arch=None, flavor_series=None, flavor_id=None, nic_count=None,
                 dec_id=None, instance_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 支持多az的资源池，可用区必填（传了flavor_id时为必填）
        :param flavor_type: 规格类型，取值范围：[CPU、CPU_S6、CPU_C6、CPU_M6、CPU_S3、CPU_C3、CPU_M3、CPU_IP3、GPU_N_T4_V、GPU_N_V100、GPU_N_V100_V、GPU_N_P2V_RENMIN、GPU_N_PI7、GPU_N_G7_V、GPU_N_V100、GPU_N_T4_JX]，支持类型会随着功能升级增加
        :param flavor_name: 规格名称
        :param flavor_cpu: VCPU个数
        :param flavor_ram: 内存大小，单位为G
        :param flavor_arch: 指令集架构 (x86/arm/sw_64)
        :param flavor_series: 规格系列，取值范围：s、c、m、hs、hc、hm、fs、fc、fm、ks、kc、km、g、p、ip3、kir3
        :param flavor_id: 规格ID
        :param nic_count: 网卡个数（暂不支持）
        :param dec_id: 计算专属云ID，查询指定专属云下关联的云主机规格
        :param instance_id: 云主机ID，支持过滤支持变配的规格
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
        self.nic_count = nic_count
        self.dec_id = dec_id
        self.instance_id = instance_id

    def set_az_name(self, az_name):
        """
        :param az_name: 支持多az的资源池，可用区必填（传了flavor_id时为必填）
        """
        self.az_name = az_name

    def set_flavor_type(self, flavor_type):
        """
        :param flavor_type: 规格类型
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
        :param flavor_ram: 内存大小，单位为G
        """
        self.flavor_ram = flavor_ram

    def set_flavor_arch(self, flavor_arch):
        """
        :param flavor_arch: 指令集架构 (x86/arm/sw_64)
        """
        self.flavor_arch = flavor_arch

    def set_flavor_series(self, flavor_series):
        """
        :param flavor_series: 规格系列
        """
        self.flavor_series = flavor_series

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: 规格ID（传了该参数时az_name为必填）
        """
        self.flavor_id = flavor_id

    def set_nic_count(self, nic_count):
        """
        :param nic_count: 网卡个数（暂不支持）
        """
        self.nic_count = nic_count

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 计算专属云ID
        """
        self.dec_id = dec_id

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 云主机ID，支持过滤支持变配的规格
        """
        self.instance_id = instance_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        # 按接口文档：传了flavorID时azName必填
        if self.flavor_id is not None and self.az_name is None:
            raise Exception("az_name can not None when flavor_id is set")
