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


class V4PaasEcsCloneInstanceRequest(CTYunRequest):
    """
    克隆云主机(工单)
    """

    def __init__(self, request_param):
        super(V4PaasEcsCloneInstanceRequest, self).__init__("/v4/paas/ecs/clone-instance", "POST", "ct", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
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
        if self.parameters.sec_group_list is not None:
            body_param["secGroupList"] = self.parameters.sec_group_list
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
        :param nic_name: 暂不支持
        :param fixed_ip: 内网IPv4地址
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
        :param nic_name: 暂不支持
        """
        self.nic_name = nic_name

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
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


class V4PaasEcsCloneInstanceRequestParam(object):

    def __init__(self, client_token, region_id, instance_id, instance_name, display_name, vpc_id, network_card_list, ext_ip, channel_info=None, sec_group_list=None, ip_version=None, bandwidth=None, eip_id=None, affinity_group_id=None, key_pair_id=None, user_password=None, user_data=None, project_id=None):
        """
        :param channel_info: 渠道侧信息
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param instance_id: 被克隆云主机ID
        :param instance_name: Windows：长度为2~15个字符，允许使用大小写字母、数字或连字符（-）。不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字；<br />其他操作系统：长度为2-64字符，允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾
        :param display_name: 云主机显示名称，长度为2-63字符
        :param vpc_id: 虚拟私有云ID
        :param network_card_list: 网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围:<br />0：不使用，<br />1：自动分配，<br />2：使用已有
        :param sec_group_list: 安全组id列表 注意:此参数为数组
        :param ip_version: 取值范围:<br />ipv4：v4地址，<br />ipv6：v6地址(目前仅支持ipv4)
        :param bandwidth: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        :param eip_id: 弹性公网IP的ID（orderCount>1时不可用）
        :param affinity_group_id: 云主机组ID
        :param key_pair_id: 密钥对ID
        :param user_password: 满足以下规则：<br />长度在8～30个字符;<br />必须包含大写字母、小写字母、数字以及特殊符号中的三项;<br />特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头
        :param user_data: 需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param project_id: 默认值为"0"
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.display_name = display_name
        self.vpc_id = vpc_id
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.sec_group_list = sec_group_list
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.eip_id = eip_id
        self.affinity_group_id = affinity_group_id
        self.key_pair_id = key_pair_id
        self.user_password = user_password
        self.user_data = user_data
        self.project_id = project_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息
        """
        self.channel_info = channel_info

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

    def set_project_id(self, project_id):
        """
        :param project_id: 默认值为"0"
        """
        self.project_id = project_id

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
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

