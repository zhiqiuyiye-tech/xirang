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


class QueryAlarmDataHybridRequest(CTYunRequest):
    """
    查询宿主机告警数据   
    注：返回数据中的ip是宿主机名称、云主机名称-->原因：混合云创建告警规则使用name和id创建，查询告警数据需关联规则进行查询，因此ip返回的实际是名称   
    告警数据有权限控制，超管查询全部数据   
    
    """

    def __init__(self, request_param):
        super(QueryAlarmDataHybridRequest, self).__init__("/v4/ops/monitor/query-alarmdata", "POST", "monitor", "application/json")
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
        if self.parameters.obj_type is not None:
            body_param["objType"] = self.parameters.obj_type
        if self.parameters.alarm_start_time is not None:
            body_param["alarmStartTime"] = self.parameters.alarm_start_time
        if self.parameters.alarm_end_time is not None:
            body_param["alarmEndTime"] = self.parameters.alarm_end_time
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


class QueryAlarmDataHybridRequestParam(object):

    def __init__(self, alarm_start_time, alarm_end_time, page_no, page_size, idc=None, obj_type=None):
        """
        :param idc: 资源池
        :param obj_type: 告警资源类型，默认为全部类型: ph（宿主机）;vm（云主机）
        :param alarm_start_time: 告警开始时间戳(精确到秒)
        :param alarm_end_time: 告警结束时间戳(精确到秒)
        :param page_no: 页码，0或不传默认值:1，小于0时报错
        :param page_size: 取值范围 [1, 100]，小于0时报错；0或不传默认是10；超过100默认是100，不报错
        """
        self.idc = idc
        self.obj_type = obj_type
        self.alarm_start_time = alarm_start_time
        self.alarm_end_time = alarm_end_time
        self.page_no = page_no
        self.page_size = page_size

    def set_idc(self, idc):
        """
        :param idc: 资源池
        """
        self.idc = idc

    def set_obj_type(self, obj_type):
        """
        :param obj_type: 告警资源类型，默认为全部类型: ph（宿主机）;vm（云主机）
        """
        self.obj_type = obj_type

    def check_param(self):
        """
        the param required check
        """
        if self.alarm_start_time is None:
            raise Exception("alarm_start_time can not None")
        if self.alarm_end_time is None:
            raise Exception("alarm_end_time can not None")
        if self.page_no is None:
            raise Exception("page_no can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

