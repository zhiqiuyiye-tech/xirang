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


class RegionCheckDemandRequest(CTYunRequest):
    """
    约束：云主机规格资源池4.0区分az，product=ecs时请给azName字段赋值   
    spec对象中云主机规格参数：flavorID、specName。product=ecs时两者传其中一个即可   
    spec对象中磁盘规格参数: size。product=ebs时必传
    """

    def __init__(self, request_param):
        super(RegionCheckDemandRequest, self).__init__("/v4/region/check-demand", "POST", "common", "application/json")
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
        if self.parameters.demand is not None:
            if type(self.parameters.demand) is dict:
                demand_dict_value = self.parameters.demand
            else:
                demand_dict_value = self.parameters.demand.get_dic()
            body_param["demand"] = demand_dict_value
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


class Demand(object):

    def __init__(self, product, spec, amount=None):
        """
        :param amount: 需求量（可选，不传默认为1）
        :param product: 产品代码, ecs(资源池4.0区分AZ)/ebs(不区分AZ))
        :param spec: 规格信息
        """
        self.amount = amount
        self.product = product
        self.spec = spec
        self.check_param()

    def set_amount(self, amount):
        """
        :param amount: 需求量（可选，不传默认为1）
        """
        self.amount = amount

    def get_dic(self):
        obj_dict = dict()
        if self.amount is not None:
            obj_dict["amount"] = self.amount
        if self.product is not None:
            obj_dict["product"] = self.product
        if self.spec is not None:
            if type(self.spec) is dict:
                obj_dict["spec"] = self.spec
            else:
                obj_dict["spec"] = self.spec.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.product is None:
            raise Exception("product can not None")
        if self.spec is None:
            raise Exception("spec can not None")


class Spec(object):

    def __init__(self, flavor_id=None, spec_name=None, size=None, dec_id=None):
        """
        :param flavor_id: 云主机规格ID
        :param spec_name: 云主机规格名称
        :param size: 磁盘大小(GB) (product为ebs时不能为空)
        :param dec_id: 新增计算侧参数decID(专属云ID)
        """
        self.flavor_id = flavor_id
        self.spec_name = spec_name
        self.size = size
        self.dec_id = dec_id

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: 云主机规格ID
        """
        self.flavor_id = flavor_id

    def set_spec_name(self, spec_name):
        """
        :param spec_name: 云主机规格名称
        """
        self.spec_name = spec_name

    def set_size(self, size):
        """
        :param size: 磁盘大小(GB) (product为ebs时不能为空)
        """
        self.size = size

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 新增计算侧参数decID(专属云ID)
        """
        self.dec_id = dec_id

    def get_dic(self):
        obj_dict = dict()
        if self.flavor_id is not None:
            obj_dict["flavorID"] = self.flavor_id
        if self.spec_name is not None:
            obj_dict["specName"] = self.spec_name
        if self.size is not None:
            obj_dict["size"] = self.size
        if self.dec_id is not None:
            obj_dict["decID"] = self.dec_id
        return obj_dict


class RegionCheckDemandRequestParam(object):

    def __init__(self, region_id, demand, az_name=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称(云主机规格资源池4.0区分az)
        :param demand: 产品规格下的需求量
        """
        self.region_id = region_id
        self.az_name = az_name
        self.demand = demand

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(云主机规格资源池4.0区分az)
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.demand is None:
            raise Exception("demand can not None")

