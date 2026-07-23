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


class SyncSalesRequest(CTYunRequest):
    """
    同步销售品
    """

    def __init__(self, request_param):
        super(SyncSalesRequest, self).__init__("/v1/billing/syncSales", "POST", "billing", "application/json")
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
        if self.parameters.version is not None:
            body_param["version"] = self.parameters.version
        if self.parameters.service_tag is not None:
            body_param["serviceTag"] = self.parameters.service_tag
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.sync_region_infos is not None:
            sync_region_infos = []
            if isinstance(self.parameters.sync_region_infos, list):
                for item in self.parameters.sync_region_infos:
                    if type(item) is dict:
                        sync_region_infos.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        sync_region_infos.append(item_dict_value)
            else:
                sync_region_infos.append(self.parameters.sync_region_infos.get_dic())
            body_param["syncRegionInfos"] = sync_region_infos
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


class SyncRegionInfo(object):

    def __init__(self, region_id, az_ids=None):
        """
        :param region_id: 资源池ID
        :param az_ids: 可用区ID
        """
        self.region_id = region_id
        self.az_ids = az_ids
        self.check_param()

    def set_az_ids(self, az_ids):
        """
        :param az_ids: 可用区ID
        """
        self.az_ids = az_ids

    def get_dic(self):
        obj_dict = dict()
        if self.region_id is not None:
            obj_dict["regionID"] = self.region_id
        if self.az_ids is not None:
            obj_dict["azIDs"] = self.az_ids
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")


class SyncSalesRequestParam(object):

    def __init__(self, version, service_tag, resource_type, sync_region_infos, ):
        """
        :param version: 云管版本 v1/v2
        :param service_tag: 产品的serviceTag
        :param resource_type: 产品的resourceType
        :param sync_region_infos: 资源池信息 注意:此参数为数组
        """
        self.version = version
        self.service_tag = service_tag
        self.resource_type = resource_type
        self.sync_region_infos = sync_region_infos

    def check_param(self):
        """
        the param required check
        """
        if self.version is None:
            raise Exception("version can not None")
        if self.service_tag is None:
            raise Exception("service_tag can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.sync_region_infos is None:
            raise Exception("sync_region_infos can not None")

