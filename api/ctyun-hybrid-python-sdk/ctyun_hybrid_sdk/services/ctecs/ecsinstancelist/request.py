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


class EcsInstanceListRequest(CTYunRequest):
    """
    该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机的部分信息。混合云请求、返回字段projectID不支持。   
       
    vmState:   
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
    create_failed:创建失败
    """

    def __init__(self, request_param):
        super(EcsInstanceListRequest, self).__init__("/v4/ecs/instance-list", "POST", "ctecs", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.sg_uuid is not None:
            body_param["sgUUID"] = self.parameters.sg_uuid
        if self.parameters.exclude_recycled is not None:
            body_param["excludeRecycled"] = self.parameters.exclude_recycled
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


class EcsInstanceListRequestParam(object):

    def __init__(self, region_id, az_name=None, project_id=None, page_no=None, page_size=None, status=None, keyword=None, instance_id_list=None, name=None, id=None, vpc_id=None, sg_uuid=None, exclude_recycled=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param project_id: 项目ID-暂未提供
        :param page_no: 页码，取值范围：正整数（≥1）
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param status: 云主机状态
        :param keyword: 关键字name、displayName、ID、privateIP对这些字段模糊查询
        :param instance_id_list: ecs实例ID列表，
        :param name: 云主机名称
        :param id: 云主机ID 
        :param vpc_id: 虚拟网络ID(主网卡所在vpc)
        :param sg_uuid: 安全组ID 
        :param exclude_recycled: true-过滤掉回收站数据
        """
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.page_no = page_no
        self.page_size = page_size
        self.status = status
        self.keyword = keyword
        self.instance_id_list = instance_id_list
        self.name = name
        self.id = id
        self.vpc_id = vpc_id
        self.sg_uuid = sg_uuid
        self.exclude_recycled = exclude_recycled

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 项目ID-暂未提供
        """
        self.project_id = project_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：正整数（≥1）
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_status(self, status):
        """
        :param status: 云主机状态
        """
        self.status = status

    def set_keyword(self, keyword):
        """
        :param keyword: 关键字name、displayName、ID、privateIP对这些字段模糊查询
        """
        self.keyword = keyword

    def set_instance_id_list(self, instance_id_list):
        """
        :param instance_id_list: ecs实例ID列表，
        """
        self.instance_id_list = instance_id_list

    def set_name(self, name):
        """
        :param name: 云主机名称
        """
        self.name = name

    def set_id(self, id):
        """
        :param id: 云主机ID 
        """
        self.id = id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 虚拟网络ID(主网卡所在vpc)
        """
        self.vpc_id = vpc_id

    def set_sg_uuid(self, sg_uuid):
        """
        :param sg_uuid: 安全组ID 
        """
        self.sg_uuid = sg_uuid

    def set_exclude_recycled(self, exclude_recycled):
        """
        :param exclude_recycled: true-过滤掉回收站数据
        """
        self.exclude_recycled = exclude_recycled

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

