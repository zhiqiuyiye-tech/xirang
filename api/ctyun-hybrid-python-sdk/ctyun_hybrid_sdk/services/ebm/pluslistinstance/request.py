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


class PlusListInstanceRequest(CTYunRequest):
    """
    物理机状态列表   
    status参数取值列表   
       
    序号	status	说明   
    1	CREATING	创建中   
    2	STARTING	启动中   
    3	RUNNING	运行中   
    4	STOPPING	关机中   
    5	STOPPED	已关机   
    6	RESTARTING	重启中   
    7	ERROR	故障中   
    8	REINSTALLING	重装系统中   
    9	MAINTAINING	维护中   
    10	RESETTING_PASSWORD	重置密码中   
    11	DELETE	删除   
    12	ADDACH_VOLUME_IN_RUNNING	运行状态挂载卷中   
    13	DETACH_VOLUME_IN_RUNNING	运行状态卸载卷中   
    14	ADDACH_VOLUME_IN_STOPPED	关机状态挂载卷中   
    15	DETACH_VOLUME_IN_STOPPED	关机状态卸载卷中   
    16	ADDING_NETWORK	添加网卡中   
    17	DELETING_NETWORK	删除网卡中   
    18	TRANSFERING	迁移中   
    19	EXPORT_IMAGE	导出镜像中   
    20	MODIFY_NETWORK	重置网络中   
    21	RESETTING_HOSTNAME	重置hostname中   
    22	UNSUBSCRIBING	包年包月物理机退订中   
    23	UNSUBSCRIBED	包年包月物理机已退订   
    RUNNING 运行中 可进行关机、重启操作、挂载卷、卸载卷、添加网卡、删除网卡   
    STOPPED 已关机 可进行开机、重装、重置密码、删除、挂载卷、卸载卷、添加网卡、删除网卡、重置内网IP   
    ERROR 故障 可进行删除操作   
    
    """

    def __init__(self, request_param):
        super(PlusListInstanceRequest, self).__init__("/v4/ebm/list-instance", "GET", "ebm", "application/json")
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
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        if self.parameters.ip is not None:
            query_param["ip"] = self.parameters.ip
        if self.parameters.instance_name is not None:
            query_param["instanceName"] = self.parameters.instance_name
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.device_type is not None:
            query_param["deviceType"] = self.parameters.device_type
        if self.parameters.device_uuid_list is not None:
            query_param["deviceUUIDList"] = self.parameters.device_uuid_list
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.instance_uuid_list is not None:
            query_param["instanceUUIDList"] = self.parameters.instance_uuid_list
        if self.parameters.instance_uuid is not None:
            query_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.vip_id is not None:
            query_param["vipID"] = self.parameters.vip_id
        if self.parameters.volume_uuid is not None:
            query_param["volumeUUID"] = self.parameters.volume_uuid
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


class PlusListInstanceRequestParam(object):

    def __init__(self, region_id, az_name=None, resource_id=None, ip=None, instance_name=None, vpc_id=None, subnet_id=None, device_type=None, device_uuid_list=None, query_content=None, instance_uuid_list=None, instance_uuid=None, status=None, vip_id=None, volume_uuid=None, page_no=None, page_size=None, project_id=None):
        """
        :param region_id: 区域ID 
        :param az_name: 可用区
        :param resource_id: 资源ID
        :param ip: 弹性ip，公网IP地址
        :param instance_name: 实例名称
        :param vpc_id:  VPC的UUID
        :param subnet_id: 子网UUID
        :param device_type: 套餐类型
        :param device_uuid_list: 设备uuid 用,分隔
        :param query_content: 对instanceName，内网IP，displayName这些字段模糊查询
        :param instance_uuid_list: 多个实例ID用,分隔，同时支持传入resourceID和底层uuid
        :param instance_uuid: 物理机id，同时支持传入resourceID和底层uuid
        :param status: 实例状态, 参考物理机状态列表取值。
        :param vip_id: vip_id
        :param volume_uuid: 云硬盘ID
        :param page_no: 页码，取值范围：正整数（≥1）
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.az_name = az_name
        self.resource_id = resource_id
        self.ip = ip
        self.instance_name = instance_name
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.device_type = device_type
        self.device_uuid_list = device_uuid_list
        self.query_content = query_content
        self.instance_uuid_list = instance_uuid_list
        self.instance_uuid = instance_uuid
        self.status = status
        self.vip_id = vip_id
        self.volume_uuid = volume_uuid
        self.page_no = page_no
        self.page_size = page_size
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源ID
        """
        self.resource_id = resource_id

    def set_ip(self, ip):
        """
        :param ip: 弹性ip，公网IP地址
        """
        self.ip = ip

    def set_instance_name(self, instance_name):
        """
        :param instance_name: 实例名称
        """
        self.instance_name = instance_name

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id:  VPC的UUID
        """
        self.vpc_id = vpc_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网UUID
        """
        self.subnet_id = subnet_id

    def set_device_type(self, device_type):
        """
        :param device_type: 套餐类型
        """
        self.device_type = device_type

    def set_device_uuid_list(self, device_uuid_list):
        """
        :param device_uuid_list: 设备uuid 用,分隔
        """
        self.device_uuid_list = device_uuid_list

    def set_query_content(self, query_content):
        """
        :param query_content: 对instanceName，内网IP，displayName这些字段模糊查询
        """
        self.query_content = query_content

    def set_instance_uuid_list(self, instance_uuid_list):
        """
        :param instance_uuid_list: 多个实例ID用,分隔，同时支持传入resourceID和底层uuid
        """
        self.instance_uuid_list = instance_uuid_list

    def set_instance_uuid(self, instance_uuid):
        """
        :param instance_uuid: 物理机id，同时支持传入resourceID和底层uuid
        """
        self.instance_uuid = instance_uuid

    def set_status(self, status):
        """
        :param status: 实例状态, 参考物理机状态列表取值。
        """
        self.status = status

    def set_vip_id(self, vip_id):
        """
        :param vip_id: vip_id
        """
        self.vip_id = vip_id

    def set_volume_uuid(self, volume_uuid):
        """
        :param volume_uuid: 云硬盘ID
        """
        self.volume_uuid = volume_uuid

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

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

