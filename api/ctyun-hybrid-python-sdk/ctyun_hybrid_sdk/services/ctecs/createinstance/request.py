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


class CreateInstanceRequest(CTYunRequest):
    """
    1. 目前不支持预付费账户创建按需付费类型云主机   
    2. 计费模式选择包年包月计费方式时，需要填写订购周期类型与订购时长   
    3. 自动分配弹性IP（extIP="1"）时，需要填写弹性IP版本（ipVersion）与带宽大小（bandwidth）；使用已有的弹性IP（extIP="2"）时，需要填写弹性IP的版本（ipVersion），和对应弹性IP的ID（eipID或ipv6AddressID）   
    4. 挂载网卡时，子网与虚拟私有云存在对应关系，确保子网属于当前虚拟私有云   
    5. 云主机绑定多个标签时，标签键（参数labelKey）不可重复，单台云主机最多可绑定10个标签   
    6. 因对接方原因，instanceName允许重复
    """

    def __init__(self, request_param):
        super(CreateInstanceRequest, self).__init__("/v4/ecs/create-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.flavor_name is not None:
            body_param["flavorName"] = self.parameters.flavor_name
        if self.parameters.image_type is not None:
            body_param["imageType"] = self.parameters.image_type
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
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
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.sec_group_list is not None:
            body_param["secGroupList"] = self.parameters.sec_group_list
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
        if self.parameters.ip_version is not None:
            body_param["ipVersion"] = self.parameters.ip_version
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.ipv6_address_id is not None:
            body_param["ipv6AddressID"] = self.parameters.ipv6_address_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.affinity_group_id is not None:
            body_param["affinityGroupID"] = self.parameters.affinity_group_id
        if self.parameters.key_pair_id is not None:
            body_param["keyPairID"] = self.parameters.key_pair_id
        if self.parameters.user_password is not None:
            body_param["userPassword"] = self.parameters.user_password
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.auto_renew_status is not None:
            body_param["autoRenewStatus"] = self.parameters.auto_renew_status
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
        if self.parameters.pay_voucher_price is not None:
            body_param["payVoucherPrice"] = self.parameters.pay_voucher_price
        if self.parameters.label_list is not None:
            label_list = []
            if isinstance(self.parameters.label_list, list):
                for item in self.parameters.label_list:
                    if type(item) is dict:
                        label_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        label_list.append(item_dict_value)
            else:
                label_list.append(self.parameters.label_list.get_dic())
            body_param["labelList"] = label_list
        if self.parameters.gpu_driver_kits is not None:
            body_param["gpuDriverKits"] = self.parameters.gpu_driver_kits
        if self.parameters.monitor_service is not None:
            body_param["monitorService"] = self.parameters.monitor_service
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.dec_id is not None:
            body_param["decID"] = self.parameters.dec_id
        if self.parameters.dec_host_id is not None:
            body_param["decHostID"] = self.parameters.dec_host_id
        if self.parameters.host_id is not None:
            body_param["hostID"] = self.parameters.host_id
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


class DataDisk(object):

    def __init__(self, disk_type, disk_size, disk_mode=None, cmk_id=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None):
        """
        :param disk_mode: （暂不支持，传参不生效）云硬盘属性，取值范围: [FCSAN、ISCSI、VBD]，默认值为VBD
        :param disk_type: 云硬盘类型，取值范围： SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        :param disk_size: 磁盘容量大小单位为GiB，取值范围[10-32768]，单位GB
        :param cmk_id: （暂不支持，传参不生效）注：加密数据盘填写该参数
        :param dss_cluster_id: 专属集群ID
        :param dss_pool_id: 专属集群存储池ID
        :param pool_id: 非专属集群存储池ID
        """
        self.disk_mode = disk_mode
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.cmk_id = cmk_id
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.check_param()

    def set_disk_mode(self, disk_mode):
        """
        :param disk_mode: （暂不支持，传参不生效）云硬盘属性，取值范围: [FCSAN、ISCSI、VBD]，默认值为VBD
        """
        self.disk_mode = disk_mode

    def set_cmk_id(self, cmk_id):
        """
        :param cmk_id: （暂不支持，传参不生效）注：加密数据盘填写该参数
        """
        self.cmk_id = cmk_id

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
        if self.disk_mode is not None:
            obj_dict["diskMode"] = self.disk_mode
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.disk_size is not None:
            obj_dict["diskSize"] = self.disk_size
        if self.cmk_id is not None:
            obj_dict["cmkID"] = self.cmk_id
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
        if self.disk_type is None:
            raise Exception("disk_type can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")


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


class NetworkCard(object):

    def __init__(self, is_master, subnet_id, fixed_ip=None, enable_ipv6=None, ipv6_address=None):
        """
        :param fixed_ip: 内网IPv4地址
        :param is_master: 是否主网卡，取值范围： true：主网卡， false：扩展网卡
        :param subnet_id: 子网id 
        :param enable_ipv6: 是否开启ipv6，不传默认跟随子网
        :param ipv6_address: 开启ipv6时可指定地址
        """
        self.fixed_ip = fixed_ip
        self.is_master = is_master
        self.subnet_id = subnet_id
        self.enable_ipv6 = enable_ipv6
        self.ipv6_address = ipv6_address
        self.check_param()

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
        """
        self.fixed_ip = fixed_ip

    def set_enable_ipv6(self, enable_ipv6):
        """
        :param enable_ipv6: 是否开启ipv6，不传默认跟随子网
        """
        self.enable_ipv6 = enable_ipv6

    def set_ipv6_address(self, ipv6_address):
        """
        :param ipv6_address: 开启ipv6时可指定地址
        """
        self.ipv6_address = ipv6_address

    def get_dic(self):
        obj_dict = dict()
        if self.fixed_ip is not None:
            obj_dict["fixedIP"] = self.fixed_ip
        if self.is_master is not None:
            obj_dict["isMaster"] = self.is_master
        if self.subnet_id is not None:
            obj_dict["subnetID"] = self.subnet_id
        if self.enable_ipv6 is not None:
            obj_dict["enableIpv6"] = self.enable_ipv6
        if self.ipv6_address is not None:
            obj_dict["ipv6Address"] = self.ipv6_address
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.is_master is None:
            raise Exception("is_master can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")


class Label(object):

    def __init__(self, label_key, label_value, ):
        """
        :param label_key: 长度限制1~32字符，注：同一台云主机绑定多个标签时，标签键不可重复
        :param label_value: 长度限制1~32字符
        """
        self.label_key = label_key
        self.label_value = label_value
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.label_key is not None:
            obj_dict["labelKey"] = self.label_key
        if self.label_value is not None:
            obj_dict["labelValue"] = self.label_value
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.label_key is None:
            raise Exception("label_key can not None")
        if self.label_value is None:
            raise Exception("label_value can not None")


class CreateInstanceRequestParam(object):

    def __init__(self, region_id, instance_name, display_name, local_disk_list, vpc_id, network_card_list, ext_ip, client_token=None, az_name=None, flavor_id=None, flavor_name=None, image_type=None, image_id=None, boot_disk_type=None, boot_disk_size=None, sys_volume_id=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None, data_disk_list=None, on_demand=None, sec_group_list=None, ip_version=None, bandwidth=None, ipv6_address_id=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, cycle_count=None, cycle_type=None, auto_renew_status=None, user_data=None, pay_voucher_price=None, label_list=None, gpu_driver_kits=None, monitor_service=None, project_id=None, dec_id=None, dec_host_id=None, host_id=None, order_count=None):
        """
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param region_id: 资源池ID
        :param az_name: 4.0资源池必填，当多可用区时支持随机分配可用区，本字段填写random
        :param instance_name: 不同操作系统下，云主机名称规则有差异。 Windows：长度为2-15个字符（当创建两台及两台以上的云主机时名称长度为2-10个字符），允许使用大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字； 其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2-59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param display_name: 长度为2-63字符
        :param flavor_id: 注：同一规格名称在不同资源池不同可用区的规格ID是不同的，调用前需确认规格ID是否归属当前资源池，多可用区资源池确认是否归属当前可用区
        :param flavor_name: 注：当创建云主机随机分配可用区时，规格名称为必填项，规格ID无效。当采用确定可用区时，规格ID和规格名称两者均可使用，必填其中一个，当两个都填写以规格ID为准。
        :param image_type: 镜像类型，取值范围: 0：私有镜像， 1：公有镜像， 2：共享镜像， 3：安全镜像， 4：甄选镜像
        :param image_id: sysVolumeID为空时必填
        :param boot_disk_type: sysVolumeID为空时必填，取值范围: SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        :param boot_disk_size: sysVolumeID为空时必填，取值范围[40-32768]
        :param sys_volume_id: 指定系统盘创建云主机场景
        :param dss_cluster_id: 系统盘指定专属集群ID
        :param dss_pool_id: 系统盘指定专属集群存储池ID
        :param pool_id: 系统盘指定非专属集群存储池
        :param data_disk_list: 数据盘 注意:此参数为数组
        :param local_disk_list: 目前仅4.0资源池的kir4规格族支持   
         * 校验本地盘数量：1-6块   
         * 校验所有本地盘类型必须相同 注意:此参数为数组
        :param vpc_id: 虚拟私有云ID 
        :param on_demand: sysVolumeID为空时必填，取值范围：false（按周期），true（按需）注：按周期（false）创建云主机需要同时指定cycleCount和cycleType参数；   
         sysVolumeID不为空时，云主机计费方式和云硬盘保持一致
        :param sec_group_list: 安全组ID列表，默认使用默认安全组，无默认安全组情况下请填写该参数 注意:此参数为数组
        :param network_card_list: 最大支持7张网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围: 0：不使用， 1：自动分配，自动分配需指定带宽大小， 2：使用已有   
         注1：当extIP=2时，必须传eipID
        :param ip_version: （暂不支持，传参不生效）弹性IP版本，取值范围: ipv4：v4地址， ipv6：v6地址， 默认选择ipv4
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        :param ipv6_address_id: pv6地址的ID（多可用区类资源池暂不支持）	
        :param eip_id: 弹性公网IP的ID
        :param affinity_group_id: 云主机亲和组ID 
        :param key_pair_id: 密钥对ID 
        :param user_password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年
        :param cycle_type: （按周期必传）表示订购周期类型，取值范围： MONTH：按月， YEAR：按年， 最长订购周期为5年
        :param auto_renew_status: （暂不支持，传参不生效）是否自动续订 ，取值范围： 0：不续费， 1：自动续费， 按月购买：自动续订周期为1个月， 按年购买：自动续订周期为1年
        :param user_data: 用户自定义数据,需要以Base64方式编码,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param pay_voucher_price: （暂不支持，传参不生效）满足以下规则： 两位小数，不足两位自动补0，超过两位小数无效； 不可为负数； 注：字段为0时表示不使用代金券，默认不使用
        :param label_list: （暂不支持，传参不生效）注：单台云主机最多可绑定10个标签；主机创建完成后，云主机变为运行状态，此时标签仍可能未绑定，需等待一段时间（0~10分钟）。 注意:此参数为数组
        :param gpu_driver_kits: （暂不支持，传参不生效）仅在同时选择NVIDIA显卡、计算加速型、linux公共镜像三个条件下，支持安装驱动
        :param monitor_service: （暂不支持，传参不生效）支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启） 若指定该参数为true或不指定该参数，云主机内默认开启最新详细监控服务。 若指定该参数为false，默认公共镜像不开启最新监控服务；私有镜像使用镜像中保留的监控服务。
        :param project_id: 企业项目ID
        :param dec_id: 指定专属云内自由调度
        :param dec_host_id: 指定宿主机，与decID一起传时校验组合关系
        :param host_id: 指定宿主机uuid
        :param order_count: 订购数量，不传默认是1
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.instance_name = instance_name
        self.display_name = display_name
        self.flavor_id = flavor_id
        self.flavor_name = flavor_name
        self.image_type = image_type
        self.image_id = image_id
        self.boot_disk_type = boot_disk_type
        self.boot_disk_size = boot_disk_size
        self.sys_volume_id = sys_volume_id
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.data_disk_list = data_disk_list
        self.local_disk_list = local_disk_list
        self.vpc_id = vpc_id
        self.on_demand = on_demand
        self.sec_group_list = sec_group_list
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.ipv6_address_id = ipv6_address_id
        self.eip_id = eip_id
        self.affinity_group_id = affinity_group_id
        self.key_pair_id = key_pair_id
        self.user_password = user_password
        self.cycle_count = cycle_count
        self.cycle_type = cycle_type
        self.auto_renew_status = auto_renew_status
        self.user_data = user_data
        self.pay_voucher_price = pay_voucher_price
        self.label_list = label_list
        self.gpu_driver_kits = gpu_driver_kits
        self.monitor_service = monitor_service
        self.project_id = project_id
        self.dec_id = dec_id
        self.dec_host_id = dec_host_id
        self.host_id = host_id
        self.order_count = order_count

    def set_client_token(self, client_token):
        """
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 4.0资源池必填，当多可用区时支持随机分配可用区，本字段填写random
        """
        self.az_name = az_name

    def set_flavor_id(self, flavor_id):
        """
        :param flavor_id: 注：同一规格名称在不同资源池不同可用区的规格ID是不同的，调用前需确认规格ID是否归属当前资源池，多可用区资源池确认是否归属当前可用区
        """
        self.flavor_id = flavor_id

    def set_flavor_name(self, flavor_name):
        """
        :param flavor_name: 注：当创建云主机随机分配可用区时，规格名称为必填项，规格ID无效。当采用确定可用区时，规格ID和规格名称两者均可使用，必填其中一个，当两个都填写以规格ID为准。
        """
        self.flavor_name = flavor_name

    def set_image_type(self, image_type):
        """
        :param image_type: 镜像类型，取值范围: 0：私有镜像， 1：公有镜像， 2：共享镜像， 3：安全镜像， 4：甄选镜像
        """
        self.image_type = image_type

    def set_image_id(self, image_id):
        """
        :param image_id: sysVolumeID为空时必填
        """
        self.image_id = image_id

    def set_boot_disk_type(self, boot_disk_type):
        """
        :param boot_disk_type: sysVolumeID为空时必填，取值范围: SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        """
        self.boot_disk_type = boot_disk_type

    def set_boot_disk_size(self, boot_disk_size):
        """
        :param boot_disk_size: sysVolumeID为空时必填，取值范围[40-32768]
        """
        self.boot_disk_size = boot_disk_size

    def set_sys_volume_id(self, sys_volume_id):
        """
        :param sys_volume_id: 指定系统盘创建云主机场景
        """
        self.sys_volume_id = sys_volume_id

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 系统盘指定专属集群ID
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 系统盘指定专属集群存储池ID
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 系统盘指定非专属集群存储池
        """
        self.pool_id = pool_id

    def set_data_disk_list(self, data_disk_list):
        """
        :param data_disk_list: 数据盘
        """
        self.data_disk_list = data_disk_list

    def set_on_demand(self, on_demand):
        """
        :param on_demand: sysVolumeID为空时必填，取值范围：false（按周期），true（按需）注：按周期（false）创建云主机需要同时指定cycleCount和cycleType参数；   
         sysVolumeID不为空时，云主机计费方式和云硬盘保持一致
        """
        self.on_demand = on_demand

    def set_sec_group_list(self, sec_group_list):
        """
        :param sec_group_list: 安全组ID列表，默认使用默认安全组，无默认安全组情况下请填写该参数
        """
        self.sec_group_list = sec_group_list

    def set_ip_version(self, ip_version):
        """
        :param ip_version: （暂不支持，传参不生效）弹性IP版本，取值范围: ipv4：v4地址， ipv6：v6地址， 默认选择ipv4
        """
        self.ip_version = ip_version

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        """
        self.bandwidth = bandwidth

    def set_ipv6_address_id(self, ipv6_address_id):
        """
        :param ipv6_address_id: pv6地址的ID（多可用区类资源池暂不支持）	
        """
        self.ipv6_address_id = ipv6_address_id

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID
        """
        self.eip_id = eip_id

    def set_affinity_group_id(self, affinity_group_id):
        """
        :param affinity_group_id: 云主机亲和组ID 
        """
        self.affinity_group_id = affinity_group_id

    def set_key_pair_id(self, key_pair_id):
        """
        :param key_pair_id: 密钥对ID 
        """
        self.key_pair_id = key_pair_id

    def set_user_password(self, user_password):
        """
        :param user_password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等
        """
        self.user_password = user_password

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年
        """
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: （按周期必传）表示订购周期类型，取值范围： MONTH：按月， YEAR：按年， 最长订购周期为5年
        """
        self.cycle_type = cycle_type

    def set_auto_renew_status(self, auto_renew_status):
        """
        :param auto_renew_status: （暂不支持，传参不生效）是否自动续订 ，取值范围： 0：不续费， 1：自动续费， 按月购买：自动续订周期为1个月， 按年购买：自动续订周期为1年
        """
        self.auto_renew_status = auto_renew_status

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据,需要以Base64方式编码,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        """
        self.user_data = user_data

    def set_pay_voucher_price(self, pay_voucher_price):
        """
        :param pay_voucher_price: （暂不支持，传参不生效）满足以下规则： 两位小数，不足两位自动补0，超过两位小数无效； 不可为负数； 注：字段为0时表示不使用代金券，默认不使用
        """
        self.pay_voucher_price = pay_voucher_price

    def set_label_list(self, label_list):
        """
        :param label_list: （暂不支持，传参不生效）注：单台云主机最多可绑定10个标签；主机创建完成后，云主机变为运行状态，此时标签仍可能未绑定，需等待一段时间（0~10分钟）。
        """
        self.label_list = label_list

    def set_gpu_driver_kits(self, gpu_driver_kits):
        """
        :param gpu_driver_kits: （暂不支持，传参不生效）仅在同时选择NVIDIA显卡、计算加速型、linux公共镜像三个条件下，支持安装驱动
        """
        self.gpu_driver_kits = gpu_driver_kits

    def set_monitor_service(self, monitor_service):
        """
        :param monitor_service: （暂不支持，传参不生效）支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启） 若指定该参数为true或不指定该参数，云主机内默认开启最新详细监控服务。 若指定该参数为false，默认公共镜像不开启最新监控服务；私有镜像使用镜像中保留的监控服务。
        """
        self.monitor_service = monitor_service

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 指定专属云内自由调度
        """
        self.dec_id = dec_id

    def set_dec_host_id(self, dec_host_id):
        """
        :param dec_host_id: 指定宿主机，与decID一起传时校验组合关系
        """
        self.dec_host_id = dec_host_id

    def set_host_id(self, host_id):
        """
        :param host_id: 指定宿主机uuid
        """
        self.host_id = host_id

    def set_order_count(self, order_count):
        """
        :param order_count: 订购数量，不传默认是1
        """
        self.order_count = order_count

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_name is None:
            raise Exception("instance_name can not None")
        if self.display_name is None:
            raise Exception("display_name can not None")
        if self.local_disk_list is None:
            raise Exception("local_disk_list can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

