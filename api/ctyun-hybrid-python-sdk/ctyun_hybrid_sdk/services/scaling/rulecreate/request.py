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


class RuleCreateRequest(CTYunRequest):
    """
    创建一条伸缩策略
    """

    def __init__(self, request_param):
        super(RuleCreateRequest, self).__init__("/v4/scaling/rule/create", "POST", "scaling", "application/json")
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
        if self.parameters.operate_unit is not None:
            body_param["operateUnit"] = self.parameters.operate_unit
        if self.parameters.cooldown is not None:
            body_param["cooldown"] = self.parameters.cooldown
        if self.parameters.operate_count is not None:
            body_param["operateCount"] = self.parameters.operate_count
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.execution_time is not None:
            body_param["executionTime"] = self.parameters.execution_time
        if self.parameters.effective_from is not None:
            body_param["effectiveFrom"] = self.parameters.effective_from
        if self.parameters.effective_till is not None:
            body_param["effectiveTill"] = self.parameters.effective_till
        if self.parameters.cycle is not None:
            body_param["cycle"] = self.parameters.cycle
        if self.parameters.day is not None:
            body_param["day"] = self.parameters.day
        if self.parameters.trigger_obj is not None:
            if type(self.parameters.trigger_obj) is dict:
                trigger_obj_dict_value = self.parameters.trigger_obj
            else:
                trigger_obj_dict_value = self.parameters.trigger_obj.get_dic()
            body_param["triggerObj"] = trigger_obj_dict_value
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


class TriggerObj(object):

    def __init__(self, name, metric_name, statistics, comparison_operator, threshold, period, evaluation_count, ):
        """
        :param name: 告警规则名称，长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param metric_name: 监控项，具体可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items
        :param statistics: 聚合方法：avg、max、min、last
        :param comparison_operator: 比较符：eq,gt,ge,lt,le
        :param threshold: 阈值，1-100
        :param period: 监控周期，例：5m、10m
        :param evaluation_count: 连续出现次数，云管支持1-5
        """
        self.name = name
        self.metric_name = metric_name
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.period = period
        self.evaluation_count = evaluation_count
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.name is not None:
            obj_dict["name"] = self.name
        if self.metric_name is not None:
            obj_dict["metricName"] = self.metric_name
        if self.statistics is not None:
            obj_dict["statistics"] = self.statistics
        if self.comparison_operator is not None:
            obj_dict["comparisonOperator"] = self.comparison_operator
        if self.threshold is not None:
            obj_dict["threshold"] = self.threshold
        if self.period is not None:
            obj_dict["period"] = self.period
        if self.evaluation_count is not None:
            obj_dict["evaluationCount"] = self.evaluation_count
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.metric_name is None:
            raise Exception("metric_name can not None")
        if self.statistics is None:
            raise Exception("statistics can not None")
        if self.comparison_operator is None:
            raise Exception("comparison_operator can not None")
        if self.threshold is None:
            raise Exception("threshold can not None")
        if self.period is None:
            raise Exception("period can not None")
        if self.evaluation_count is None:
            raise Exception("evaluation_count can not None")


class RuleCreateRequestParam(object):

    def __init__(self, region_id, operate_unit, operate_count, action, type, group_id, name, cooldown=None, execution_time=None, effective_from=None, effective_till=None, cycle=None, day=None, trigger_obj=None):
        """
        :param region_id: 资源池ID
        :param operate_unit: 操作的单位 个数（1） 百分比（2）;int 16;
        :param cooldown: 冷却时间 告警策略时必填，单位：秒(大于0)
        :param operate_count: 操作数量（大于0）
        :param action: 执行动作 增加（1） 减少（2） 设置为N（3）;int 16;
        :param type: 策略类型 告警（1） 定时（2） 周期（3）;int 16
        :param group_id: 伸缩组ID
        :param name: 规则名称, 长度2～50,
        :param execution_time: 触发时间 type为2、3时必填 TZ格式
        :param effective_from: 周期策略生效开始时间 type=3时必填 TZ格式
        :param effective_till: 周期策略生效截止时间 type=3时必填 TZ格式
        :param cycle: 周期 月（1） 周（2） 天（3），type=3时必填;int16;
        :param day: 周/月的第几天，type=3且cycle为1、2时必填 注意:此参数为数组
        :param trigger_obj: 新建告警规则传规则内容，创建告警规则时，此结构体中的内容必填
        """
        self.region_id = region_id
        self.operate_unit = operate_unit
        self.cooldown = cooldown
        self.operate_count = operate_count
        self.action = action
        self.type = type
        self.group_id = group_id
        self.name = name
        self.execution_time = execution_time
        self.effective_from = effective_from
        self.effective_till = effective_till
        self.cycle = cycle
        self.day = day
        self.trigger_obj = trigger_obj

    def set_cooldown(self, cooldown):
        """
        :param cooldown: 冷却时间 告警策略时必填，单位：秒(大于0)
        """
        self.cooldown = cooldown

    def set_execution_time(self, execution_time):
        """
        :param execution_time: 触发时间 type为2、3时必填 TZ格式
        """
        self.execution_time = execution_time

    def set_effective_from(self, effective_from):
        """
        :param effective_from: 周期策略生效开始时间 type=3时必填 TZ格式
        """
        self.effective_from = effective_from

    def set_effective_till(self, effective_till):
        """
        :param effective_till: 周期策略生效截止时间 type=3时必填 TZ格式
        """
        self.effective_till = effective_till

    def set_cycle(self, cycle):
        """
        :param cycle: 周期 月（1） 周（2） 天（3），type=3时必填;int16;
        """
        self.cycle = cycle

    def set_day(self, day):
        """
        :param day: 周/月的第几天，type=3且cycle为1、2时必填
        """
        self.day = day

    def set_trigger_obj(self, trigger_obj):
        """
        :param trigger_obj: 新建告警规则传规则内容，创建告警规则时，此结构体中的内容必填
        """
        self.trigger_obj = trigger_obj

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.operate_unit is None:
            raise Exception("operate_unit can not None")
        if self.operate_count is None:
            raise Exception("operate_count can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.type is None:
            raise Exception("type can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.name is None:
            raise Exception("name can not None")

