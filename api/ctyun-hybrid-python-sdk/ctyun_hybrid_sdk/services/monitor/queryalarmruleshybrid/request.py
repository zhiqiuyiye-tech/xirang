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


class QueryAlarmRulesHybridRequest(CTYunRequest):
    """
    根据筛选项查询告警规则列表。   
    因与公有云底层逻辑区别，返回格式与公有云不同。
    """

    def __init__(self, request_param):
        super(QueryAlarmRulesHybridRequest, self).__init__("/v4/monitor/query-alarm-rules", "GET", "monitor", "")
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
        if self.parameters.service is not None:
            query_param["service"] = self.parameters.service
        if self.parameters.alarm_status is not None:
            query_param["alarmStatus"] = self.parameters.alarm_status
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
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


class QueryAlarmRulesHybridRequestParam(object):

    def __init__(self, region_id, service, alarm_status=None, name=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param service: 本参数表示服务。取值范围：vm:云主机；ph:宿主机；bare_metal:裸金属...详见“[告警规则：获取告警服务列表]”接口返回。
        :param alarm_status: 本参数表示告警规则状态。取值范围：0：启用中。1：停用。
        :param name: 规则名称
        :param page_no: 页码，默认为1
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.region_id = region_id
        self.service = service
        self.alarm_status = alarm_status
        self.name = name
        self.page_no = page_no
        self.page_size = page_size

    def set_alarm_status(self, alarm_status):
        """
        :param alarm_status: 本参数表示告警规则状态。取值范围：0：启用中。1：停用。
        """
        self.alarm_status = alarm_status

    def set_name(self, name):
        """
        :param name: 规则名称
        """
        self.name = name

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认为10， 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.service is None:
            raise Exception("service can not None")

