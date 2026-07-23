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


class PhInfoIdcHybridRequest(CTYunRequest):
    """
    查询宿主机基本信息：资源池级别(该资源池下所有用户查询结果相同)   
    注：目前返回结果仅支持主结构中的ip、hostName、hostID字段；cpuInfo对象中的cpuLcoreCount、cpuModelName字段；memInfo对象中的memVirtualTotal字段；diskInfo对象中的diskSize；hostInfo对象中的hostID、hostName字段   
       
    返回参数cpuInfo.cpuLcoreCount，v1是包含了预留核数，而v2是扣除了预留核数（之前v1中化学项目客户质疑过云管前端展示和接口返回对不上，原因就是云管前端展示的不带预留，而v2接口因为扣除了预留，所以不存在该问题）
    """

    def __init__(self, request_param):
        super(PhInfoIdcHybridRequest, self).__init__("/v4/ops/cmdb/ph-info-idc", "POST", "monitor", "application/json")
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
        if self.parameters.new_idc_id is not None:
            body_param["newIdcID"] = self.parameters.new_idc_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class PhInfoIdcHybridRequestParam(object):

    def __init__(self, new_idc_id=None, region_id=None, page_no=None, page_size=None):
        """
        :param new_idc_id: 资源池ID
        :param region_id: 资源池ID, regionID和newIdcID必传一个，两个都传regionID为第一选择
        :param page_no: 页码 默认值:1
        :param page_size: 每页显示条数 取值范围:[1~50]，默认值:10 
        """
        self.new_idc_id = new_idc_id
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size

    def set_new_idc_id(self, new_idc_id):
        """
        :param new_idc_id: 资源池ID
        """
        self.new_idc_id = new_idc_id

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID, regionID和newIdcID必传一个，两个都传regionID为第一选择
        """
        self.region_id = region_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码 默认值:1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页显示条数 取值范围:[1~50]，默认值:10 
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        pass

