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


class CreateAlarmRuleHybridRequest(CTYunRequest):
    """
    创建一个告警规则。
    """

    def __init__(self, request_param):
        super(CreateAlarmRuleHybridRequest, self).__init__("/v4/monitor/create-alarm-rule", "POST", "monitor", "application/json")
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
        if self.parameters.desc is not None:
            body_param["desc"] = self.parameters.desc
        if self.parameters.level is not None:
            body_param["level"] = self.parameters.level
        if self.parameters.alarm_object_list is not None:
            alarm_object_list = []
            if isinstance(self.parameters.alarm_object_list, list):
                for item in self.parameters.alarm_object_list:
                    if type(item) is dict:
                        alarm_object_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        alarm_object_list.append(item_dict_value)
            else:
                alarm_object_list.append(self.parameters.alarm_object_list.get_dic())
            body_param["alarmObjectList"] = alarm_object_list
        if self.parameters.notify_start is not None:
            body_param["notifyStart"] = self.parameters.notify_start
        if self.parameters.notify_end is not None:
            body_param["notifyEnd"] = self.parameters.notify_end
        if self.parameters.notify_weekdays is not None:
            body_param["notifyWeekdays"] = self.parameters.notify_weekdays
        if self.parameters.recover_notify is not None:
            body_param["recoverNotify"] = self.parameters.recover_notify
        if self.parameters.repeat_times is not None:
            body_param["repeatTimes"] = self.parameters.repeat_times
        if self.parameters.silence_time is not None:
            body_param["silenceTime"] = self.parameters.silence_time
        if self.parameters.rules is not None:
            rules = []
            if isinstance(self.parameters.rules, list):
                for item in self.parameters.rules:
                    if type(item) is dict:
                        rules.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        rules.append(item_dict_value)
            else:
                rules.append(self.parameters.rules.get_dic())
            body_param["rules"] = rules
        if self.parameters.service is not None:
            body_param["service"] = self.parameters.service
        if self.parameters.contact_group_list is not None:
            body_param["contactGroupList"] = self.parameters.contact_group_list
        if self.parameters.notify_type is not None:
            body_param["notifyType"] = self.parameters.notify_type
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


class AlarmObject(object):

    def __init__(self, id, dimension=None):
        """
        :param id: 云管ID 非UUID
        :param dimension: 创建子对象告警必传
        """
        self.id = id
        self.dimension = dimension
        self.check_param()

    def set_dimension(self, dimension):
        """
        :param dimension: 创建子对象告警必传
        """
        self.dimension = dimension

    def get_dic(self):
        obj_dict = dict()
        if self.id is not None:
            obj_dict["id"] = self.id
        if self.dimension is not None:
            if type(self.dimension) is dict:
                obj_dict["dimension"] = self.dimension
            else:
                obj_dict["dimension"] = self.dimension.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")


class Dimension(object):

    def __init__(self, code, sub_devices, ):
        """
        :param code: 挂载点:fs_dir  GPU卡:gpuno
        :param sub_devices: 子对象标签列表
        """
        self.code = code
        self.sub_devices = sub_devices
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.code is not None:
            obj_dict["code"] = self.code
        if self.sub_devices is not None:
            obj_dict["subDevices"] = self.sub_devices
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.code is None:
            raise Exception("code can not None")
        if self.sub_devices is None:
            raise Exception("sub_devices can not None")


class Rule(object):

    def __init__(self, metric, fun, operator, value, evaluation_count, period, ):
        """
        :param metric: 可通过查询监控项列表接口，查询监控指标/v4/monitor/query-monitor-items
        :param fun: 取值范围： last：原始值算法。 avg：平均值算法。 max：最大值算法。 min：最小值算法。 根据以上范围取值。
        :param operator: 默认值le。取值范围： eq：等于。 gt：大于。 ge：大于等于。 lt：小于。 le：小于等于。 根据以上范围取值。
        :param value: 大于0整数。若指标单位为%，不能大于100
        :param evaluation_count: 当规则执行结果持续多久符合条件时报警（防抖）。（云管支持1-5次）
        :param period: 混合云管支持：1m, 5m, 20m, 1h, 4h, 12h, 24h
        """
        self.metric = metric
        self.fun = fun
        self.operator = operator
        self.value = value
        self.evaluation_count = evaluation_count
        self.period = period
        self.check_param()

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


class CreateAlarmRuleHybridRequestParam(object):

    def __init__(self, region_id, name, level, alarm_object_list, rules, service, contact_group_list, notify_type, desc=None, notify_start=None, notify_end=None, notify_weekdays=None, recover_notify=None, repeat_times=None, silence_time=None):
        """
        :param region_id: 资源池id
        :param name: 长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param desc: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!）
        :param level: 取值1-4：1-灾难，2-严重，3-一般，4-提示
        :param alarm_object_list: 告警资源id和名称数组 注意:此参数为数组
        :param notify_start: 通知起始时段，默认为00:00:00
        :param notify_end: 通知结束时段，默认为23:59:59
        :param notify_weekdays: [0,1,2,3,4,5,6] 0周日... 注意:此参数为数组
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        :param repeat_times: 重复告警通知次数（云管只支持0-3次）
        :param silence_time: 静默时间，多久重复通知一次，单位为秒（混合云支持：300, 600, 900, 1800, 3600, 10800, 21600, 43200, 86400）
        :param rules:  注意:此参数为数组
        :param service: 本参数表示服务。vm:云主机；bare_metal:裸金属；eip:弹性IP；详见“[告警规则：获取告警服务列表]”接口返回。
        :param contact_group_list: （云管只支持1个） 注意:此参数为数组
        :param notify_type: 取值范围：internal:站内信通知。sms：短信通知。email：邮件通知。internal、email根据云管要求必填 注意:此参数为数组
        """
        self.region_id = region_id
        self.name = name
        self.desc = desc
        self.level = level
        self.alarm_object_list = alarm_object_list
        self.notify_start = notify_start
        self.notify_end = notify_end
        self.notify_weekdays = notify_weekdays
        self.recover_notify = recover_notify
        self.repeat_times = repeat_times
        self.silence_time = silence_time
        self.rules = rules
        self.service = service
        self.contact_group_list = contact_group_list
        self.notify_type = notify_type

    def set_desc(self, desc):
        """
        :param desc: 长度为0-128个字符，中文、英文（大小写）、数字、特殊字符（@*()-_.。，、：:” “；?!）
        """
        self.desc = desc

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

    def set_notify_weekdays(self, notify_weekdays):
        """
        :param notify_weekdays: [0,1,2,3,4,5,6] 0周日...
        """
        self.notify_weekdays = notify_weekdays

    def set_recover_notify(self, recover_notify):
        """
        :param recover_notify: 本参数表示恢复是否通知。默认值0。取值范围：0：否。1：是。根据以上范围取值
        """
        self.recover_notify = recover_notify

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

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.level is None:
            raise Exception("level can not None")
        if self.alarm_object_list is None:
            raise Exception("alarm_object_list can not None")
        if self.rules is None:
            raise Exception("rules can not None")
        if self.service is None:
            raise Exception("service can not None")
        if self.contact_group_list is None:
            raise Exception("contact_group_list can not None")
        if self.notify_type is None:
            raise Exception("notify_type can not None")

