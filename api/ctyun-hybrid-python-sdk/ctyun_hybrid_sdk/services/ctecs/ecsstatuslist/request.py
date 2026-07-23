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


class EcsStatusListRequest(CTYunRequest):
    """
    获取多台云主机的状态信息   
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
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
    """

    def __init__(self, request_param):
        super(EcsStatusListRequest, self).__init__("/v4/ecs/status-list", "GET", "ctecs", "")
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
        if self.parameters.instance_id_list is not None:
            query_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EcsStatusListRequestParam(object):

    def __init__(self, region_id, instance_id_list=None, page_no=None, page_size=None, project_id=None):
        """
        :param region_id: 资源池id
        :param instance_id_list: 实例ID列表,string类型数组     
        :param page_no: 页数
        :param page_size: 每页数据条数
        :param project_id: 项目ID 不支持 可不传
        """
        self.region_id = region_id
        self.instance_id_list = instance_id_list
        self.page_no = page_no
        self.page_size = page_size
        self.project_id = project_id

    def set_instance_id_list(self, instance_id_list):
        """
        :param instance_id_list: 实例ID列表,string类型数组     
        """
        self.instance_id_list = instance_id_list

    def set_page_no(self, page_no):
        """
        :param page_no: 页数
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页数据条数
        """
        self.page_size = page_size

    def set_project_id(self, project_id):
        """
        :param project_id: 项目ID 不支持 可不传
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

