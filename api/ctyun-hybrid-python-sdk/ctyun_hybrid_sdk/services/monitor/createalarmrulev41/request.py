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


class CreateAlarmRuleV41Request(CTYunRequest):
    """
    创建一个告警规则。
    """

    def __init__(self, request_param):
        super(CreateAlarmRuleV41Request, self).__init__("/v4.1/monitor/create-alarm-rule", "POST", "monitor", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.service is not None:
            body_param["service"] = self.parameters.service
        if self.parameters.dimension is not None:
            body_param["dimension"] = self.parameters.dimension
        if self.parameters.conditions is not None:
            conditions = []
            if isinstance(self.parameters.conditions, list):
                for item in self.parameters.conditions:
                    if type(item) is dict:
                        conditions.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        conditions.append(item_dict_value)
            else:
                conditions.append(self.parameters.conditions.get_dic())
            body_param["conditions"] = conditions
        if self.parameters.desc is not None:
            body_param["desc"] = self.parameters.desc
        if self.parameters.repeat_times is not None:
            body_param["repeatTimes"] = self.parameters.repeat_times
        if self.parameters.silence_time is not None:
            body_param["silenceTime"] = self.parameters.silence_time
        if self.parameters.recover_notify is not None:
            body_param["recoverNotify"] = self.parameters.recover_notify
        if self.parameters.notify_type is not None:
            body_param["notifyType"] = self.parameters.notify_type
        if self.parameters.contact_group_list is not None:
            body_param["contactGroupList"] = self.parameters.contact_group_list
        if self.parameters.notify_weekdays is not None:
            body_param["notifyWeekdays"] = self.parameters.notify_weekdays
        if self.parameters.notify_start is not None:
            body_param["notifyStart"] = self.parameters.notify_start
        if self.parameters.notify_end is not None:
            body_param["notifyEnd"] = self.parameters.notify_end
        if self.parameters.webhook_url is not None:
            body_param["webhookUrl"] = self.parameters.webhook_url
        if self.parameters.res_group_id is not None:
            body_param["resGroupID"] = self.parameters.res_group_id
        if self.parameters.resources is not None:
            resources = []
            if isinstance(self.parameters.resources, list):
                for item in self.parameters.resources:
                    if type(item) is dict:
                        resources.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        resources.append(item_dict_value)
            else:
                resources.append(self.parameters.resources.get_dic())
            body_param["resources"] = resources
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.condition_type is not None:
            body_param["conditionType"] = self.parameters.condition_type
        if self.parameters.resource_scope is not None:
            body_param["resourceScope"] = self.parameters.resource_scope
        if self.parameters.default_contact is not None:
            body_param["defaultContact"] = self.parameters.default_contact
        if self.parameters.notice_strategy_id is not None:
            body_param["noticeStrategyID"] = self.parameters.notice_strategy_id
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


class Condition(object):

    def __init__(self, metric, fun, operator, value, evaluation_count, period, unit=None, level=None):
        """
        :param metric: 可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items
        :param fun: 取值范围： last：原始值算法。 avg：平均值算法。 max：最大值算法。 min：最小值算法。 根据以上范围取值。
        :param operator: 默认值le。取值范围： eq：等于。 gt：大于。 ge：大于等于。 lt：小于。 le：小于等于。 根据以上范围取值。
        :param value: 大于0整数。若指标单位为%，不能大于100
        :param evaluation_count: 当规则执行结果持续多久符合条件时报警（防抖）。（云管支持1-5次）
        :param period: 混合云管支持：1m, 5m, 20m, 1h, 4h, 12h, 24h
        :param unit: 部分资源池不支持，默认为空（混合云openAPI此字段不支持，可以不传）
        :param level: 默认值：3。 取值范围： 1：紧急。 2：警示。 3：普通。 根据以上范围取值。
        """
        self.metric = metric
        self.fun = fun
        self.operator = operator
        self.value = value
        self.evaluation_count = evaluation_count
        self.period = period
        self.unit = unit
        self.level = level
        self.check_param()

    def set_unit(self, unit):
        """
        :param unit: 部分资源池不支持，默认为空（混合云openAPI此字段不支持，可以不传）
        """
        self.unit = unit

    def set_level(self, level):
        """
        :param level: 默认值：3。 取值范围： 1：紧急。 2：警示。 3：普通。 根据以上范围取值。
        """
        self.level = level

    def get_dic(self):
        obj_dict = dict()
        if self.metric is not None:
            obj_dict["metric"] = self.metric
        if self.fun is not None:
            obj_dict["fun"] = self.fun
        if self.operator is not None:
            obj_dict["operator"] = self.operator
        if self.value is not None:
            obj_dict["value"] = self.value
        if self.evaluation_count is not None:
            obj_dict["evaluationCount"] = self.evaluation_count
        if self.period is not None:
            obj_dict["period"] = self.period
        if self.unit is not None:
            obj_dict["unit"] = self.unit
        if self.level is not None:
            obj_dict["level"] = self.level
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.metric is None:
            raise Exception("metric can not None")
        if self.fun is None:
            raise Exception("fun can not None")
        if self.operator is None:
            raise Exception("operator can not None")
        if self.value is None:
            raise Exception("value can not None")
        if self.evaluation_count is None:
            raise Exception("evaluation_count can not None")
        if self.period is None:
            raise Exception("period can not None")


class Resource(object):

    def __init__(self, resource=None):
        """
        :param resource: 资源信息
        """
        self.resource = resource

    def set_resource(self, resource):
        """
        :param resource: 资源信息
        """
        self.resource = resource

    def get_dic(self):
        obj_dict = dict()
        if self.resource is not None:
            resource_array = []
            for item in self.resource:
                if type(item) is dict:
                    resource_array.append(item)
                else:
                    resource_array.append(item.get_dic())
            obj_dict["resource"] = resource_array
        return obj_dict


class CreateAlarmRuleV41RequestParam(object):

    def __init__(self, region_id, name, service, dimension, conditions, desc=None, repeat_times=None, silence_time=None, recover_notify=None, notify_type=None, contact_group_list=None, notify_weekdays=None, notify_start=None, notify_end=None, webhook_url=None, res_group_id=None, resources=None, project_id=None, condition_type=None, resource_scope=None, default_contact=None, notice_strategy_id=None):
        """
        :param region_id: 资源池id
        :param name: 长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param service: 本参数表示服务。取值范围：   
         ecs：云主机；   
         pms：物理机；   
         ph：宿主机；   
         scaling：弹性伸缩；   
         ippool：弹性IP；   
         elb：弹性负载均衡；   
         cda：专线网关（暂不支持）   
         physical_line：物理专线；   
         pushgateway_hpfs：并行文件服务
        :param dimension: 本参数表示告警维度。取值范围：   
         ecs：云主机；   
         pms：物理机；   
         ph：宿主机；   
         scaling：弹性伸缩；   
         ippool：弹性IP；   
         elb：弹性负载均衡；   
         cda_virtual_gateway：专线网关（暂不支持）   
         physical_line：物理专线；   
         pushgateway_hpfs：并行文件服务
        :param conditions:  注意:此参数为数组
        :param desc: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!）
        :param repeat_times: 重复告警通知次数（云管只支持0-3次）
        :param silence_time: 静默时间，多久重复通知一次，单位为秒（混合云支持：300, 600, 900, 1800, 3600, 10800, 21600, 43200, 86400）
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        :param notify_type: 本参数表示告警接收策略。取值范围：   
         email：邮件告警。   
         sms：短信告警。   
         根据以上范围取值。 注意:此参数为数组
        :param contact_group_list: （云管只支持1个） 注意:此参数为数组
        :param notify_weekdays: [0,1,2,3,4,5,6] 0周日... 注意:此参数为数组
        :param notify_start: 通知起始时段，默认为00:00:00
        :param notify_end: 通知结束时段，默认为23:59:59
        :param webhook_url: webhook消息推送url 注意:此参数为数组
        :param res_group_id: 与resources字段互斥。 1.以资源分组为资源对象的告警规则，不需要传入resources。 2.非资源分组为资源对象的告警规则，resources为必填项。
        :param resources: 具体告警匹配资源 注意:此参数为数组
        :param project_id: 暂不支持
        :param condition_type: 默认值0。取值范围： 0：或，任一条件触发。 1：全部条件满足触发。 根据以上范围取值。
        :param resource_scope: 默认值0，取值范围： 0：实例资源类型。 1：资源分组类型。 2：全部资源类型 。 根据以上范围取值。混合云目前不支持全部资源类型，可以不传此参数。
        :param default_contact: 默认值0，取值范围： 0：否。 1：是。 根据以上范围取值。暂不支持
        :param notice_strategy_id: 暂不支持
        """
        self.region_id = region_id
        self.name = name
        self.service = service
        self.dimension = dimension
        self.conditions = conditions
        self.desc = desc
        self.repeat_times = repeat_times
        self.silence_time = silence_time
        self.recover_notify = recover_notify
        self.notify_type = notify_type
        self.contact_group_list = contact_group_list
        self.notify_weekdays = notify_weekdays
        self.notify_start = notify_start
        self.notify_end = notify_end
        self.webhook_url = webhook_url
        self.res_group_id = res_group_id
        self.resources = resources
        self.project_id = project_id
        self.condition_type = condition_type
        self.resource_scope = resource_scope
        self.default_contact = default_contact
        self.notice_strategy_id = notice_strategy_id

    def set_desc(self, desc):
        """
        :param desc: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!）
        """
        self.desc = desc

    def set_repeat_times(self, repeat_times):
        """
        :param repeat_times: 重复告警通知次数（云管只支持0-3次）
        """
        self.repeat_times = repeat_times

    def set_silence_time(self, silence_time):
        """
        :param silence_time: 静默时间，多久重复通知一次，单位为秒（混合云支持：300, 600, 900, 1800, 3600, 10800, 21600, 43200, 86400）
        """
        self.silence_time = silence_time

    def set_recover_notify(self, recover_notify):
        """
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        """
        self.recover_notify = recover_notify

    def set_notify_type(self, notify_type):
        """
        :param notify_type: 本参数表示告警接收策略。取值范围：   
         email：邮件告警。   
         sms：短信告警。   
         根据以上范围取值。
        """
        self.notify_type = notify_type

    def set_contact_group_list(self, contact_group_list):
        """
        :param contact_group_list: （云管只支持1个）
        """
        self.contact_group_list = contact_group_list

    def set_notify_weekdays(self, notify_weekdays):
        """
        :param notify_weekdays: [0,1,2,3,4,5,6] 0周日...
        """
        self.notify_weekdays = notify_weekdays

    def set_notify_start(self, notify_start):
        """
        :param notify_start: 通知起始时段，默认为00:00:00
        """
        self.notify_start = notify_start

    def set_notify_end(self, notify_end):
        """
        :param notify_end: 通知结束时段，默认为23:59:59
        """
        self.notify_end = notify_end

    def set_webhook_url(self, webhook_url):
        """
        :param webhook_url: webhook消息推送url
        """
        self.webhook_url = webhook_url

    def set_res_group_id(self, res_group_id):
        """
        :param res_group_id: 与resources字段互斥。 1.以资源分组为资源对象的告警规则，不需要传入resources。 2.非资源分组为资源对象的告警规则，resources为必填项。
        """
        self.res_group_id = res_group_id

    def set_resources(self, resources):
        """
        :param resources: 具体告警匹配资源
        """
        self.resources = resources

    def set_project_id(self, project_id):
        """
        :param project_id: 暂不支持
        """
        self.project_id = project_id

    def set_condition_type(self, condition_type):
        """
        :param condition_type: 默认值0。取值范围： 0：或，任一条件触发。 1：全部条件满足触发。 根据以上范围取值。
        """
        self.condition_type = condition_type

    def set_resource_scope(self, resource_scope):
        """
        :param resource_scope: 默认值0，取值范围： 0：实例资源类型。 1：资源分组类型。 2：全部资源类型 。 根据以上范围取值。混合云目前不支持全部资源类型，可以不传此参数。
        """
        self.resource_scope = resource_scope

    def set_default_contact(self, default_contact):
        """
        :param default_contact: 默认值0，取值范围： 0：否。 1：是。 根据以上范围取值。暂不支持
        """
        self.default_contact = default_contact

    def set_notice_strategy_id(self, notice_strategy_id):
        """
        :param notice_strategy_id: 暂不支持
        """
        self.notice_strategy_id = notice_strategy_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.service is None:
            raise Exception("service can not None")
        if self.dimension is None:
            raise Exception("dimension can not None")
        if self.conditions is None:
            raise Exception("conditions can not None")

