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


class SwitchRegionStatusRequest(CTYunRequest):
    """
    切换资源池状态
    """

    def __init__(self, request_param):
        super(SwitchRegionStatusRequest, self).__init__("/v1/regions/switch-status", "PUT", "hybridregion", "application/json")
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
        if self.parameters.regions is not None:
            regions = []
            if isinstance(self.parameters.regions, list):
                for item in self.parameters.regions:
                    if type(item) is dict:
                        regions.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        regions.append(item_dict_value)
            else:
                regions.append(self.parameters.regions.get_dic())
            body_param["regions"] = regions
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


class Region(object):

    def __init__(self, region_id, status, ):
        """
        :param region_id: 资源池ID
        :param status: 1：上线 ；0：下线
        """
        self.region_id = region_id
        self.status = status
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.region_id is not None:
            obj_dict["regionID"] = self.region_id
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.status is None:
            raise Exception("status can not None")


class SwitchRegionStatusRequestParam(object):

    def __init__(self, regions, ):
        """
        :param regions: 支持批量修改，regionID 不存在则跳过 注意:此参数为数组
        """
        self.regions = regions

    def check_param(self):
        """
        the param required check
        """
        if self.regions is None:
            raise Exception("regions can not None")

