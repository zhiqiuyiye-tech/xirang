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


class QueryAlarmRulesV41Request(CTYunRequest):
    """
    根据筛选项查询告警规则列表。   
    2.2.5版本支持
    """

    def __init__(self, request_param):
        super(QueryAlarmRulesV41Request, self).__init__("/v4.1/monitor/query-alarm-rules", "GET", "monitor", "")
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
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.contact_group_name is not None:
            query_param["contactGroupName"] = self.parameters.contact_group_name
        if self.parameters.instance_name is not None:
            query_param["instanceName"] = self.parameters.instance_name
        if self.parameters.sort_key is not None:
            query_param["sortKey"] = self.parameters.sort_key
        if self.parameters.sort_type is not None:
            query_param["sortType"] = self.parameters.sort_type
        if self.parameters.res_group_id is not None:
            query_param["resGroupID"] = self.parameters.res_group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryAlarmRulesV41RequestParam(object):

    def __init__(self, region_id, service=None, alarm_status=None, status=None, name=None, page_no=None, page_size=None, contact_group_name=None, instance_name=None, sort_key=None, sort_type=None, res_group_id=None):
        """
        :param region_id: 资源池ID
        :param service: 本参数表示服务。取值范围：   
         vm:云主机；   
         ph:宿主机；   
         bare_metal:裸金属；   
         详见“[告警规则：获取告警服务列表]”接口返回。
        :param alarm_status: 本参数表示告警规则是否告警。取值范围：   
         0：未触发告警。   
         1：触发告警。   
         2：无数据。（暂不支持）   
         根据以上范围取值。
        :param status: 本参数表示告警规则状态。取值范围：   
         0：启用。   
         1：停用。   
         根据以上范围取值。
        :param name: 规则名称
        :param page_no: 页码，默认为1
        :param page_size: 页大小，默认值：20
        :param contact_group_name: 告警联系组名（模糊查询）
        :param instance_name: 监控对象名称（模糊查询）
        :param sort_key: 排序字段:   
         createTime-规则创建时间   
         updateTime-规则更新时间   
         statusUpdateTime-规则状态更新时间
        :param sort_type: 排序类型。取值范围：   
         ASC：升序。   
         DESC：降序。   
         根据以上范围取值。
        :param res_group_id: 资源分组id（2.2.6版本支持）
        """
        self.region_id = region_id
        self.service = service
        self.alarm_status = alarm_status
        self.status = status
        self.name = name
        self.page_no = page_no
        self.page_size = page_size
        self.contact_group_name = contact_group_name
        self.instance_name = instance_name
        self.sort_key = sort_key
        self.sort_type = sort_type
        self.res_group_id = res_group_id

    def set_service(self, service):
        """
        :param service: 本参数表示服务。取值范围：   
         vm:云主机；   
         ph:宿主机；   
         bare_metal:裸金属；   
         详见“[告警规则：获取告警服务列表]”接口返回。
        """
        self.service = service

    def set_alarm_status(self, alarm_status):
        """
        :param alarm_status: 本参数表示告警规则是否告警。取值范围：   
         0：未触发告警。   
         1：触发告警。   
         2：无数据。（暂不支持）   
         根据以上范围取值。
        """
        self.alarm_status = alarm_status

    def set_status(self, status):
        """
        :param status: 本参数表示告警规则状态。取值范围：   
         0：启用。   
         1：停用。   
         根据以上范围取值。
        """
        self.status = status

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
        :param page_size: 页大小，默认值：20
        """
        self.page_size = page_size

    def set_contact_group_name(self, contact_group_name):
        """
        :param contact_group_name: 告警联系组名（模糊查询）
        """
        self.contact_group_name = contact_group_name

    def set_instance_name(self, instance_name):
        """
        :param instance_name: 监控对象名称（模糊查询）
        """
        self.instance_name = instance_name

    def set_sort_key(self, sort_key):
        """
        :param sort_key: 排序字段:   
         createTime-规则创建时间   
         updateTime-规则更新时间   
         statusUpdateTime-规则状态更新时间
        """
        self.sort_key = sort_key

    def set_sort_type(self, sort_type):
        """
        :param sort_type: 排序类型。取值范围：   
         ASC：升序。   
         DESC：降序。   
         根据以上范围取值。
        """
        self.sort_type = sort_type

    def set_res_group_id(self, res_group_id):
        """
        :param res_group_id: 资源分组id（2.2.6版本支持）
        """
        self.res_group_id = res_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

