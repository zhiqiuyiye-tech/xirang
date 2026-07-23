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


class QueryHpfsClusterByDeviceRequest(CTYunRequest):
    """
    1. 返回字段remainingStatus（该集群是否可以售卖），V2暂不支持，暂时返回默认值false
    """

    def __init__(self, request_param):
        super(QueryHpfsClusterByDeviceRequest, self).__init__("/v4/hpfs/list-cluster-by-device", "GET", "hpfs", "")
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
        if self.parameters.ebm_device_type is not None:
            query_param["ebmDeviceType"] = self.parameters.ebm_device_type
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryHpfsClusterByDeviceRequestParam(object):

    def __init__(self, region_id, ebm_device_type, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param ebm_device_type: 裸金属设备规格
        :param page_no: 列表的分页页码，默认值为1
        :param page_size: 每页包含的元素个数范围(1-100)，默认值为10，大于100取100，不传、传0取10
        """
        self.region_id = region_id
        self.ebm_device_type = ebm_device_type
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的分页页码，默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页包含的元素个数范围(1-100)，默认值为10，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ebm_device_type is None:
            raise Exception("ebm_device_type can not None")

