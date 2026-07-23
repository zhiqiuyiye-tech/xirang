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


class CreateInstanceByInstanceBackupRequest(CTYunRequest):
    """
    注意：必须是当前用户的安全组 安全组和网卡的vpc必须一致
    """

    def __init__(self, request_param):
        super(CreateInstanceByInstanceBackupRequest, self).__init__("/v4/ecs/backup/create-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_backup_id is not None:
            body_param["instanceBackupID"] = self.parameters.instance_backup_id
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.dss_cluster_id is not None:
            body_param["dssClusterID"] = self.parameters.dss_cluster_id
        if self.parameters.dss_pool_id is not None:
            body_param["dssPoolID"] = self.parameters.dss_pool_id
        if self.parameters.pool_id is not None:
            body_param["poolID"] = self.parameters.pool_id
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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
        if self.parameters.monitor_service is not None:
            body_param["monitorService"] = self.parameters.monitor_service
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


class NetworkCard(object):

    def __init__(self, subnet_id, is_master, nic_name=None, fixed_ip=None):
        """
        :param subnet_id: 非共享网卡时该参数为vpcID对应VPC下的子网ID，共享网卡时该参数为shareVpcID对应VPC下的子网ID
        :param is_master: true：表示主网卡，false：表示扩展网卡
        :param nic_name: 网卡名称
        :param fixed_ip: 内网IPv4地址
        """
        self.subnet_id = subnet_id
        self.is_master = is_master
        self.nic_name = nic_name
        self.fixed_ip = fixed_ip
        self.check_param()

    def set_nic_name(self, nic_name):
        """
        :param nic_name: 网卡名称
        """
        self.nic_name = nic_name

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
        """
        self.fixed_ip = fixed_ip

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
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.is_master is None:
            raise Exception("is_master can not None")


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


class CreateInstanceByInstanceBackupRequestParam(object):

    def __init__(self, client_token, region_id, instance_name, display_name, instance_backup_id, flavor_id, vpc_id, network_card_list, ext_ip, az_name=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None, on_demand=None, sec_group_list=None, ip_version=None, bandwidth=None, ipv6_address_id=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, cycle_count=None, cycle_type=None, auto_renew_status=None, user_data=None, project_id=None, pay_voucher_price=None, label_list=None, monitor_service=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param az_name: 可用区名称，不填写时默认使用备份所在可用区。
        :param instance_name: Windows：长度为2~15个字符，允许使用大小写字母、数字或连字符（-）。不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字；<br />其他操作系统：长度为2-64字符，允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param display_name: 云主机显示名称，长度为2-63字符
        :param instance_backup_id: 云主机备份ID
        :param flavor_id: 云主机规格ID
        :param dss_cluster_id: 存储专属集群ID（不传表示不指定专属集群）
        :param dss_pool_id: 专属集群存储池ID（与 dssClusterID 配套使用）
        :param pool_id: 非专属集群存储池ID（不传表示由底层调度）
        :param vpc_id: 虚拟私有云ID
        :param on_demand: 购买方式，取值范围：<br />false（按周期），<br />true（按需<br/>onDemand=false时cycleType与cycleCount必填
        :param sec_group_list: 安全组id列表 注意:此参数为数组
        :param network_card_list: 网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围:<br />0：不使用，<br />1：自动分配，<br />2：使用已有<br/>extIP=1，bandwidth必填；extIP=2，eipID必填
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        :param ipv6_address_id: 多可用区类资源池暂不支持
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）（因弹性公网不支持ipv6，extIP=2使用已有 该字段必填）
        :param affinity_group_id: 云主机组ID
        :param key_pair_id: 密钥对ID
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        :param cycle_count: 该参数需要与cycleType一同使用<br />注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写（包周期必填>0）
        :param cycle_type: 取值范围：<br />MONTH：按月<br />YEAR：按年<br />最长订购周期为5年（包周期必填）
        :param auto_renew_status: 取值范围：<br />0（不续费），<br />1（自动续费），<br />注：按月购买，自动续订周期为3个月；按年购买，自动续订周期为1年
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param project_id: 默认值为"0"
        :param pay_voucher_price: 暂不支持
        :param label_list: （暂不支持）单台云主机最多可绑定10个标签；主机创建完成后，云主机变为运行状态，此时标签仍可能未绑定，需等待一段时间（0~10分钟）。 注意:此参数为数组
        :param monitor_service: 暂不支持
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.instance_name = instance_name
        self.display_name = display_name
        self.instance_backup_id = instance_backup_id
        self.flavor_id = flavor_id
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
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
        self.project_id = project_id
        self.pay_voucher_price = pay_voucher_price
        self.label_list = label_list
        self.monitor_service = monitor_service

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，不填写时默认使用备份所在可用区。
        """
        self.az_name = az_name

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 存储专属集群ID（不传表示不指定专属集群）
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 专属集群存储池ID（与 dssClusterID 配套使用）
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 非专属集群存储池ID（不传表示由底层调度）
        """
        self.pool_id = pool_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 购买方式，取值范围：<br />false（按周期），<br />true（按需<br/>onDemand=false时cycleType与cycleCount必填
        """
        self.on_demand = on_demand

    def set_sec_group_list(self, sec_group_list):
        """
        :param sec_group_list: 安全组id列表
        """
        self.sec_group_list = sec_group_list

    def set_ip_version(self, ip_version):
        """
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址
        """
        self.ip_version = ip_version

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        """
        self.bandwidth = bandwidth

    def set_ipv6_address_id(self, ipv6_address_id):
        """
        :param ipv6_address_id: 多可用区类资源池暂不支持
        """
        self.ipv6_address_id = ipv6_address_id

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）（因弹性公网不支持ipv6，extIP=2使用已有 该字段必填）
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

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 该参数需要与cycleType一同使用<br />注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写（包周期必填>0）
        """
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 取值范围：<br />MONTH：按月<br />YEAR：按年<br />最长订购周期为5年（包周期必填）
        """
        self.cycle_type = cycle_type

    def set_auto_renew_status(self, auto_renew_status):
        """
        :param auto_renew_status: 取值范围：<br />0（不续费），<br />1（自动续费），<br />注：按月购买，自动续订周期为3个月；按年购买，自动续订周期为1年
        """
        self.auto_renew_status = auto_renew_status

    def set_user_data(self, user_data):
        """
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        """
        self.user_data = user_data

    def set_project_id(self, project_id):
        """
        :param project_id: 默认值为"0"
        """
        self.project_id = project_id

    def set_pay_voucher_price(self, pay_voucher_price):
        """
        :param pay_voucher_price: 暂不支持
        """
        self.pay_voucher_price = pay_voucher_price

    def set_label_list(self, label_list):
        """
        :param label_list: （暂不支持）单台云主机最多可绑定10个标签；主机创建完成后，云主机变为运行状态，此时标签仍可能未绑定，需等待一段时间（0~10分钟）。
        """
        self.label_list = label_list

    def set_monitor_service(self, monitor_service):
        """
        :param monitor_service: 暂不支持
        """
        self.monitor_service = monitor_service

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
        if self.instance_backup_id is None:
            raise Exception("instance_backup_id can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

