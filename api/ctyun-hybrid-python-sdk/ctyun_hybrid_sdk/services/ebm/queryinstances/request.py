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


class QueryInstancesRequest(CTYunRequest):
    """
    查询物理机列表接口
    """

    def __init__(self, request_param):
        super(QueryInstancesRequest, self).__init__("/v4/ebm/list", "GET", "ebm", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
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
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        if self.parameters.ip_type is not None:
            query_param["ipType"] = self.parameters.ip_type
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


class QueryInstancesRequestParam(object):

    def __init__(self, region_id, az_name=None, resource_id=None, ip=None, name=None, vpc_id=None, subnet_id=None, device_type=None, device_uuid_list=None, query_content=None, instance_uuid_list=None, id=None, ip_type=None, status=None, vip_id=None, volume_uuid=None, page_no=None, page_size=None, project_id=None):
        """
        :param region_id: 区域ID 
        :param az_name: 可用区
        :param resource_id: 资源ID
        :param ip: 弹性ip，公网IP地址
        :param name: 实例名称
        :param vpc_id:  网络ID
        :param subnet_id: 子网ID
        :param device_type: 套餐类型
        :param device_uuid_list: 设备uuid 用,分隔
        :param query_content: 对instanceName，内网IP，displayName这些字段模糊查询
        :param instance_uuid_list: 多个实例ID用,分隔，同时支持传入resourceID和底层uuid
        :param id: 物理机id，同时支持传入resourceID和底层uuid
        :param ip_type: 弹性IP版本：取值范围:[ipv4=v4地址,ipv6=v6地址]，默认值:ipv4 (暂不支持该参数)
        :param status: 实例状态：   
         "RUNNING", #运行中   
         "STOPPED", #关机   
         "SHUTOFF",#关机   
         "STOPPING", #关机中   
         "STARTING", #开机中   
         "ERROR", #异常   
         "CREATING", #创建中   
         "REINSTALLING", #重装   
         "HOSTNAME_RESETTING", #宿主机名称重置中   
         "MODIFY_NETWORK", # 裸金属重置网络中   
         "RESTARTING", #重启   
         'CREATING_IMAGE', #创建镜像   
         'EXPORT_IMAGE', #裸金属创建镜像中   
         'DELETING', #退订中   
         'RESTORING', #恢复中   
         'DELETING_NETWORK', # 裸金属删除网卡中   
         'ADDING_NETWORK', # 裸金属添加网卡中   
         'ACTIVE',#运行中 同RUNNING   
         'EXPIRED', #已到期   
         'FREEZING', #冻结中
        :param vip_id: 虚ipID
        :param volume_uuid: 云硬盘ID
        :param page_no: 页码
        :param page_size: 页数
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.az_name = az_name
        self.resource_id = resource_id
        self.ip = ip
        self.name = name
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.device_type = device_type
        self.device_uuid_list = device_uuid_list
        self.query_content = query_content
        self.instance_uuid_list = instance_uuid_list
        self.id = id
        self.ip_type = ip_type
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

    def set_name(self, name):
        """
        :param name: 实例名称
        """
        self.name = name

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id:  网络ID
        """
        self.vpc_id = vpc_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网ID
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

    def set_id(self, id):
        """
        :param id: 物理机id，同时支持传入resourceID和底层uuid
        """
        self.id = id

    def set_ip_type(self, ip_type):
        """
        :param ip_type: 弹性IP版本：取值范围:[ipv4=v4地址,ipv6=v6地址]，默认值:ipv4 (暂不支持该参数)
        """
        self.ip_type = ip_type

    def set_status(self, status):
        """
        :param status: 实例状态：   
         "RUNNING", #运行中   
         "STOPPED", #关机   
         "SHUTOFF",#关机   
         "STOPPING", #关机中   
         "STARTING", #开机中   
         "ERROR", #异常   
         "CREATING", #创建中   
         "REINSTALLING", #重装   
         "HOSTNAME_RESETTING", #宿主机名称重置中   
         "MODIFY_NETWORK", # 裸金属重置网络中   
         "RESTARTING", #重启   
         'CREATING_IMAGE', #创建镜像   
         'EXPORT_IMAGE', #裸金属创建镜像中   
         'DELETING', #退订中   
         'RESTORING', #恢复中   
         'DELETING_NETWORK', # 裸金属删除网卡中   
         'ADDING_NETWORK', # 裸金属添加网卡中   
         'ACTIVE',#运行中 同RUNNING   
         'EXPIRED', #已到期   
         'FREEZING', #冻结中
        """
        self.status = status

    def set_vip_id(self, vip_id):
        """
        :param vip_id: 虚ipID
        """
        self.vip_id = vip_id

    def set_volume_uuid(self, volume_uuid):
        """
        :param volume_uuid: 云硬盘ID
        """
        self.volume_uuid = volume_uuid

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页数
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

