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


class EcsTypeFamiliesRequest(CTYunRequest):
    """
    该接口提供用户可用规格族列表查询功能，每种规格族代表不同种类的云主机规格，用户可以根据此接口的返回值了解自己可使用的规格族有哪些。    
    规格族说明如下：    
    云主机-二代机：X86云主机,包含通用型s2、内存优化型m2。s2、m2实例规格簇均为cpu共享型，上线时间较早。    
    云主机-三代机：X86云主机,包含通用型S3、计算增强型c3、内存优化型m3。S3实例规格簇为cpu共享型，c3、m3实例规格簇为cpu独享,软硬件升级，性能增强。    
    云主机-六代机：X86云主机,包含通用型s6、通用计算增强c6、内存优化型m6。S6实例规格簇为cpu共享型，c6、m6实例规格簇为cpu独享,性能优良，能承载不同业务需求。    
    云主机-七代机：X86云主机,包含通用型s7、通用计算增强c7、内存优化型m7。通用型S7实例规格簇为cpu共享型，c7、m7实例规格簇为cpu独享,提供更大规格更优性能，能满足更高业务需要。    
    国产化云主机：X86与ARM云主机,包含鲲鹏计算增强型kc1、海光计算增强型hc1、飞腾计算增强型fc1、鲲鹏内存优化型km1、海光内存优化型hm1、飞腾内存优化型fm1，对安全性有较高要求的政府或企业应用。    
    本地盘云主机：X86云主机，包含云主机规格（ip3），提供数据盘为本地盘的云主机。    
    GPU云主机：包含图形加速基础型G5、图形加速基础型G7；计算加速型P2V、计算加速型PI7、计算加速型P8A、计算加速型PS4、计算加速型PI3、计算加速型PI2；图形加速基础型G6、图形加速基础型G7。
    """

    def __init__(self, request_param):
        super(EcsTypeFamiliesRequest, self).__init__("/v4/ecs/type-families", "POST", "ctecs", "application/json")
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


class EcsTypeFamiliesRequestParam(object):

    def __init__(self, region_id, az_name=None):
        """
        :param region_id: 资源池ID
        :param az_name: 您可以调用获取[资源池信息](https://app.apifox.com/link/project/4152543/apis/api-154988743)，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        """
        self.region_id = region_id
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 您可以调用获取[资源池信息](https://app.apifox.com/link/project/4152543/apis/api-154988743)，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

