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


class PaasEcsBatchCreateLiteVmRequest(CTYunRequest):
    """
    多台开通时fixedIP不能进行指定，指定后开通一台后其余会报错。   
    instanceName在批量开通多台时会按照 001 ，顺序递增。
    """

    def __init__(self, request_param):
        super(PaasEcsBatchCreateLiteVmRequest, self).__init__("/v4/paas/ecs/batch-create-lite-vm", "POST", "ct", "application/json")
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
        if self.parameters.channel_info is not None:
            if type(self.parameters.channel_info) is dict:
                channel_info_dict_value = self.parameters.channel_info
            else:
                channel_info_dict_value = self.parameters.channel_info.get_dic()
            body_param["channelInfo"] = channel_info_dict_value
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.image_type is not None:
            body_param["imageType"] = self.parameters.image_type
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.zone is not None:
            body_param["zone"] = self.parameters.zone
        if self.parameters.network_card_list is not None:
            network_card_list = []
            if isinstance(self.parameters.network_card_list, list):
                for item in self.parameters.network_card_list:
                    if type(item) is dict:
                        network_card_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        network_card_list.append(item_dict_value)
            else:
                network_card_list.append(self.parameters.network_card_list.get_dic())
            body_param["networkCardList"] = network_card_list
        if self.parameters.ext_ip is not None:
            body_param["extIP"] = self.parameters.ext_ip
        if self.parameters.boot_disk_type is not None:
            body_param["bootDiskType"] = self.parameters.boot_disk_type
        if self.parameters.boot_disk_size is not None:
            body_param["bootDiskSize"] = self.parameters.boot_disk_size
        if self.parameters.sys_volume_id is not None:
            body_param["sysVolumeID"] = self.parameters.sys_volume_id
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.sec_group_list is not None:
            body_param["secGroupList"] = self.parameters.sec_group_list
        if self.parameters.data_disk_list is not None:
            data_disk_list = []
            if isinstance(self.parameters.data_disk_list, list):
                for item in self.parameters.data_disk_list:
                    if type(item) is dict:
                        data_disk_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        data_disk_list.append(item_dict_value)
            else:
                data_disk_list.append(self.parameters.data_disk_list.get_dic())
            body_param["dataDiskList"] = data_disk_list
        if self.parameters.data_disk_id_list is not None:
            body_param["dataDiskIDList"] = self.parameters.data_disk_id_list
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.affinity_group_id is not None:
            body_param["affinityGroupID"] = self.parameters.affinity_group_id
        if self.parameters.key_pair_id is not None:
            body_param["keyPairID"] = self.parameters.key_pair_id
        if self.parameters.user_password is not None:
            body_param["userPassword"] = self.parameters.user_password
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
        if self.parameters.order_count is not None:
            body_param["orderCount"] = self.parameters.order_count
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


class ChannelInfo(object):

    def __init__(self, paas_accout_id, master_order_id, paas_resource_id, ):
        """
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算
        :param master_order_id: 中台主订单ID，IaaS记⼊话单，用来关联订单和资源
        :param paas_resource_id: IT侧订单对应资源ID
        """
        self.paas_accout_id = paas_accout_id
        self.master_order_id = master_order_id
        self.paas_resource_id = paas_resource_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.paas_accout_id is not None:
            obj_dict["paasAccoutID"] = self.paas_accout_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_accout_id is None:
            raise Exception("paas_accout_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")


class NetworkCard(object):

    def __init__(self, subnet_id, is_master, nic_name=None, fixed_ip=None, share_vpc_id=None):
        """
        :param subnet_id: 非共享网卡时该参数为vpcID对应VPC下的子网ID，共享网卡时该参数为shareVpcID对应VPC下的子网ID
        :param is_master: true：表示主网卡，false：表示扩展网卡
        :param nic_name: 网卡名称
        :param fixed_ip: 多台不能指定ip
        :param share_vpc_id: 共享网卡的虚拟私有云ID
        """
        self.subnet_id = subnet_id
        self.is_master = is_master
        self.nic_name = nic_name
        self.fixed_ip = fixed_ip
        self.share_vpc_id = share_vpc_id
        self.check_param()

    def set_nic_name(self, nic_name):
        """
        :param nic_name: 网卡名称
        """
        self.nic_name = nic_name

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 多台不能指定ip
        """
        self.fixed_ip = fixed_ip

    def set_share_vpc_id(self, share_vpc_id):
        """
        :param share_vpc_id: 共享网卡的虚拟私有云ID
        """
        self.share_vpc_id = share_vpc_id

    def get_dic(self):
        obj_dict = dict()
        if self.subnet_id is not None:
            obj_dict["subnetID"] = self.subnet_id
        if self.is_master is not None:
            obj_dict["isMaster"] = self.is_master
        if self.nic_name is not None:
            obj_dict["nicName"] = self.nic_name
        if self.fixed_ip is not None:
            obj_dict["fixedIP"] = self.fixed_ip
        if self.share_vpc_id is not None:
            obj_dict["shareVpcID"] = self.share_vpc_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.is_master is None:
            raise Exception("is_master can not None")


class DataDisk(object):

    def __init__(self, disk_size, disk_type, disk_name=None):
        """
        :param disk_size: 单位为GiB，取值范围：[10-32768]
        :param disk_type: 取值范围:SATA：普通IO，SAS：高IO，SSD：超高IO，SSD-genric：通用型SSD，FAST-SSD：极速型SSD；由于历史原因，目前仅按照前缀进行匹配
        :param disk_name: 长度2~63，不支持中文
        """
        self.disk_size = disk_size
        self.disk_type = disk_type
        self.disk_name = disk_name
        self.check_param()

    def set_disk_name(self, disk_name):
        """
        :param disk_name: 长度2~63，不支持中文
        """
        self.disk_name = disk_name

    def get_dic(self):
        obj_dict = dict()
        if self.disk_size is not None:
            obj_dict["diskSize"] = self.disk_size
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.disk_name is not None:
            obj_dict["diskName"] = self.disk_name
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.disk_size is None:
            raise Exception("disk_size can not None")
        if self.disk_type is None:
            raise Exception("disk_type can not None")


class PaasEcsBatchCreateLiteVmRequestParam(object):

    def __init__(self, client_token, region_id, az_name, instance_name, display_name, flavor_id, image_type, image_id, vpc_id, network_card_list, ext_ip, channel_info=None, zone=None, boot_disk_type=None, boot_disk_size=None, sys_volume_id=None, project_id=None, sec_group_list=None, data_disk_list=None, data_disk_id_list=None, ip_version=None, bandwidth=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, user_data=None, order_count=None):
        """
        :param channel_info: 渠道侧信息
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param instance_name: 云主机名称，不可以使用已存在的云主机名称。不同操作系统下云主机名称规则有差异。   
         Windows：长度为2 ~ 15个字符（当创建两台及两台以上的云主机时名称长度为2 ~ 10个字符），允许使用大小写字母、数字或连字符（-）。不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字；   
         其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2~59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param display_name: 云主机显示名称，长度为2-63字符
        :param flavor_id: 云主机规格ID
        :param image_type: 取值范围:<br />0：私有镜像，<br />1：公有镜像，<br />2：共享镜像，<br />3：安全镜像，<br />4：甄选镜像
        :param image_id: 镜像ID
        :param vpc_id: 虚拟私有云ID
        :param zone: 暂不支持，该参数在生成环境中作废
        :param network_card_list: 网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围:<br />0：不使用，<br />1：自动分配，<br />2：使用已有
        :param boot_disk_type: 取值范围:<br />SATA：普通IO，<br />SAS：高IO，<br />SSD：超高IO，<br />SSD-genric：通用型SSD，<br />FAST-SSD：极速型SSD,由于历史原因，目前仅按照前缀进行匹配
        :param boot_disk_size: 在不指定系统盘ID创建时，该参数必填；指定系统盘ID创建时，该参数不可填。单位为GiB，取值范围：[40-32768]
        :param sys_volume_id: 填写该参数，bootDiskType、bootDiskSize不可填，不填写该参数，bootDiskType、bootDiskSize都必填
        :param project_id: 企业项目ID
        :param sec_group_list: 安全组id列表 注意:此参数为数组
        :param data_disk_list: 填写dataDiskIDList时，该参数无效 注意:此参数为数组
        :param data_disk_id_list: 数据盘ID列表 注意:此参数为数组
        :param ip_version: （暂不支持，传参不生效）取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]， 传0或者不传默认赋100
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）
        :param affinity_group_id: 云主机组ID
        :param key_pair_id: 密钥对ID
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param order_count: 不指定默认为1，最大数量为50台。   
         注：传了sysVolumeID或者dataDiskIDList，不支持批量操作
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.instance_name = instance_name
        self.display_name = display_name
        self.flavor_id = flavor_id
        self.image_type = image_type
        self.image_id = image_id
        self.vpc_id = vpc_id
        self.zone = zone
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.boot_disk_type = boot_disk_type
        self.boot_disk_size = boot_disk_size
        self.sys_volume_id = sys_volume_id
        self.project_id = project_id
        self.sec_group_list = sec_group_list
        self.data_disk_list = data_disk_list
        self.data_disk_id_list = data_disk_id_list
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.eip_id = eip_id
        self.affinity_group_id = affinity_group_id
        self.key_pair_id = key_pair_id
        self.user_password = user_password
        self.user_data = user_data
        self.order_count = order_count

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息
        """
        self.channel_info = channel_info

    def set_zone(self, zone):
        """
        :param zone: 暂不支持，该参数在生成环境中作废
        """
        self.zone = zone

    def set_boot_disk_type(self, boot_disk_type):
        """
        :param boot_disk_type: 取值范围:<br />SATA：普通IO，<br />SAS：高IO，<br />SSD：超高IO，<br />SSD-genric：通用型SSD，<br />FAST-SSD：极速型SSD,由于历史原因，目前仅按照前缀进行匹配
        """
        self.boot_disk_type = boot_disk_type

    def set_boot_disk_size(self, boot_disk_size):
        """
        :param boot_disk_size: 在不指定系统盘ID创建时，该参数必填；指定系统盘ID创建时，该参数不可填。单位为GiB，取值范围：[40-32768]
        """
        self.boot_disk_size = boot_disk_size

    def set_sys_volume_id(self, sys_volume_id):
        """
        :param sys_volume_id: 填写该参数，bootDiskType、bootDiskSize不可填，不填写该参数，bootDiskType、bootDiskSize都必填
        """
        self.sys_volume_id = sys_volume_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_sec_group_list(self, sec_group_list):
        """
        :param sec_group_list: 安全组id列表
        """
        self.sec_group_list = sec_group_list

    def set_data_disk_list(self, data_disk_list):
        """
        :param data_disk_list: 填写dataDiskIDList时，该参数无效
        """
        self.data_disk_list = data_disk_list

    def set_data_disk_id_list(self, data_disk_id_list):
        """
        :param data_disk_id_list: 数据盘ID列表
        """
        self.data_disk_id_list = data_disk_id_list

    def set_ip_version(self, ip_version):
        """
        :param ip_version: （暂不支持，传参不生效）取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        """
        self.ip_version = ip_version

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]， 传0或者不传默认赋100
        """
        self.bandwidth = bandwidth

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）
        """
        self.eip_id = eip_id

    def set_affinity_group_id(self, affinity_group_id):
        """
        :param affinity_group_id: 云主机组ID
        """
        self.affinity_group_id = affinity_group_id

    def set_key_pair_id(self, key_pair_id):
        """
        :param key_pair_id: 密钥对ID
        """
        self.key_pair_id = key_pair_id

    def set_user_password(self, user_password):
        """
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        """
        self.user_password = user_password

    def set_user_data(self, user_data):
        """
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        """
        self.user_data = user_data

    def set_order_count(self, order_count):
        """
        :param order_count: 不指定默认为1，最大数量为50台。   
         注：传了sysVolumeID或者dataDiskIDList，不支持批量操作
        """
        self.order_count = order_count

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")
        if self.instance_name is None:
            raise Exception("instance_name can not None")
        if self.display_name is None:
            raise Exception("display_name can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")
        if self.image_type is None:
            raise Exception("image_type can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

