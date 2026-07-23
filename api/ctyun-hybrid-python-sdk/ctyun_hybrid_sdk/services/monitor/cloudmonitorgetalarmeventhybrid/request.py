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


class CloudMonitorGetAlarmEventHybridRequest(CTYunRequest):
    """
    （2.2.6版本支持）
    """

    def __init__(self, request_param):
        super(CloudMonitorGetAlarmEventHybridRequest, self).__init__("/v4/alarm/cloudMonitor/get-alarm-event", "GET", "monitor", "")
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
        if self.parameters.confirm_status is not None:
            query_param["confirmStatus"] = self.parameters.confirm_status
        if self.parameters.monitoring_types is not None:
            query_param["monitoringTypes"] = self.parameters.monitoring_types
        if self.parameters.resource_name is not None:
            query_param["resourceName"] = self.parameters.resource_name
        if self.parameters.exact_instance is not None:
            query_param["exactInstance"] = self.parameters.exact_instance
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CloudMonitorGetAlarmEventHybridRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, alarm_id=None, from_value=None, to=None, alarm_level=None, rule_name=None, alarm_obj_id=None, rule_id=None, obj_type=None, history=None, current=None, shield=None, confirm_status=None, monitoring_types=None, resource_name=None, exact_instance=None):
        """
        :param region_id: 资源池ID
        :param page_no: 查询页码，默认1
        :param page_size: 每页记录数目，取值范围:[1~10000]，默认值:10，单页最大记录不超过10000
        :param alarm_id: 告警事件id
        :param from_value: 告警起始时间(毫秒级时间戳)
        :param to: 告警截至时间(毫秒级时间戳)
        :param alarm_level: 告警级别（枚举值含义：2：warning-提示告警，3：average-一般告警，4：high-严重告警，5：disaster-紧急告警）
        :param rule_name: 规则名称 模糊查询 不支持批量模糊查询 由于网关解析问题请避免输入带有“%”
        :param alarm_obj_id: 告警对象uuid
        :param rule_id: 告警规则id
        :param obj_type: 告警对象类型(宿主机:ph/云主机:vm/弹性IP:eip/弹性伸缩组:scaling/裸金属:bare_metal)，不做强制性校验以防底层/未来增加类型，输入有误则查询不到
        :param history: 仅展示历史数据(是：1；否：不传)，进行确认和清除之后的告警事件在此显示
        :param current: 仅展示当前数据(是：1；否：不传)，没进行确认清除操作的告警事件在此显示
        :param shield: 仅展示被屏蔽告警数据(是：1；否：不传)，根据屏蔽规则进行判断
        :param confirm_status: 处理状态id（(0：未处理  1：处理中  2：已处理)）
        :param monitoring_types: 监控类型id（1：时序，2：事件，3：日志）。当前只支持时序
        :param resource_name: 告警对象名称（模糊匹配）
        :param exact_instance: 告警对象名称（精确匹配）
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
        self.confirm_status = confirm_status
        self.monitoring_types = monitoring_types
        self.resource_name = resource_name
        self.exact_instance = exact_instance

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
        :param from_value: 告警起始时间(毫秒级时间戳)
        """
        self.from_value = from_value

    def set_to(self, to):
        """
        :param to: 告警截至时间(毫秒级时间戳)
        """
        self.to = to

    def set_alarm_level(self, alarm_level):
        """
        :param alarm_level: 告警级别（枚举值含义：2：warning-提示告警，3：average-一般告警，4：high-严重告警，5：disaster-紧急告警）
        """
        self.alarm_level = alarm_level

    def set_rule_name(self, rule_name):
        """
        :param rule_name: 规则名称 模糊查询 不支持批量模糊查询 由于网关解析问题请避免输入带有“%”
        """
        self.rule_name = rule_name

    def set_alarm_obj_id(self, alarm_obj_id):
        """
        :param alarm_obj_id: 告警对象uuid
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

    def set_confirm_status(self, confirm_status):
        """
        :param confirm_status: 处理状态id（(0：未处理  1：处理中  2：已处理)）
        """
        self.confirm_status = confirm_status

    def set_monitoring_types(self, monitoring_types):
        """
        :param monitoring_types: 监控类型id（1：时序，2：事件，3：日志）。当前只支持时序
        """
        self.monitoring_types = monitoring_types

    def set_resource_name(self, resource_name):
        """
        :param resource_name: 告警对象名称（模糊匹配）
        """
        self.resource_name = resource_name

    def set_exact_instance(self, exact_instance):
        """
        :param exact_instance: 告警对象名称（精确匹配）
        """
        self.exact_instance = exact_instance

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

