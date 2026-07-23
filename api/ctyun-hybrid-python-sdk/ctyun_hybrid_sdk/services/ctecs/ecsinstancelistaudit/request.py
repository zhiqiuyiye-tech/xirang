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


class EcsInstanceListAuditRequest(CTYunRequest):
    """
    该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机的部分信息。混合云请求、返回字段projectID不支持。   
       
    status:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backuping: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshoting: 快照创建中
    """

    def __init__(self, request_param):
        super(EcsInstanceListAuditRequest, self).__init__("/v4/ecs/instance-list-audit", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.status is not None:
            body_param["status"] = self.parameters.status
        if self.parameters.keyword is not None:
            body_param["keyword"] = self.parameters.keyword
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
        if self.parameters.start is not None:
            body_param["start"] = self.parameters.start
        if self.parameters.end is not None:
            body_param["end"] = self.parameters.end
        if self.parameters.all is not None:
            body_param["all"] = self.parameters.all
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


class EcsInstanceListAuditRequestParam(object):

    def __init__(self, region_id, az_name=None, page_no=None, page_size=None, status=None, keyword=None, instance_id_list=None, display_name=None, start=None, end=None, all=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param page_no: 页码，取值范围：（≥0）
        :param page_size: 每页记录数目，取值范围：[0, 50]，大于50按50算
        :param status: 云主机状态
        :param keyword: 关键字name、displayName、uuid、privateIP对这些字段模糊查询
        :param instance_id_list: ecs实例UUID列表，
        :param display_name: 名称
        :param start: 创建时间筛选开始时间，与结束时间两者必需时有效，例如2025-09-01T00:00:00Z
        :param end: 创建时间筛选结束时间,与开始时间两者必需时有效，例如2025-09-11T00:00:00Z
        :param all: 查询全部不分页
        """
        self.region_id = region_id
        self.az_name = az_name
        self.page_no = page_no
        self.page_size = page_size
        self.status = status
        self.keyword = keyword
        self.instance_id_list = instance_id_list
        self.display_name = display_name
        self.start = start
        self.end = end
        self.all = all

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：（≥0）
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[0, 50]，大于50按50算
        """
        self.page_size = page_size

    def set_status(self, status):
        """
        :param status: 云主机状态
        """
        self.status = status

    def set_keyword(self, keyword):
        """
        :param keyword: 关键字name、displayName、uuid、privateIP对这些字段模糊查询
        """
        self.keyword = keyword

    def set_instance_id_list(self, instance_id_list):
        """
        :param instance_id_list: ecs实例UUID列表，
        """
        self.instance_id_list = instance_id_list

    def set_display_name(self, display_name):
        """
        :param display_name: 名称
        """
        self.display_name = display_name

    def set_start(self, start):
        """
        :param start: 创建时间筛选开始时间，与结束时间两者必需时有效，例如2025-09-01T00:00:00Z
        """
        self.start = start

    def set_end(self, end):
        """
        :param end: 创建时间筛选结束时间,与开始时间两者必需时有效，例如2025-09-11T00:00:00Z
        """
        self.end = end

    def set_all(self, all):
        """
        :param all: 查询全部不分页
        """
        self.all = all

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

