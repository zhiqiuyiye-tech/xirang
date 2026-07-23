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


class PaasEbsListByResourceRequest(CTYunRequest):
    """
    云硬盘信息列表_PAAS(可通过resourceID查询)
    """

    def __init__(self, request_param):
        super(PaasEbsListByResourceRequest, self).__init__("/v4/paas/ebs/list", "GET", "ct", "")
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
        if self.parameters.paas_resource_type is not None:
            query_param["paasResourceType"] = self.parameters.paas_resource_type
        if self.parameters.is_paas is not None:
            query_param["isPaas"] = self.parameters.is_paas
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class PaasEbsListByResourceRequestParam(object):

    def __init__(self, region_id, paas_resource_type=None, is_paas=None, page_no=None, page_size=None, resource_id=None):
        """
        :param region_id: 资源池ID
        :param paas_resource_type: 查询资源类型；0--只返回paas资源，1--只返回非paas资源，2--返回全部资源，默认为2(与isPaas二选一即可，都存在以isPaas为主)(公有云参数)
        :param is_paas: 是否paas资源：true-是;false-否;不传返回全部(与paasResourceType二选一即可，都存在以isPaas为主)(v1参数)
        :param page_no: 页码，默认1
        :param page_size: 页大小，默认10，最小值为1，最大值为100，超过最大值按100取值
        :param resource_id: 资源ID   
         
        """
        self.region_id = region_id
        self.paas_resource_type = paas_resource_type
        self.is_paas = is_paas
        self.page_no = page_no
        self.page_size = page_size
        self.resource_id = resource_id

    def set_paas_resource_type(self, paas_resource_type):
        """
        :param paas_resource_type: 查询资源类型；0--只返回paas资源，1--只返回非paas资源，2--返回全部资源，默认为2(与isPaas二选一即可，都存在以isPaas为主)(公有云参数)
        """
        self.paas_resource_type = paas_resource_type

    def set_is_paas(self, is_paas):
        """
        :param is_paas: 是否paas资源：true-是;false-否;不传返回全部(与paasResourceType二选一即可，都存在以isPaas为主)(v1参数)
        """
        self.is_paas = is_paas

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认10，最小值为1，最大值为100，超过最大值按100取值
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源ID   
         
        """
        self.resource_id = resource_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

