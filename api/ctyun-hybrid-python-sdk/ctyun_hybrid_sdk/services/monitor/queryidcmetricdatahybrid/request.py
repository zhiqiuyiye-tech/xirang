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


class QueryIDCMetricDataHybridRequest(CTYunRequest):
    """
    查询资源池使用率。监控项itemNameList支持：cpu_til（cpu利用率）、disk_util（系统盘利用率）、mem_util（内存利用率）   
    
    """

    def __init__(self, request_param):
        super(QueryIDCMetricDataHybridRequest, self).__init__("/v4/ops/monitor/query-idc-metricdata", "POST", "monitor", "application/json")
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
        if self.parameters.idc is not None:
            body_param["idc"] = self.parameters.idc
        if self.parameters.item_name_list is not None:
            body_param["itemNameList"] = self.parameters.item_name_list
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


class QueryIDCMetricDataHybridRequestParam(object):

    def __init__(self, idc, item_name_list, ):
        """
        :param idc: 资源池
        :param item_name_list: 监控项名称 注意:此参数为数组
        """
        self.idc = idc
        self.item_name_list = item_name_list

    def check_param(self):
        """
        the param required check
        """
        if self.idc is None:
            raise Exception("idc can not None")
        if self.item_name_list is None:
            raise Exception("item_name_list can not None")

