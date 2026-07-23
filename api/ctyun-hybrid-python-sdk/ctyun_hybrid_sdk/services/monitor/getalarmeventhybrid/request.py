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


class GetAlarmEventHybridRequest(CTYunRequest):
    """
    告警事件查询 开发未对齐原因：公有云无此接口，按照upms接口开发   
    （2.2.4版本支持）
    """

    def __init__(self, request_param):
        super(GetAlarmEventHybridRequest, self).__init__("/v4/alarm/get-alarm-event", "GET", "monitor", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.alarm_id is not None:
            query_param["alarmId"] = self.parameters.alarm_id
        if self.parameters.from_value is not None:
            query_param["from"] = self.parameters.from_value
        if self.parameters.to is not None:
            query_param["to"] = self.parameters.to
        if self.parameters.alarm_level is not None:
            query_param["alarmLevel"] = self.parameters.alarm_level
        if self.parameters.rule_name is not None:
            query_param["ruleName"] = self.parameters.rule_name
        if self.parameters.alarm_obj_id is not None:
            query_param["alarmObjId"] = self.parameters.alarm_obj_id
        if self.parameters.rule_id is not None:
            query_param["ruleId"] = self.parameters.rule_id
        if self.parameters.obj_type is not None:
            query_param["objType"] = self.parameters.obj_type
        if self.parameters.history is not None:
            query_param["history"] = self.parameters.history
        if self.parameters.current is not None:
            query_param["current"] = self.parameters.current
        if self.parameters.shield is not None:
            query_param["shield"] = self.parameters.shield
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetAlarmEventHybridRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, alarm_id=None, from_value=None, to=None, alarm_level=None, rule_name=None, alarm_obj_id=None, rule_id=None, obj_type=None, history=None, current=None, shield=None):
        """
        :param region_id: 资源池ID
        :param page_no: 查询页码，默认1
        :param page_size: 每页记录数目，取值范围:[1~10000]，默认值:10，单页最大记录不超过10000
        :param alarm_id: 告警事件id
        :param from_value: 告警起始时间(毫秒级时间戳) from和to必须同时使用
        :param to: 告警截至时间(毫秒级时间戳) from和to必须同时使用
        :param alarm_level: 告警级别
        :param rule_name: 规则名称 模糊查询 不支持批量模糊查询 由于网关解析问题请避免输入带有“%”
        :param alarm_obj_id: 告警对象id
        :param rule_id: 告警规则id
        :param obj_type: 告警对象类型(宿主机:ph/云主机:vm/弹性IP:eip/弹性伸缩组:scaling/裸金属:bare_metal)，不做强制性校验以防底层/未来增加类型，输入有误则查询不到
        :param history: 仅展示历史数据(是：1；否：不传)，进行确认和清除之后的告警事件在此显示
        :param current: 仅展示当前数据(是：1；否：不传)，没进行确认清除操作的告警事件在此显示
        :param shield: 仅展示被屏蔽告警数据(是：1；否：不传)，根据屏蔽规则进行判断
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.alarm_id = alarm_id
        self.from_value = from_value
        self.to = to
        self.alarm_level = alarm_level
        self.rule_name = rule_name
        self.alarm_obj_id = alarm_obj_id
        self.rule_id = rule_id
        self.obj_type = obj_type
        self.history = history
        self.current = current
        self.shield = shield

    def set_page_no(self, page_no):
        """
        :param page_no: 查询页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围:[1~10000]，默认值:10，单页最大记录不超过10000
        """
        self.page_size = page_size

    def set_alarm_id(self, alarm_id):
        """
        :param alarm_id: 告警事件id
        """
        self.alarm_id = alarm_id

    def set_from_value(self, from_value):
        """
        :param from_value: 告警起始时间(毫秒级时间戳) from和to必须同时使用
        """
        self.from_value = from_value

    def set_to(self, to):
        """
        :param to: 告警截至时间(毫秒级时间戳) from和to必须同时使用
        """
        self.to = to

    def set_alarm_level(self, alarm_level):
        """
        :param alarm_level: 告警级别
        """
        self.alarm_level = alarm_level

    def set_rule_name(self, rule_name):
        """
        :param rule_name: 规则名称 模糊查询 不支持批量模糊查询 由于网关解析问题请避免输入带有“%”
        """
        self.rule_name = rule_name

    def set_alarm_obj_id(self, alarm_obj_id):
        """
        :param alarm_obj_id: 告警对象id
        """
        self.alarm_obj_id = alarm_obj_id

    def set_rule_id(self, rule_id):
        """
        :param rule_id: 告警规则id
        """
        self.rule_id = rule_id

    def set_obj_type(self, obj_type):
        """
        :param obj_type: 告警对象类型(宿主机:ph/云主机:vm/弹性IP:eip/弹性伸缩组:scaling/裸金属:bare_metal)，不做强制性校验以防底层/未来增加类型，输入有误则查询不到
        """
        self.obj_type = obj_type

    def set_history(self, history):
        """
        :param history: 仅展示历史数据(是：1；否：不传)，进行确认和清除之后的告警事件在此显示
        """
        self.history = history

    def set_current(self, current):
        """
        :param current: 仅展示当前数据(是：1；否：不传)，没进行确认清除操作的告警事件在此显示
        """
        self.current = current

    def set_shield(self, shield):
        """
        :param shield: 仅展示被屏蔽告警数据(是：1；否：不传)，根据屏蔽规则进行判断
        """
        self.shield = shield

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

