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


class V4EcsCloneInstanceRequest(CTYunRequest):
    """
    1. 被克隆云主机存在，且云主机处于运行中（running）或关机（stopped）状态   
    2. 目前不支持预付费账户创建按需付费类型云主机   
    3. 计费模式选择包年包月计费方式时，需要填写订购周期类型与订购时长   
    4. 挂载网卡时，子网与虚拟私有云存在对应关系，确保子网属于当前虚拟私有云   
    5. 云主机已挂载的云硬盘状态不能处于“镜像制作中”
    """

    def __init__(self, request_param):
        super(V4EcsCloneInstanceRequest, self).__init__("/v4/ecs/clone-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
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
        :param nic_name: 暂不支持
        :param fixed_ip: 内网IPv4地址
        """
        self.subnet_id = subnet_id
        self.is_master = is_master
        self.nic_name = nic_name
        self.fixed_ip = fixed_ip
        self.check_param()

    def set_nic_name(self, nic_name):
        """
        :param nic_name: 暂不支持
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
        :param label_key: 长度限制1-32字符，注：同一台云主机绑定多个标签时，标签键不可重复
        :param label_value: 长度限制1-32字符
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


class V4EcsCloneInstanceRequestParam(object):

    def __init__(self, client_token, region_id, instance_id, instance_name, display_name, vpc_id, on_demand, network_card_list, ext_ip, sec_group_list=None, ip_version=None, bandwidth=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, cycle_count=None, cycle_type=None, auto_renew_status=None, user_data=None, project_id=None, label_list=None, monitor_service=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param instance_id: 被克隆云主机ID
        :param instance_name: Windows：长度为2~15个字符，允许使用大小写字母、数字或连字符（-）。不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字；<br />其他操作系统：长度为2-64字符，允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾
        :param display_name: 云主机显示名称，长度为2-63字符
        :param vpc_id: 虚拟私有云ID
        :param on_demand: 取值范围：false（按周期）， true（按需）
        :param sec_group_list: 安全组id列表 注意:此参数为数组
        :param network_card_list: 网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围:<br />0：不使用，<br />1：自动分配，<br />2：使用已有   
         注：当extIP=2时，必须传eipID
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址(目前仅支持ipv4)
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]   
         注：extIP取值1时，bandwidth生效且必填
        :param eip_id: 弹性公网IP的ID
        :param affinity_group_id: 云主机组ID
        :param key_pair_id: 密钥对ID
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        :param cycle_count: 该参数需要与cycleType一同使用 注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写；按量付费（即onDemand为true）时，无需填写该参数（填写无效）
        :param cycle_type: 取值范围： MONTH：按月， YEAR：按年。注：cycleType与cycleCount一起填写；按量付费（即onDemand为true）时，无需填写该参数（填写无效）
        :param auto_renew_status: 取值范围： 0（不续费）， 1（自动续费）， 注：按月购买，自动续订周期为1个月；按年购买，自动续订周期为1年   
         ps：暂不支持
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param project_id: 默认值为"0"
        :param label_list: 注：暂不支持 注意:此参数为数组
        :param monitor_service: 支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启） 若指定该参数为true或不指定该参数，云主机内默认开启最新详细监控服务。 若指定该参数为false，默认不开启最新监控服务，而使用与原云主机相同的监控服务。
        """
        self.client_token = client_token
        self.region_id = region_id
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.display_name = display_name
        self.vpc_id = vpc_id
        self.on_demand = on_demand
        self.sec_group_list = sec_group_list
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.eip_id = eip_id
        self.affinity_group_id = affinity_group_id
        self.key_pair_id = key_pair_id
        self.user_password = user_password
        self.cycle_count = cycle_count
        self.cycle_type = cycle_type
        self.auto_renew_status = auto_renew_status
        self.user_data = user_data
        self.project_id = project_id
        self.label_list = label_list
        self.monitor_service = monitor_service

    def set_sec_group_list(self, sec_group_list):
        """
        :param sec_group_list: 安全组id列表
        """
        self.sec_group_list = sec_group_list

    def set_ip_version(self, ip_version):
        """
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址(目前仅支持ipv4)
        """
        self.ip_version = ip_version

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]   
         注：extIP取值1时，bandwidth生效且必填
        """
        self.bandwidth = bandwidth

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID
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
        :param cycle_count: 该参数需要与cycleType一同使用 注：最长订购周期为60个月（5年）；cycleType与cycleCount一起填写；按量付费（即onDemand为true）时，无需填写该参数（填写无效）
        """
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 取值范围： MONTH：按月， YEAR：按年。注：cycleType与cycleCount一起填写；按量付费（即onDemand为true）时，无需填写该参数（填写无效）
        """
        self.cycle_type = cycle_type

    def set_auto_renew_status(self, auto_renew_status):
        """
        :param auto_renew_status: 取值范围： 0（不续费）， 1（自动续费）， 注：按月购买，自动续订周期为1个月；按年购买，自动续订周期为1年   
         ps：暂不支持
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

    def set_label_list(self, label_list):
        """
        :param label_list: 注：暂不支持
        """
        self.label_list = label_list

    def set_monitor_service(self, monitor_service):
        """
        :param monitor_service: 支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启） 若指定该参数为true或不指定该参数，云主机内默认开启最新详细监控服务。 若指定该参数为false，默认不开启最新监控服务，而使用与原云主机相同的监控服务。
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
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.instance_name is None:
            raise Exception("instance_name can not None")
        if self.display_name is None:
            raise Exception("display_name can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.on_demand is None:
            raise Exception("on_demand can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

