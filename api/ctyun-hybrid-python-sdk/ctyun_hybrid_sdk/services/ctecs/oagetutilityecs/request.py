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


class OAGetUtilityEcsRequest(CTYunRequest):
    """
    2.2.5版本上线
    """

    def __init__(self, request_param):
        super(OAGetUtilityEcsRequest, self).__init__("/v4/report/utility/ecs", "POST", "ctecs", "application/json")
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
        if self.parameters.creator_id is not None:
            body_param["creatorId"] = self.parameters.creator_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.vdc_id_list is not None:
            body_param["vdcIDList"] = self.parameters.vdc_id_list
        if self.parameters.ecs_id is not None:
            body_param["ecsId"] = self.parameters.ecs_id
        if self.parameters.monitor_start_date is not None:
            body_param["monitorStartDate"] = self.parameters.monitor_start_date
        if self.parameters.monitor_end_date is not None:
            body_param["monitorEndDate"] = self.parameters.monitor_end_date
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.project_name is not None:
            body_param["projectName"] = self.parameters.project_name
        if self.parameters.creator is not None:
            body_param["creator"] = self.parameters.creator
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
        if self.parameters.ipv4 is not None:
            body_param["ipv4"] = self.parameters.ipv4
        if self.parameters.ecs_uuid is not None:
            body_param["ecsUUID"] = self.parameters.ecs_uuid
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.query_content_columns is not None:
            body_param["queryContentColumns"] = self.parameters.query_content_columns
        if self.parameters.time_range_config is not None:
            if type(self.parameters.time_range_config) is dict:
                time_range_config_dict_value = self.parameters.time_range_config
            else:
                time_range_config_dict_value = self.parameters.time_range_config.get_dic()
            body_param["timeRangeConfig"] = time_range_config_dict_value
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


class TimeRangeConfig(object):

    def __init__(self, type, repeat=None):
        """
        :param type: 自定义时段，ALL/CUSTOM
        :param repeat: 
        """
        self.type = type
        self.repeat = repeat
        self.check_param()

    def set_repeat(self, repeat):
        """
        :param repeat: 
        """
        self.repeat = repeat

    def get_dic(self):
        obj_dict = dict()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.repeat is not None:
            if type(self.repeat) is dict:
                obj_dict["repeat"] = self.repeat
            else:
                obj_dict["repeat"] = self.repeat.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class Repeat(object):

    def __init__(self, type, daily_schedule=None, weekly_schedule=None):
        """
        :param type: 重复周期，DAILY/WEEKLY
        :param daily_schedule: 按天重复时间段数组
        :param weekly_schedule: 按周重复时间段数组
        """
        self.type = type
        self.daily_schedule = daily_schedule
        self.weekly_schedule = weekly_schedule
        self.check_param()

    def set_daily_schedule(self, daily_schedule):
        """
        :param daily_schedule: 按天重复时间段数组
        """
        self.daily_schedule = daily_schedule

    def set_weekly_schedule(self, weekly_schedule):
        """
        :param weekly_schedule: 按周重复时间段数组
        """
        self.weekly_schedule = weekly_schedule

    def get_dic(self):
        obj_dict = dict()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.daily_schedule is not None:
            daily_schedule_array = []
            for item in self.daily_schedule:
                if type(item) is dict:
                    daily_schedule_array.append(item)
                else:
                    daily_schedule_array.append(item.get_dic())
            obj_dict["dailySchedule"] = daily_schedule_array
        if self.weekly_schedule is not None:
            if type(self.weekly_schedule) is dict:
                obj_dict["weeklySchedule"] = self.weekly_schedule
            else:
                obj_dict["weeklySchedule"] = self.weekly_schedule.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class DailySchedule(object):

    def __init__(self, start_time, end_time, ):
        """
        :param start_time: 开始时间，小时级别
        :param end_time: 结束时间，小时级别
        """
        self.start_time = start_time
        self.end_time = end_time
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.start_time is not None:
            obj_dict["startTime"] = self.start_time
        if self.end_time is not None:
            obj_dict["endTime"] = self.end_time
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")


class WeeklySchedule(object):

    def __init__(self, workday=None, weekend=None):
        """
        :param workday: 工作日时间段数组
        :param weekend: 周末时间段数组
        """
        self.workday = workday
        self.weekend = weekend

    def set_workday(self, workday):
        """
        :param workday: 工作日时间段数组
        """
        self.workday = workday

    def set_weekend(self, weekend):
        """
        :param weekend: 周末时间段数组
        """
        self.weekend = weekend

    def get_dic(self):
        obj_dict = dict()
        if self.workday is not None:
            workday_array = []
            for item in self.workday:
                if type(item) is dict:
                    workday_array.append(item)
                else:
                    workday_array.append(item.get_dic())
            obj_dict["workday"] = workday_array
        if self.weekend is not None:
            weekend_array = []
            for item in self.weekend:
                if type(item) is dict:
                    weekend_array.append(item)
                else:
                    weekend_array.append(item.get_dic())
            obj_dict["weekend"] = weekend_array
        return obj_dict


class Workday(object):

    def __init__(self, start_time, end_time, ):
        """
        :param start_time: 开始时间，小时级别
        :param end_time: 结束时间，小时级别
        """
        self.start_time = start_time
        self.end_time = end_time
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.start_time is not None:
            obj_dict["startTime"] = self.start_time
        if self.end_time is not None:
            obj_dict["endTime"] = self.end_time
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")


class Weekend(object):

    def __init__(self, start_time, end_time, ):
        """
        :param start_time: 开始时间，小时级别
        :param end_time: 结束时间，小时级别
        """
        self.start_time = start_time
        self.end_time = end_time
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.start_time is not None:
            obj_dict["startTime"] = self.start_time
        if self.end_time is not None:
            obj_dict["endTime"] = self.end_time
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")


class OAGetUtilityEcsRequestParam(object):

    def __init__(self, region_id, monitor_start_date, monitor_end_date, page, page_size, creator_id=None, vdc_id_list=None, ecs_id=None, project_name=None, creator=None, display_name=None, ipv4=None, ecs_uuid=None, query_content=None, query_content_columns=None, time_range_config=None):
        """
        :param creator_id: 创建人编号
        :param region_id: 资源池编号
        :param vdc_id_list: 组织id集合 注意:此参数为数组
        :param ecs_id: 云主机id
        :param monitor_start_date: 监控查询起始日期，yyyy-MM-dd
        :param monitor_end_date: 监控查询截止日期，yyyy-MM-dd
        :param page: 页码
        :param page_size: 每页显示数量
        :param project_name: 企业项目名称，模糊搜索
        :param creator: 创建人名称，模糊搜索
        :param display_name: 云主机展示名称，模糊搜索
        :param ipv4: 内网ipv4，模糊搜索
        :param ecs_uuid: 云主机uuid，模糊搜索
        :param query_content: 组合搜索内容
        :param query_content_columns: 前端支持精确查询的项，需要映射程模糊搜索的数据库字段：projectName,creator,displayName,ipv4,ecsUUID
        :param time_range_config: 时间段选择参数，仅在支持聚合监控指标的环境下该参数才生效
        """
        self.creator_id = creator_id
        self.region_id = region_id
        self.vdc_id_list = vdc_id_list
        self.ecs_id = ecs_id
        self.monitor_start_date = monitor_start_date
        self.monitor_end_date = monitor_end_date
        self.page = page
        self.page_size = page_size
        self.project_name = project_name
        self.creator = creator
        self.display_name = display_name
        self.ipv4 = ipv4
        self.ecs_uuid = ecs_uuid
        self.query_content = query_content
        self.query_content_columns = query_content_columns
        self.time_range_config = time_range_config

    def set_creator_id(self, creator_id):
        """
        :param creator_id: 创建人编号
        """
        self.creator_id = creator_id

    def set_vdc_id_list(self, vdc_id_list):
        """
        :param vdc_id_list: 组织id集合
        """
        self.vdc_id_list = vdc_id_list

    def set_ecs_id(self, ecs_id):
        """
        :param ecs_id: 云主机id
        """
        self.ecs_id = ecs_id

    def set_project_name(self, project_name):
        """
        :param project_name: 企业项目名称，模糊搜索
        """
        self.project_name = project_name

    def set_creator(self, creator):
        """
        :param creator: 创建人名称，模糊搜索
        """
        self.creator = creator

    def set_display_name(self, display_name):
        """
        :param display_name: 云主机展示名称，模糊搜索
        """
        self.display_name = display_name

    def set_ipv4(self, ipv4):
        """
        :param ipv4: 内网ipv4，模糊搜索
        """
        self.ipv4 = ipv4

    def set_ecs_uuid(self, ecs_uuid):
        """
        :param ecs_uuid: 云主机uuid，模糊搜索
        """
        self.ecs_uuid = ecs_uuid

    def set_query_content(self, query_content):
        """
        :param query_content: 组合搜索内容
        """
        self.query_content = query_content

    def set_query_content_columns(self, query_content_columns):
        """
        :param query_content_columns: 前端支持精确查询的项，需要映射程模糊搜索的数据库字段：projectName,creator,displayName,ipv4,ecsUUID
        """
        self.query_content_columns = query_content_columns

    def set_time_range_config(self, time_range_config):
        """
        :param time_range_config: 时间段选择参数，仅在支持聚合监控指标的环境下该参数才生效
        """
        self.time_range_config = time_range_config

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.monitor_start_date is None:
            raise Exception("monitor_start_date can not None")
        if self.monitor_end_date is None:
            raise Exception("monitor_end_date can not None")
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

