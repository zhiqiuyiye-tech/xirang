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


class CreateEbmInstanceRequest(CTYunRequest):
    """
    创建物理机
    """

    def __init__(self, request_param):
        super(CreateEbmInstanceRequest, self).__init__("/v4/ebm/create-instance", "POST", "ebm", "application/json")
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
        if self.parameters.device_type is not None:
            body_param["deviceType"] = self.parameters.device_type
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.image_uuid is not None:
            body_param["imageUUID"] = self.parameters.image_uuid
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.system_volume_raid_uuid is not None:
            body_param["systemVolumeRaidUUID"] = self.parameters.system_volume_raid_uuid
        if self.parameters.data_volume_raid_uuid is not None:
            body_param["dataVolumeRaidUUID"] = self.parameters.data_volume_raid_uuid
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.ext_ip is not None:
            body_param["extIP"] = self.parameters.ext_ip
        if self.parameters.ip_type is not None:
            body_param["ipType"] = self.parameters.ip_type
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.public_ip is not None:
            body_param["publicIP"] = self.parameters.public_ip
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.disk_list is not None:
            disk_list = []
            if isinstance(self.parameters.disk_list, list):
                for item in self.parameters.disk_list:
                    if type(item) is dict:
                        disk_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        disk_list.append(item_dict_value)
            else:
                disk_list.append(self.parameters.disk_list.get_dic())
            body_param["diskList"] = disk_list
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
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
        if self.parameters.key_name is not None:
            body_param["keyName"] = self.parameters.key_name
        if self.parameters.auto_renew_status is not None:
            body_param["autoRenewStatus"] = self.parameters.auto_renew_status
        if self.parameters.instance_charge_type is not None:
            body_param["instanceChargeType"] = self.parameters.instance_charge_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.order_count is not None:
            body_param["orderCount"] = self.parameters.order_count
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class Disk(object):

    def __init__(self, disk_type, type, size, title=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None):
        """
        :param disk_type: 磁盘类型 ，system,data ,套餐中cloudBoot为true表示支持云盘系统盘
        :param title: 磁盘名称 ，长度2~64,不支持中文
        :param type: 磁盘分类 
        :param size: 磁盘容量, 5-2000GB
        :param dss_cluster_id: 专属集群ID
        :param dss_pool_id: 专属存储池ID
        :param pool_id: 非专属存储池ID
        """
        self.disk_type = disk_type
        self.title = title
        self.type = type
        self.size = size
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.check_param()

    def set_title(self, title):
        """
        :param title: 磁盘名称 ，长度2~64,不支持中文
        """
        self.title = title

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 专属集群ID
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 专属存储池ID
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 非专属存储池ID
        """
        self.pool_id = pool_id

    def get_dic(self):
        obj_dict = dict()
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.title is not None:
            obj_dict["title"] = self.title
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.size is not None:
            obj_dict["size"] = self.size
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
        if self.type is None:
            raise Exception("type can not None")
        if self.size is None:
            raise Exception("size can not None")


class NetworkCard(object):

    def __init__(self, master, subnet_id, title=None, fixed_ip=None, ipv6=None):
        """
        :param title: 网卡名称,，长度2~64, 不支持中文
        :param fixed_ip: 内网IPv4地址
        :param master: 是否主节点(True代表主节点
        :param ipv6: 内网IPv6地址,
        :param subnet_id: 子网id
        """
        self.title = title
        self.fixed_ip = fixed_ip
        self.master = master
        self.ipv6 = ipv6
        self.subnet_id = subnet_id
        self.check_param()

    def set_title(self, title):
        """
        :param title: 网卡名称,，长度2~64, 不支持中文
        """
        self.title = title

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
        """
        self.fixed_ip = fixed_ip

    def set_ipv6(self, ipv6):
        """
        :param ipv6: 内网IPv6地址,
        """
        self.ipv6 = ipv6

    def get_dic(self):
        obj_dict = dict()
        if self.title is not None:
            obj_dict["title"] = self.title
        if self.fixed_ip is not None:
            obj_dict["fixedIP"] = self.fixed_ip
        if self.master is not None:
            obj_dict["master"] = self.master
        if self.ipv6 is not None:
            obj_dict["ipv6"] = self.ipv6
        if self.subnet_id is not None:
            obj_dict["subnetID"] = self.subnet_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.master is None:
            raise Exception("master can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")


class CreateEbmInstanceRequestParam(object):

    def __init__(self, region_id, device_type, instance_name, hostname, image_uuid, password, vpc_id, ext_ip, network_card_list, client_token, az_name=None, system_volume_raid_uuid=None, data_volume_raid_uuid=None, ip_type=None, bandwidth=None, public_ip=None, security_group_id=None, disk_list=None, user_data=None, key_name=None, auto_renew_status=None, instance_charge_type=None, cycle_count=None, cycle_type=None, order_count=None, project_id=None):
        """
        :param region_id: 区域ID  
        :param az_name: 可用区（4.0必填）
        :param device_type: 物理机套餐类型
        :param instance_name: 物理机名称，长度为2-31位
        :param hostname: hostname，linux系统2到63位长度；windows系统2-15位长度；允许使用大小写字母、数字、连字符'-'，必须以字母开头（大小写均可），不能连续使用'-'，'-'不能用于结尾，不能仅使用数字； 支持模式串{R:x}，表示生成数字[x,x+n-1]，其中n表示购买实例的数量，1 ≤ x ≤ 9799且x只能为整数。 例子：填写server{R:3}pm，购买1台时，实例主机名为server0003pm；购买2台时，实例主机名分别为server0003pm，server0004pm )
        :param image_uuid: 物理机镜像id 
        :param password: 密码 -长度8到30位，必须包含大小写字母和（数字或者特殊字符,并且^不可用），且不能包含两位以上连续数字，如012、789等
        :param system_volume_raid_uuid: 本地系统盘raid类型，如果有本地盘则必填 
        :param data_volume_raid_uuid: 本地数据盘raid类型，如果有本地盘则必填
        :param vpc_id: 主网卡网络ID 
        :param ext_ip: 是否使用弹性公网IP ，取值范围:[1=自动分配,0=不使用,2=使用已有]
        :param ip_type: 弹性IP版本 ，取值范围:[ipv4=v4地址,ipv6=v6地址]，默认值:ipv4，eip暂不知此ipv6，这里传值只支持传ipv4
        :param bandwidth: 带宽 ，取值范围:[1~2000]，默认值:100----extIP 为1时需要
        :param public_ip: 弹性公网IP的id --extIP为2时需要
        :param security_group_id: 安全组ID，套餐smartNicExist为true可支持安全组---暂不支持
        :param disk_list: 云盘信息列表，套餐中supportCloud为true表示支持云盘   注意:此参数为数组
        :param network_card_list: 网卡 注意:此参数为数组
        :param user_data: 用户自定义数据,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param key_name: 密钥对名称
        :param auto_renew_status: （混合云暂不支持）是否自动续订，取值范围： 0（不续费）， 1（自动续费）， 注：按月购买，自动续订周期为1个月；按年购买，自动续订周期为1年
        :param instance_charge_type: （混合云忽略该字段，使用cycleType替代）
        :param cycle_count: 该参数需要与cycleType一同使用 注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写；当cycleType= ondemand时，无需填写
        :param cycle_type: 订购周期类型 ，取值范围:[MONTH=按月,YEAR=按年,ondemand=按需订购]
        :param order_count: 购买数量，不传或者0时默认为1
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.az_name = az_name
        self.device_type = device_type
        self.instance_name = instance_name
        self.hostname = hostname
        self.image_uuid = image_uuid
        self.password = password
        self.system_volume_raid_uuid = system_volume_raid_uuid
        self.data_volume_raid_uuid = data_volume_raid_uuid
        self.vpc_id = vpc_id
        self.ext_ip = ext_ip
        self.ip_type = ip_type
        self.bandwidth = bandwidth
        self.public_ip = public_ip
        self.security_group_id = security_group_id
        self.disk_list = disk_list
        self.network_card_list = network_card_list
        self.user_data = user_data
        self.key_name = key_name
        self.auto_renew_status = auto_renew_status
        self.instance_charge_type = instance_charge_type
        self.cycle_count = cycle_count
        self.cycle_type = cycle_type
        self.order_count = order_count
        self.client_token = client_token
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区（4.0必填）
        """
        self.az_name = az_name

    def set_system_volume_raid_uuid(self, system_volume_raid_uuid):
        """
        :param system_volume_raid_uuid: 本地系统盘raid类型，如果有本地盘则必填 
        """
        self.system_volume_raid_uuid = system_volume_raid_uuid

    def set_data_volume_raid_uuid(self, data_volume_raid_uuid):
        """
        :param data_volume_raid_uuid: 本地数据盘raid类型，如果有本地盘则必填
        """
        self.data_volume_raid_uuid = data_volume_raid_uuid

    def set_ip_type(self, ip_type):
        """
        :param ip_type: 弹性IP版本 ，取值范围:[ipv4=v4地址,ipv6=v6地址]，默认值:ipv4，eip暂不知此ipv6，这里传值只支持传ipv4
        """
        self.ip_type = ip_type

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽 ，取值范围:[1~2000]，默认值:100----extIP 为1时需要
        """
        self.bandwidth = bandwidth

    def set_public_ip(self, public_ip):
        """
        :param public_ip: 弹性公网IP的id --extIP为2时需要
        """
        self.public_ip = public_ip

    def set_security_group_id(self, security_group_id):
        """
        :param security_group_id: 安全组ID，套餐smartNicExist为true可支持安全组---暂不支持
        """
        self.security_group_id = security_group_id

    def set_disk_list(self, disk_list):
        """
        :param disk_list: 云盘信息列表，套餐中supportCloud为true表示支持云盘  
        """
        self.disk_list = disk_list

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        """
        self.user_data = user_data

    def set_key_name(self, key_name):
        """
        :param key_name: 密钥对名称
        """
        self.key_name = key_name

    def set_auto_renew_status(self, auto_renew_status):
        """
        :param auto_renew_status: （混合云暂不支持）是否自动续订，取值范围： 0（不续费）， 1（自动续费）， 注：按月购买，自动续订周期为1个月；按年购买，自动续订周期为1年
        """
        self.auto_renew_status = auto_renew_status

    def set_instance_charge_type(self, instance_charge_type):
        """
        :param instance_charge_type: （混合云忽略该字段，使用cycleType替代）
        """
        self.instance_charge_type = instance_charge_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 该参数需要与cycleType一同使用 注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写；当cycleType= ondemand时，无需填写
        """
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 订购周期类型 ，取值范围:[MONTH=按月,YEAR=按年,ondemand=按需订购]
        """
        self.cycle_type = cycle_type

    def set_order_count(self, order_count):
        """
        :param order_count: 购买数量，不传或者0时默认为1
        """
        self.order_count = order_count

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
        if self.device_type is None:
            raise Exception("device_type can not None")
        if self.instance_name is None:
            raise Exception("instance_name can not None")
        if self.hostname is None:
            raise Exception("hostname can not None")
        if self.image_uuid is None:
            raise Exception("image_uuid can not None")
        if self.password is None:
            raise Exception("password can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")

