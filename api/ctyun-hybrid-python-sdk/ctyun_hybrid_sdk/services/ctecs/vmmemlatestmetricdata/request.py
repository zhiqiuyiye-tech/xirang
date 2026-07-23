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


class VmMemLatestMetricDataRequest(CTYunRequest):
    """
    注：该接口不推荐使用。建议使用-->实时监控数据：云主机(/v4.1/monitor/query-vm-latestmetricdata)
    """

    def __init__(self, request_param):
        super(VmMemLatestMetricDataRequest, self).__init__("/v4/ecs/vm-mem-latest-metric-data", "POST", "ctecs", "application/json")
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
        if self.parameters.device_id_list is not None:
            body_param["deviceIDList"] = self.parameters.device_id_list
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
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


class VmMemLatestMetricDataRequestParam(object):

    def __init__(self, region_id, device_id_list, page=None, page_size=None):
        """
        :param region_id: 资源池id
        :param device_id_list: 云主机ID(建议:设备数不大于20) 注意:此参数为数组
        :param page: 页码，0或不传默认值:1，小于0时报错
        :param page_size: 页大小，取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.region_id = region_id
        self.device_id_list = device_id_list
        self.page = page
        self.page_size = page_size

    def set_page(self, page):
        """
        :param page: 页码，0或不传默认值:1，小于0时报错
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_id_list is None:
            raise Exception("device_id_list can not None")

