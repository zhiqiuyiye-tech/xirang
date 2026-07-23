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


class SfsNewRequest(CTYunRequest):
    """
    支持创建按需计费/包年包月的弹性文件系统   
    1. 弹性文件类型枚举：capacity/performance/massive/hpfs_perf   
    2. 协议类型枚举：nfs/cifs/hpfs(3.0)   
    3. 包年包月：最大周期不能超过5年/60个月
    """

    def __init__(self, request_param):
        super(SfsNewRequest, self).__init__("/v4/sfs/new", "POST", "sfs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.is_encrypt is not None:
            body_param["isEncrypt"] = self.parameters.is_encrypt
        if self.parameters.kms_uuid is not None:
            body_param["kmsUUID"] = self.parameters.kms_uuid
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.sfs_type is not None:
            body_param["sfsType"] = self.parameters.sfs_type
        if self.parameters.sfs_protocol is not None:
            body_param["sfsProtocol"] = self.parameters.sfs_protocol
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class SfsNewRequestParam(object):

    def __init__(self, region_id, sfs_type, sfs_protocol, name, sfs_size, az_name=None, client_token=None, is_encrypt=None, kms_uuid=None, project_id=None, on_demand=None, cycle_type=None, cycle_count=None, vpc=None, subnet=None):
        """
        :param az_name: 多可用区资源池下，必须指定可用区
        :param client_token: 客户端存根
        :param region_id: 资源池 ID
        :param is_encrypt: 是否加密盘，true/false，默认 false
        :param kms_uuid: 如果是加密盘，需要提供 kms 的 uuid
        :param project_id: 资源所属企业项目 ID
        :param sfs_type: 弹性文件类型，capacity/performance/massive/hpfs_perf，massive/hpfs_perf为3.0参数
        :param sfs_protocol: 协议类型，nfs/cifs/hpfs, nfs 适用于 linux，cifs 适用于 windows，hpfs适用3.0并行文件
        :param name: 弹性文件名,2-63字符限制，支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param sfs_size: 大小，单位 GB，最小100，最大327680GB
        :param on_demand: 是否按需下单。true/false，默认为 false
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定。周期最大长度不能超过 5年/60个月
        :param vpc: 虚拟网 ID，非hpfs时，必传
        :param subnet: 子网 ID，非hpfs时，必传
        """
        self.az_name = az_name
        self.client_token = client_token
        self.region_id = region_id
        self.is_encrypt = is_encrypt
        self.kms_uuid = kms_uuid
        self.project_id = project_id
        self.sfs_type = sfs_type
        self.sfs_protocol = sfs_protocol
        self.name = name
        self.sfs_size = sfs_size
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.vpc = vpc
        self.subnet = subnet

    def set_az_name(self, az_name):
        """
        :param az_name: 多可用区资源池下，必须指定可用区
        """
        self.az_name = az_name

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_is_encrypt(self, is_encrypt):
        """
        :param is_encrypt: 是否加密盘，true/false，默认 false
        """
        self.is_encrypt = is_encrypt

    def set_kms_uuid(self, kms_uuid):
        """
        :param kms_uuid: 如果是加密盘，需要提供 kms 的 uuid
        """
        self.kms_uuid = kms_uuid

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目 ID
        """
        self.project_id = project_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需下单。true/false，默认为 false
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期（subscription）类型，year/month。onDemand 为 false 时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数。onDemand 为 false 时必须指定。周期最大长度不能超过 5年/60个月
        """
        self.cycle_count = cycle_count

    def set_vpc(self, vpc):
        """
        :param vpc: 虚拟网 ID，非hpfs时，必传
        """
        self.vpc = vpc

    def set_subnet(self, subnet):
        """
        :param subnet: 子网 ID，非hpfs时，必传
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
        if self.name is None:
            raise Exception("name can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")

