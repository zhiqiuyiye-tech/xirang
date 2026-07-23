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


class NewSfsRequest(CTYunRequest):
    """
    1. 用户vpc/subnet资源可用   
    2. regionID资源池支持sfsType类型的并行文件（查询可用区及可用区所支持的文件系统类型：/v4/sfs/zonelist）   
    3. 底层集群剩余可用空间大于sfsSize，sfsSize大小区间为[512GB, 1048576GB]，步长为512GB   
        例：sfsSize入参为514GB时，基于512GB的步长，调整为1024GB规格   
    4. 用户配额大小默认为50TB   
    5. 目前只支持按需下单   
    6. 新开通的文件系统会自动绑定默认权限组   
       
    开通名称不能重复   
    私有协议(即sfsProtocol为hpfs)时 不校验vpc
    """

    def __init__(self, request_param):
        super(NewSfsRequest, self).__init__("/v4/hpfs/new-sfs", "POST", "hpfs", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.sfs_type is not None:
            body_param["sfsType"] = self.parameters.sfs_type
        if self.parameters.sfs_protocol is not None:
            body_param["sfsProtocol"] = self.parameters.sfs_protocol
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.sfs_name is not None:
            body_param["sfsName"] = self.parameters.sfs_name
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.vpc is not None:
            body_param["vpc"] = self.parameters.vpc
        if self.parameters.subnet is not None:
            body_param["subnet"] = self.parameters.subnet
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


class NewSfsRequestParam(object):

    def __init__(self, region_id, sfs_type, sfs_protocol, sfs_name, sfs_size, az_name, client_token=None, project_id=None, on_demand=None, cycle_type=None, cycle_count=None, vpc=None, subnet=None):
        """
        :param client_token: 客户端存根
        :param region_id: 资源池 ID
        :param project_id: 资源所属企业项目 ID
        :param sfs_type: 并行文件类型，hpfs_perf(HPC性能型)
        :param sfs_protocol: 协议类型,nfs/hpfs
        :param on_demand: 是否按需下单。true/false，默认为 true 
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定。周期最大长度不能超过 5 年
        :param sfs_name: 并行文件名。单账户单资源池下，命名需唯一；   
         命名规则：长度2~63字符，支持使用字母、数字、中划线(-)，只能以字母开头、以数字或字母结尾
        :param sfs_size: 大小，单位 GB, 最小512G
        :param az_name: 多可用区资源池下，必须指定可用区。如不指定则在数据库中自动匹配
        :param vpc: 虚拟网 ID（私有协议sfsProtocol为hpfs时不支持）
        :param subnet: 子网 ID（私有协议sfsProtocol为hpfs时不支持）
        """
        self.client_token = client_token
        self.region_id = region_id
        self.project_id = project_id
        self.sfs_type = sfs_type
        self.sfs_protocol = sfs_protocol
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.sfs_name = sfs_name
        self.sfs_size = sfs_size
        self.az_name = az_name
        self.vpc = vpc
        self.subnet = subnet

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目 ID
        """
        self.project_id = project_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需下单。true/false，默认为 true 
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定。周期最大长度不能超过 5 年
        """
        self.cycle_count = cycle_count

    def set_vpc(self, vpc):
        """
        :param vpc: 虚拟网 ID（私有协议sfsProtocol为hpfs时不支持）
        """
        self.vpc = vpc

    def set_subnet(self, subnet):
        """
        :param subnet: 子网 ID（私有协议sfsProtocol为hpfs时不支持）
        """
        self.subnet = subnet

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_type is None:
            raise Exception("sfs_type can not None")
        if self.sfs_protocol is None:
            raise Exception("sfs_protocol can not None")
        if self.sfs_name is None:
            raise Exception("sfs_name can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")

