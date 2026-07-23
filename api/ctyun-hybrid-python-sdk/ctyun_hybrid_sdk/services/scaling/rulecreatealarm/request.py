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


class RuleCreateAlarmRequest(CTYunRequest):
    """
    创建一个告警策略
    """

    def __init__(self, request_param):
        super(RuleCreateAlarmRequest, self).__init__("/v4/scaling/rule/create-alarm", "POST", "scaling", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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
        :param name: 名称;长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param metric_name: 监控项： ‘cpu_util’: ‘CPU使用率’, ‘disk_read_bytes_rate’: ‘磁盘读速率’, ‘disk_read_requests_rate’: " +                 "‘磁盘读请求速率’, ‘disk_util_inband’: ‘磁盘分配率’, ‘disk_write_bytes_rate’: " +                 "‘磁盘写速率’, ‘disk_write_requests_rate’: ‘磁盘写请求速率’, ‘mem_util’: ‘内存使用率’, " +                 "‘network_incoming_bytes_rate_inband’: ‘网络流入速率’, ‘network_outing_bytes_rate_inband’: ‘网络流出速率’。注：磁盘分配率  指标暂不支持，具体可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items
        :param statistics: 聚合方法‘last’: ‘原始值’, ‘avg’: ‘平均值’, ‘max’: ‘最大值’, ‘min’: ‘最小值’
        :param comparison_operator: 比较符： ‘eq’: ‘=’, ‘gt’: ‘>’, ‘ge’: ‘>=’, ‘lt’: ‘<’, ‘le’: ‘<=’
        :param threshold: 阈值 0-100
        :param period: 监控周期，例：5m、10m
        :param evaluation_count: evaluation_count 连续出现次数，云管支持1-5
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


class RuleCreateAlarmRequestParam(object):

    def __init__(self, region_id, operate_unit, cooldown, operate_count, action, group_id, name, trigger_obj, ):
        """
        :param region_id: 资源池id
        :param operate_unit: 类型：int16;操作的单位：个数（1），百分比（2）
        :param cooldown: 冷却时间，告警策略时必填，单位：秒
        :param operate_count: 执行次数
        :param action: 类型：int16;执行动作：增加（1），减少（2），设置为N（3）
        :param group_id: 伸缩组ID
        :param name: 规则名称;长度2～50
        :param trigger_obj: 新建告警规则传规则内容
        """
        self.region_id = region_id
        self.operate_unit = operate_unit
        self.cooldown = cooldown
        self.operate_count = operate_count
        self.action = action
        self.group_id = group_id
        self.name = name
        self.trigger_obj = trigger_obj

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.operate_unit is None:
            raise Exception("operate_unit can not None")
        if self.cooldown is None:
            raise Exception("cooldown can not None")
        if self.operate_count is None:
            raise Exception("operate_count can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.trigger_obj is None:
            raise Exception("trigger_obj can not None")

