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


class IaasEbsNewNewRequest(CTYunRequest):
    """
    支持按需/包年包月创建云硬盘。   
    云硬盘名称：diskName和name[兼容v1]，不能同时为空，不能同时非空，只传一个；
    """

    def __init__(self, request_param):
        super(IaasEbsNewNewRequest, self).__init__("/v4/ebs/new-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.multi_attach is not None:
            body_param["multiAttach"] = self.parameters.multi_attach
        if self.parameters.is_encrypt is not None:
            body_param["isEncrypt"] = self.parameters.is_encrypt
        if self.parameters.kms_uuid is not None:
            body_param["kmsUUID"] = self.parameters.kms_uuid
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.disk_mode is not None:
            body_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.disk_type is not None:
            body_param["diskType"] = self.parameters.disk_type
        if self.parameters.disk_name is not None:
            body_param["diskName"] = self.parameters.disk_name
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
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


class IaasEbsNewNewRequestParam(object):

    def __init__(self, region_id, disk_mode, disk_type, disk_size, client_token=None, multi_attach=None, is_encrypt=None, kms_uuid=None, project_id=None, disk_name=None, name=None, on_demand=None, cycle_type=None, cycle_count=None, az_name=None, image_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。
        :param region_id: 资源池Id
        :param multi_attach: 是否多云主机挂载，默认false
        :param is_encrypt: 是否加密盘，默认false
        :param kms_uuid: 如果是加密盘，需要提供kms的uuid，传入空字符串""则使用默认密钥。
        :param project_id: 企业项目ID,默认为”0”。公有云字段，混合云暂不支持，忽略
        :param disk_mode: 磁盘模式:VBD/ISCSI
        :param disk_type: 磁盘类型:SAS/SATA/SSD
        :param disk_name: 磁盘名称，diskName和name只传一个
        :param name: 磁盘名称，diskName和name只传一个
        :param disk_size: 磁盘大小,10-32768
        :param on_demand: 是否按需下单。默认为true
        :param cycle_type: 包周期类型：year/month。onDemand为false时，必须指定
        :param cycle_count: 包周期数 onDemand为false时，必须指定,。周期最大长度不能超过5年。
        :param az_name: 可用区 多可用区资源池下，必须指定可用区
        :param image_id: 支持用系统盘镜像创建系统盘，或者数据盘镜像创建数据盘，所创建的数据盘的所在地域要与镜像源一致，容量不可小于镜像对应的磁盘容量，不支持批量创建操作，从镜像创建的数据盘不支持加密、iSCSI和FCSAN高级配置
        """
        self.client_token = client_token
        self.region_id = region_id
        self.multi_attach = multi_attach
        self.is_encrypt = is_encrypt
        self.kms_uuid = kms_uuid
        self.project_id = project_id
        self.disk_mode = disk_mode
        self.disk_type = disk_type
        self.disk_name = disk_name
        self.name = name
        self.disk_size = disk_size
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.az_name = az_name
        self.image_id = image_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def set_multi_attach(self, multi_attach):
        """
        :param multi_attach: 是否多云主机挂载，默认false
        """
        self.multi_attach = multi_attach

    def set_is_encrypt(self, is_encrypt):
        """
        :param is_encrypt: 是否加密盘，默认false
        """
        self.is_encrypt = is_encrypt

    def set_kms_uuid(self, kms_uuid):
        """
        :param kms_uuid: 如果是加密盘，需要提供kms的uuid，传入空字符串""则使用默认密钥。
        """
        self.kms_uuid = kms_uuid

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID,默认为”0”。公有云字段，混合云暂不支持，忽略
        """
        self.project_id = project_id

    def set_disk_name(self, disk_name):
        """
        :param disk_name: 磁盘名称，diskName和name只传一个
        """
        self.disk_name = disk_name

    def set_name(self, name):
        """
        :param name: 磁盘名称，diskName和name只传一个
        """
        self.name = name

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需下单。默认为true
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 包周期类型：year/month。onDemand为false时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 包周期数 onDemand为false时，必须指定,。周期最大长度不能超过5年。
        """
        self.cycle_count = cycle_count

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区 多可用区资源池下，必须指定可用区
        """
        self.az_name = az_name

    def set_image_id(self, image_id):
        """
        :param image_id: 支持用系统盘镜像创建系统盘，或者数据盘镜像创建数据盘，所创建的数据盘的所在地域要与镜像源一致，容量不可小于镜像对应的磁盘容量，不支持批量创建操作，从镜像创建的数据盘不支持加密、iSCSI和FCSAN高级配置
        """
        self.image_id = image_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.disk_mode is None:
            raise Exception("disk_mode can not None")
        if self.disk_type is None:
            raise Exception("disk_type can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")

