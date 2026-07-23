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


class CreateSaleRelationReginsRequest(CTYunRequest):
    """
    销售品批量关联资源池
    """

    def __init__(self, request_param):
        super(CreateSaleRelationReginsRequest, self).__init__("/v1/billing/createSaleRelationRegins", "POST", "billing", "application/json")
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
        if self.parameters.relate_type is not None:
            body_param["relateType"] = self.parameters.relate_type
        if self.parameters.relate_zones is not None:
            relate_zones = []
            if isinstance(self.parameters.relate_zones, list):
                for item in self.parameters.relate_zones:
                    if type(item) is dict:
                        relate_zones.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        relate_zones.append(item_dict_value)
            else:
                relate_zones.append(self.parameters.relate_zones.get_dic())
            body_param["relateZones"] = relate_zones
        if self.parameters.prod_id is not None:
            body_param["prodID"] = self.parameters.prod_id
        if self.parameters.sale_ids is not None:
            body_param["saleIDs"] = self.parameters.sale_ids
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


class RelateZone(object):

    def __init__(self, region_id=None, azs=None):
        """
        :param region_id: 资源池ID
        :param azs: 可用区信息
        """
        self.region_id = region_id
        self.azs = azs

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID
        """
        self.region_id = region_id

    def set_azs(self, azs):
        """
        :param azs: 可用区信息
        """
        self.azs = azs

    def get_dic(self):
        obj_dict = dict()
        if self.region_id is not None:
            obj_dict["regionID"] = self.region_id
        if self.azs is not None:
            azs_array = []
            for item in self.azs:
                if type(item) is dict:
                    azs_array.append(item)
                else:
                    azs_array.append(item.get_dic())
            obj_dict["azs"] = azs_array
        return obj_dict


class Az(object):

    def __init__(self, az_id=None):
        """
        :param az_id: 可用区ID
        """
        self.az_id = az_id

    def set_az_id(self, az_id):
        """
        :param az_id: 可用区ID
        """
        self.az_id = az_id

    def get_dic(self):
        obj_dict = dict()
        if self.az_id is not None:
            obj_dict["azID"] = self.az_id
        return obj_dict


class CreateSaleRelationReginsRequestParam(object):

    def __init__(self, relate_type, prod_id, sale_ids, relate_zones=None):
        """
        :param relate_type: 关联类型，1-默认，2-自定义
        :param relate_zones: 关联区域信息（如果relateType=1，可以不传） 注意:此参数为数组
        :param prod_id: 产品ID
        :param sale_ids: 销售品ID 注意:此参数为数组
        """
        self.relate_type = relate_type
        self.relate_zones = relate_zones
        self.prod_id = prod_id
        self.sale_ids = sale_ids

    def set_relate_zones(self, relate_zones):
        """
        :param relate_zones: 关联区域信息（如果relateType=1，可以不传）
        """
        self.relate_zones = relate_zones

    def check_param(self):
        """
        the param required check
        """
        if self.relate_type is None:
            raise Exception("relate_type can not None")
        if self.prod_id is None:
            raise Exception("prod_id can not None")
        if self.sale_ids is None:
            raise Exception("sale_ids can not None")

