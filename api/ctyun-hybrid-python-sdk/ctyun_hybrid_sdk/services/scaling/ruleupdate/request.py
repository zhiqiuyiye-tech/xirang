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


class RuleUpdateRequest(CTYunRequest):
    """
    修改一条伸缩策略   
    混合云管2.2.4版本及之前不支持修改告警策略已绑定的告警规则参数，仅支持ruleID更换其他已有规则，或者triggerObj新建其他告警规则，二选一。   
    2.2.4版本支持可修改告警策略已绑定的告警规则
    """

    def __init__(self, request_param):
        super(RuleUpdateRequest, self).__init__("/v4/scaling/rule/update", "POST", "scaling", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.rule_id is not None:
            body_param["ruleID"] = self.parameters.rule_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.action is not None:
            body_param["action"] = self.parameters.action
        if self.parameters.operate_count is not None:
            body_param["operateCount"] = self.parameters.operate_count
        if self.parameters.operate_unit is not None:
            body_param["operateUnit"] = self.parameters.operate_unit
        if self.parameters.cooldown is not None:
            body_param["cooldown"] = self.parameters.cooldown
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
        if self.parameters.trigger_id is not None:
            body_param["triggerID"] = self.parameters.trigger_id
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
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

    def __init__(self, name, statistics, metric_name=None, comparison_operator=None, threshold=None, period=None, evaluation_count=None):
        """
        :param name: 告警规则名称,长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param metric_name: 监控项，可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items	
        :param statistics: 聚合方法：avg、max、min、last	
        :param comparison_operator: 比较符：eq,gt,ge,lt,le	
        :param threshold: 阈值	，1-100
        :param period: 监控周期，例：5m、10m	
        :param evaluation_count: 连续出现次数	，云管支持1-5
        """
        self.name = name
        self.metric_name = metric_name
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.period = period
        self.evaluation_count = evaluation_count
        self.check_param()

    def set_metric_name(self, metric_name):
        """
        :param metric_name: 监控项，可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items	
        """
        self.metric_name = metric_name

    def set_comparison_operator(self, comparison_operator):
        """
        :param comparison_operator: 比较符：eq,gt,ge,lt,le	
        """
        self.comparison_operator = comparison_operator

    def set_threshold(self, threshold):
        """
        :param threshold: 阈值	，1-100
        """
        self.threshold = threshold

    def set_period(self, period):
        """
        :param period: 监控周期，例：5m、10m	
        """
        self.period = period

    def set_evaluation_count(self, evaluation_count):
        """
        :param evaluation_count: 连续出现次数	，云管支持1-5
        """
        self.evaluation_count = evaluation_count

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
        if self.statistics is None:
            raise Exception("statistics can not None")


class RuleUpdateRequestParam(object):

    def __init__(self, rule_id, region_id, name=None, action=None, operate_count=None, operate_unit=None, cooldown=None, execution_time=None, effective_from=None, effective_till=None, cycle=None, day=None, trigger_id=None, group_id=None, trigger_obj=None):
        """
        :param name: 规则名称，长度2～50
        :param rule_id: 伸缩规则ID	
        :param region_id: 资源池ID
        :param action: 执行动作 增加（1） 减少（2） 设置为N（3）;int 16;(0值无效，视为不修改)
        :param operate_count: 操作数量	(大于0，0值无效，视为不修改)
        :param operate_unit: 操作的单位 个数（1） 百分比（2）	;int 16;(0值无效，视为不修改)
        :param cooldown: 冷却时间 告警策略时必填，单位：秒 (0值无效，视为不修改)
        :param execution_time: 触发时间 type为2、3时必填 TZ格式	
        :param effective_from: 周期策略生效开始时间 TZ格式	
        :param effective_till: 周期策略生效截止时间 TZ格式	
        :param cycle: 循环方式，type为3时必填，取值范围1至3（包含边界）1：按月循环，2：按周循环，3：按天循环;int 16;
        :param day: 当cycle为1时必填，且list元素限制为1-31（包含边界）中的整数且不重复；当cycle为2时必填，且list元素限制为1-7（包含边界）中的整数且不重复；当cycle为3时非必填 注意:此参数为数组
        :param trigger_id: 使用现有告警规则传告警规则ID
        :param group_id: 伸缩组ID（底层不需要该参数，公有云必选，故只做接收处理）
        :param trigger_obj: 新建告警规则传规则内容	
        """
        self.name = name
        self.rule_id = rule_id
        self.region_id = region_id
        self.action = action
        self.operate_count = operate_count
        self.operate_unit = operate_unit
        self.cooldown = cooldown
        self.execution_time = execution_time
        self.effective_from = effective_from
        self.effective_till = effective_till
        self.cycle = cycle
        self.day = day
        self.trigger_id = trigger_id
        self.group_id = group_id
        self.trigger_obj = trigger_obj

    def set_name(self, name):
        """
        :param name: 规则名称，长度2～50
        """
        self.name = name

    def set_action(self, action):
        """
        :param action: 执行动作 增加（1） 减少（2） 设置为N（3）;int 16;(0值无效，视为不修改)
        """
        self.action = action

    def set_operate_count(self, operate_count):
        """
        :param operate_count: 操作数量	(大于0，0值无效，视为不修改)
        """
        self.operate_count = operate_count

    def set_operate_unit(self, operate_unit):
        """
        :param operate_unit: 操作的单位 个数（1） 百分比（2）	;int 16;(0值无效，视为不修改)
        """
        self.operate_unit = operate_unit

    def set_cooldown(self, cooldown):
        """
        :param cooldown: 冷却时间 告警策略时必填，单位：秒 (0值无效，视为不修改)
        """
        self.cooldown = cooldown

    def set_execution_time(self, execution_time):
        """
        :param execution_time: 触发时间 type为2、3时必填 TZ格式	
        """
        self.execution_time = execution_time

    def set_effective_from(self, effective_from):
        """
        :param effective_from: 周期策略生效开始时间 TZ格式	
        """
        self.effective_from = effective_from

    def set_effective_till(self, effective_till):
        """
        :param effective_till: 周期策略生效截止时间 TZ格式	
        """
        self.effective_till = effective_till

    def set_cycle(self, cycle):
        """
        :param cycle: 循环方式，type为3时必填，取值范围1至3（包含边界）1：按月循环，2：按周循环，3：按天循环;int 16;
        """
        self.cycle = cycle

    def set_day(self, day):
        """
        :param day: 当cycle为1时必填，且list元素限制为1-31（包含边界）中的整数且不重复；当cycle为2时必填，且list元素限制为1-7（包含边界）中的整数且不重复；当cycle为3时非必填
        """
        self.day = day

    def set_trigger_id(self, trigger_id):
        """
        :param trigger_id: 使用现有告警规则传告警规则ID
        """
        self.trigger_id = trigger_id

    def set_group_id(self, group_id):
        """
        :param group_id: 伸缩组ID（底层不需要该参数，公有云必选，故只做接收处理）
        """
        self.group_id = group_id

    def set_trigger_obj(self, trigger_obj):
        """
        :param trigger_obj: 新建告警规则传规则内容	
        """
        self.trigger_obj = trigger_obj

    def check_param(self):
        """
        the param required check
        """
        if self.rule_id is None:
            raise Exception("rule_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

