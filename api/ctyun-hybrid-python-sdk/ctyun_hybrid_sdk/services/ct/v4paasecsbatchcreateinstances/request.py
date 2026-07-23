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


class V4PaasEcsBatchCreateInstancesRequest(CTYunRequest):
    """
    多台开通时fixedIP不能进行指定，指定后开通一台后其余会报错。   
    instanceName在批量开通多台时会按照 001 ，顺序递增。   
    sysVolumeID 此参数暂不支持。
    """

    def __init__(self, request_param):
        super(V4PaasEcsBatchCreateInstancesRequest, self).__init__("/v4/paas/ecs/batch-create-instances", "POST", "ct", "application/json")
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
        if self.parameters.destination_eip_cidrs is not None:
            destination_eip_cidrs = []
            if isinstance(self.parameters.destination_eip_cidrs, list):
                for item in self.parameters.destination_eip_cidrs:
                    if type(item) is dict:
                        destination_eip_cidrs.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        destination_eip_cidrs.append(item_dict_value)
            else:
                destination_eip_cidrs.append(self.parameters.destination_eip_cidrs.get_dic())
            body_param["destinationEipCidrs"] = destination_eip_cidrs
        if self.parameters.boot_disk_type is not None:
            body_param["bootDiskType"] = self.parameters.boot_disk_type
        if self.parameters.boot_disk_size is not None:
            body_param["bootDiskSize"] = self.parameters.boot_disk_size
        if self.parameters.sys_volume_id is not None:
            body_param["sysVolumeID"] = self.parameters.sys_volume_id
        if self.parameters.dss_cluster_id is not None:
            body_param["dssClusterID"] = self.parameters.dss_cluster_id
        if self.parameters.dss_pool_id is not None:
            body_param["dssPoolID"] = self.parameters.dss_pool_id
        if self.parameters.pool_id is not None:
            body_param["poolID"] = self.parameters.pool_id
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
        if self.parameters.local_disk_list is not None:
            local_disk_list = []
            if isinstance(self.parameters.local_disk_list, list):
                for item in self.parameters.local_disk_list:
                    if type(item) is dict:
                        local_disk_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        local_disk_list.append(item_dict_value)
            else:
                local_disk_list.append(self.parameters.local_disk_list.get_dic())
            body_param["localDiskList"] = local_disk_list
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
        if self.parameters.dec_id is not None:
            body_param["decID"] = self.parameters.dec_id
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

    def __init__(self, paas_account_id, master_order_id, paas_resource_id, ):
        """
        :param paas_account_id: paas账号，资源的付费账号，通过上送IT用于内部结算
        :param master_order_id: 中台主订单ID，IaaS记⼊话单，用来关联订单和资源
        :param paas_resource_id: IT侧订单对应资源ID
        """
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.paas_resource_id = paas_resource_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_account_id is None:
            raise Exception("paas_account_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")


class NetworkCard(object):

    def __init__(self, subnet_id, is_master, nic_name=None, fixed_ip=None, share_vpc_id=None, enable_ipv6=None):
        """
        :param subnet_id: 非共享网卡时该参数为vpcID对应VPC下的子网ID，共享网卡时该参数为shareVpcID对应VPC下的子网ID
        :param is_master: true：表示主网卡，false：表示扩展网卡
        :param nic_name: 网卡名称
        :param fixed_ip: 多台不能指定ip
        :param share_vpc_id: 共享网卡的虚拟私有云ID
        :param enable_ipv6: 该参数不填情况下，网卡默认跟随子网。注：当前参数仅支持多可用区类型资源池（即4.0资源池）；仅在同级参数subnetID对应子网支持ipv6情况下，该参数有效；共享网卡该参数无效。
        """
        self.subnet_id = subnet_id
        self.is_master = is_master
        self.nic_name = nic_name
        self.fixed_ip = fixed_ip
        self.share_vpc_id = share_vpc_id
        self.enable_ipv6 = enable_ipv6
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

    def set_enable_ipv6(self, enable_ipv6):
        """
        :param enable_ipv6: 该参数不填情况下，网卡默认跟随子网。注：当前参数仅支持多可用区类型资源池（即4.0资源池）；仅在同级参数subnetID对应子网支持ipv6情况下，该参数有效；共享网卡该参数无效。
        """
        self.enable_ipv6 = enable_ipv6

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
        if self.enable_ipv6 is not None:
            obj_dict["enableIpv6"] = self.enable_ipv6
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.is_master is None:
            raise Exception("is_master can not None")


class DestinationEipCidr(object):

    def __init__(self, start, end, ):
        """
        :param start: 
        :param end: 
        """
        self.start = start
        self.end = end
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.start is not None:
            obj_dict["start"] = self.start
        if self.end is not None:
            obj_dict["end"] = self.end
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.start is None:
            raise Exception("start can not None")
        if self.end is None:
            raise Exception("end can not None")


class DataDisk(object):

    def __init__(self, size, disk_type, disk_name=None, cmk_id=None, is_encrypt=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None):
        """
        :param size: 磁盘容量, 5-2000GB, 磁盘类型为system的磁盘容量最小为100G
        :param disk_type: 取值范围:SATA：普通IO，SAS：高IO，SSD：超高IO，SSD-genric：通用型SSD，FAST-SSD：极速型SSD；由于历史原因，目前仅按照前缀进行匹配
        :param disk_name: 长度2~63，不支持中文
        :param cmk_id: 暂不支持
        :param is_encrypt: 默认值为false
        :param dss_cluster_id: 专属集群ID
        :param dss_pool_id: 专属集群存储池ID
        :param pool_id: 非专属集群存储池ID
        """
        self.size = size
        self.disk_type = disk_type
        self.disk_name = disk_name
        self.cmk_id = cmk_id
        self.is_encrypt = is_encrypt
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.check_param()

    def set_disk_name(self, disk_name):
        """
        :param disk_name: 长度2~63，不支持中文
        """
        self.disk_name = disk_name

    def set_cmk_id(self, cmk_id):
        """
        :param cmk_id: 暂不支持
        """
        self.cmk_id = cmk_id

    def set_is_encrypt(self, is_encrypt):
        """
        :param is_encrypt: 默认值为false
        """
        self.is_encrypt = is_encrypt

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 专属集群ID
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 专属集群存储池ID
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 非专属集群存储池ID
        """
        self.pool_id = pool_id

    def get_dic(self):
        obj_dict = dict()
        if self.size is not None:
            obj_dict["size"] = self.size
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.disk_name is not None:
            obj_dict["diskName"] = self.disk_name
        if self.cmk_id is not None:
            obj_dict["cmkID"] = self.cmk_id
        if self.is_encrypt is not None:
            obj_dict["isEncrypt"] = self.is_encrypt
        if self.dss_cluster_id is not None:
            obj_dict["dssClusterID"] = self.dss_cluster_id
        if self.dss_pool_id is not None:
            obj_dict["dssPoolID"] = self.dss_pool_id
        if self.pool_id is not None:
            obj_dict["poolID"] = self.pool_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.size is None:
            raise Exception("size can not None")
        if self.disk_type is None:
            raise Exception("disk_type can not None")


class LocalDisk(object):

    def __init__(self, disk_type, disk_size, ):
        """
        :param disk_type: LOCAL-NVME-public / LOCAL-SATA-public
        :param disk_size: 可取范围100GB-资源池配置上限LocalDiskSizeLimit(默认2TB, 最大6TB)
        """
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.disk_size is not None:
            obj_dict["diskSize"] = self.disk_size
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.disk_type is None:
            raise Exception("disk_type can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")


class V4PaasEcsBatchCreateInstancesRequestParam(object):

    def __init__(self, client_token, region_id, instance_name, display_name, flavor_id, image_type, image_id, vpc_id, network_card_list, ext_ip, local_disk_list, channel_info=None, az_name=None, destination_eip_cidrs=None, boot_disk_type=None, boot_disk_size=None, sys_volume_id=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None, project_id=None, sec_group_list=None, data_disk_list=None, data_disk_id_list=None, ip_version=None, bandwidth=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, user_data=None, order_count=None, dec_id=None):
        """
        :param channel_info: 渠道侧信息
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param az_name: 可用区名称(4.0必填)
        :param instance_name: 云主机名称，不可以使用已存在的云主机名称。不同操作系统下，云主机名称规则有差异。 Windows：长度为2-15个字符（当创建两台及两台以上的云主机时名称长度为2-10个字符），允许使用大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字； 其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2-59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param display_name: 云主机显示名称，长度为2-63字符
        :param flavor_id: 云主机规格ID
        :param image_type: 暂时不支持，取值范围:<br />0：私有镜像，<br />1：公有镜像，<br />2：共享镜像，<br />3：安全镜像，<br />4：甄选镜像
        :param image_id: 镜像ID
        :param vpc_id: 虚拟私有云ID
        :param network_card_list: 网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围:<br />0：不使用，<br />1：自动分配，<br />2：使用已有   
         注：当extIP=2时，必须传eipID
        :param destination_eip_cidrs: extIP=1时有效 注意:此参数为数组
        :param boot_disk_type: 取值范围:<br />SATA：普通IO，<br />SAS：高IO，<br />SSD：超高IO，<br />SSD-genric：通用型SSD，<br />FAST-SSD：极速型SSD,由于历史原因，目前仅按照前缀进行匹配
        :param boot_disk_size: 在不指定系统盘ID创建时，该参数必填；指定系统盘ID创建时，该参数不可填。单位为GiB，取值范围：[40-32768]
        :param sys_volume_id: 填写该参数，bootDiskType、bootDiskSize不可填，不填写该参数，bootDiskType、bootDiskSize都必填
        :param dss_cluster_id: 系统盘专属集群ID
        :param dss_pool_id: 系统盘专属集群存储池ID
        :param pool_id: 系统盘非专属集群存储池ID
        :param project_id: 企业项目ID
        :param sec_group_list: 安全组id列表 注意:此参数为数组
        :param data_disk_list: 填写dataDiskIDList时，该参数无效 注意:此参数为数组
        :param data_disk_id_list: 数据盘ID列表 注意:此参数为数组
        :param local_disk_list: 目前仅4.0资源池的kir4规格族支持   
         * 校验本地盘数量：1-6块   
         * 校验所有本地盘类型必须相同 注意:此参数为数组
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]，传0或者 不传默认赋100
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）
        :param affinity_group_id: 云主机组ID
        :param key_pair_id: 密钥对ID
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param order_count: 不指定默认为1，最大数量为50台。
        :param dec_id: 计算专属云ID
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
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.destination_eip_cidrs = destination_eip_cidrs
        self.boot_disk_type = boot_disk_type
        self.boot_disk_size = boot_disk_size
        self.sys_volume_id = sys_volume_id
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.project_id = project_id
        self.sec_group_list = sec_group_list
        self.data_disk_list = data_disk_list
        self.data_disk_id_list = data_disk_id_list
        self.local_disk_list = local_disk_list
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.eip_id = eip_id
        self.affinity_group_id = affinity_group_id
        self.key_pair_id = key_pair_id
        self.user_password = user_password
        self.user_data = user_data
        self.order_count = order_count
        self.dec_id = dec_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息
        """
        self.channel_info = channel_info

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(4.0必填)
        """
        self.az_name = az_name

    def set_destination_eip_cidrs(self, destination_eip_cidrs):
        """
        :param destination_eip_cidrs: extIP=1时有效
        """
        self.destination_eip_cidrs = destination_eip_cidrs

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

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 系统盘专属集群ID
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 系统盘专属集群存储池ID
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 系统盘非专属集群存储池ID
        """
        self.pool_id = pool_id

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
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        """
        self.ip_version = ip_version

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]，传0或者 不传默认赋100
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
        """
        self.order_count = order_count

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 计算专属云ID
        """
        self.dec_id = dec_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
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
        if self.local_disk_list is None:
            raise Exception("local_disk_list can not None")

