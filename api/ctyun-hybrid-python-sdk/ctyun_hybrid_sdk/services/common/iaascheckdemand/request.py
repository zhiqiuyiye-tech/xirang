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


class IaasCheckDemandRequest(CTYunRequest):
    """
    查询用户可用的产品是否可售，支持云主机、云硬盘、弹性公网IP产品的可售查询。   
    如果当前用户所属vdc未开启配额，直接返回满足条件   
       
    ## 接口约束   
       
    渠道用户产品未售罄可售，   
       
    非渠道用户产品未售罄且用户当前配额有余量可售。   
    原有存量接口仍然可用,   
    存量接口：POST /v4/region/check-demand   
       
       
    ## 参数约束   
    productType传ecs时，flavorID和specName有一个必须为必填项，如果都传，以flavorID为准   
       
    productType传ebs时，ebsSize为必填项   
       
    productType传eip时，eipAmount不是必填项，不填默认1
    """

    def __init__(self, request_param):
        super(IaasCheckDemandRequest, self).__init__("/v4/region/check-demand", "GET", "common", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.product_type is not None:
            query_param["productType"] = self.parameters.product_type
        if self.parameters.flavor_id is not None:
            query_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.spec_name is not None:
            query_param["specName"] = self.parameters.spec_name
        if self.parameters.ecs_amount is not None:
            query_param["ecsAmount"] = self.parameters.ecs_amount
        if self.parameters.ebs_size is not None:
            query_param["ebsSize"] = self.parameters.ebs_size
        if self.parameters.eip_amount is not None:
            query_param["eipAmount"] = self.parameters.eip_amount
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.dec_id is not None:
            query_param["decID"] = self.parameters.dec_id
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IaasCheckDemandRequestParam(object):

    def __init__(self, region_id, product_type, flavor_id=None, spec_name=None, ecs_amount=None, ebs_size=None, eip_amount=None, az_name=None, dec_id=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param product_type: 产品类型 可选值：ecs:云主机,eip:IP,ebs:磁盘
        :param flavor_id: productType为ecs时传，云主机规格ID（获取规格列表/v4/common/get-ecs-flavors，取flavorID或specName）
        :param spec_name: productType为ecs时传，主机规格名称（specName和flavorID可二选一，都传以flavorID为准，获取规格列表/v4/common/get-ecs-flavors，取specName）
        :param ecs_amount: productType为ecs时传，云主机需求量（可选，不传默认为1）单位：个数， 范围[0， 2^32-1]
        :param ebs_size: productType为ebs时传，磁盘大小, 单位：GB， 范围 [0 , 2 ^32-1]
        :param eip_amount: productType为eip时传，IP需求量（可选，不传默认为1）单位：个数, 范围 [0, 2 ^32-1]
        :param az_name: 可用区名称，传入可用区的code
        :param dec_id: 新增计算侧参数decID(专属云ID)
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.product_type = product_type
        self.flavor_id = flavor_id
        self.spec_name = spec_name
        self.ecs_amount = ecs_amount
        self.ebs_size = ebs_size
        self.eip_amount = eip_amount
        self.az_name = az_name
        self.dec_id = dec_id
        self.project_id = project_id

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: productType为ecs时传，云主机规格ID（获取规格列表/v4/common/get-ecs-flavors，取flavorID或specName）
        """
        self.flavor_id = flavor_id

    def set_spec_name(self, spec_name):
        """
        :param spec_name: productType为ecs时传，主机规格名称（specName和flavorID可二选一，都传以flavorID为准，获取规格列表/v4/common/get-ecs-flavors，取specName）
        """
        self.spec_name = spec_name

    def set_ecs_amount(self, ecs_amount):
        """
        :param ecs_amount: productType为ecs时传，云主机需求量（可选，不传默认为1）单位：个数， 范围[0， 2^32-1]
        """
        self.ecs_amount = ecs_amount

    def set_ebs_size(self, ebs_size):
        """
        :param ebs_size: productType为ebs时传，磁盘大小, 单位：GB， 范围 [0 , 2 ^32-1]
        """
        self.ebs_size = ebs_size

    def set_eip_amount(self, eip_amount):
        """
        :param eip_amount: productType为eip时传，IP需求量（可选，不传默认为1）单位：个数, 范围 [0, 2 ^32-1]
        """
        self.eip_amount = eip_amount

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，传入可用区的code
        """
        self.az_name = az_name

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 新增计算侧参数decID(专属云ID)
        """
        self.dec_id = dec_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.product_type is None:
            raise Exception("product_type can not None")

