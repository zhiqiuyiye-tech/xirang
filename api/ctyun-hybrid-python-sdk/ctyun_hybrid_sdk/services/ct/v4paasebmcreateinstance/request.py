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


class V4PaasEbmCreateInstanceRequest(CTYunRequest):
    """
    创建物理机（工单）
    """

    def __init__(self, request_param):
        super(V4PaasEbmCreateInstanceRequest, self).__init__("/v4/paas/ebm/create-instance", "POST", "ct", "application/json")
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
        if self.parameters.hostname is not None:
            body_param["hostname"] = self.parameters.hostname
        if self.parameters.device_type is not None:
            body_param["deviceType"] = self.parameters.device_type
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
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.ext_ip is not None:
            body_param["extIP"] = self.parameters.ext_ip
        if self.parameters.ip_type is not None:
            body_param["ipType"] = self.parameters.ip_type
        if self.parameters.band_width is not None:
            body_param["bandWidth"] = self.parameters.band_width
        if self.parameters.public_ip is not None:
            body_param["publicIP"] = self.parameters.public_ip
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
        if self.parameters.order_count is not None:
            body_param["orderCount"] = self.parameters.order_count
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

    def __init__(self, paas_resource_id, paas_account_id, master_order_id, tags=None, metas=None):
        """
        :param paas_resource_id: 
        :param paas_account_id: 
        :param master_order_id: 
        :param tags: 不支持标签
        :param metas: 元数据中key的字符串长度必须小于257
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas
        self.check_param()

    def set_tags(self, tags):
        """
        :param tags: 不支持标签
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 元数据中key的字符串长度必须小于257
        """
        self.metas = metas

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.tags is not None:
            if type(self.tags) is dict:
                obj_dict["tags"] = self.tags
            else:
                obj_dict["tags"] = self.tags.get_dic()
        if self.metas is not None:
            if type(self.metas) is dict:
                obj_dict["metas"] = self.metas
            else:
                obj_dict["metas"] = self.metas.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")
        if self.paas_account_id is None:
            raise Exception("paas_account_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")


class Tags(object):

    def __init__(self, ebm_attr, ):
        """
        :param ebm_attr: 
        """
        self.ebm_attr = ebm_attr
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.ebm_attr is not None:
            obj_dict["ebm_attr"] = self.ebm_attr
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.ebm_attr is None:
            raise Exception("ebm_attr can not None")


class Metas(object):

    def __init__(self, ebm_attr, ):
        """
        :param ebm_attr: 
        """
        self.ebm_attr = ebm_attr
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.ebm_attr is not None:
            obj_dict["ebm_attr"] = self.ebm_attr
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.ebm_attr is None:
            raise Exception("ebm_attr can not None")


class Disk(object):

    def __init__(self, disk_type, type, size, disk_mode=None, title=None):
        """
        :param disk_mode: 磁盘属性(VBD)
        :param title: 长度2~64,不支持中文
        :param disk_type: system,data,套餐中cloudBoot为true表示支持云盘系统盘
        :param type: 取值范围:[SAS=SAS盘,SATA=SATA盘,SSD-genric=SSD-genric盘,SSD=SSD盘]
        :param size: 磁盘容量, 5-2000GB, 磁盘类型为system的磁盘容量最小为100GB
        """
        self.disk_mode = disk_mode
        self.title = title
        self.disk_type = disk_type
        self.type = type
        self.size = size
        self.check_param()

    def set_disk_mode(self, disk_mode):
        """
        :param disk_mode: 磁盘属性(VBD)
        """
        self.disk_mode = disk_mode

    def set_title(self, title):
        """
        :param title: 长度2~64,不支持中文
        """
        self.title = title

    def get_dic(self):
        obj_dict = dict()
        if self.disk_mode is not None:
            obj_dict["diskMode"] = self.disk_mode
        if self.title is not None:
            obj_dict["title"] = self.title
        if self.disk_type is not None:
            obj_dict["diskType"] = self.disk_type
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.size is not None:
            obj_dict["size"] = self.size
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

    def __init__(self, master, subnet_id, title=None, fixed_ip=None, shared_vpc_id=None):
        """
        :param title: 网卡名称, 传递的话长度2~64, 不支持中文
        :param fixed_ip: 内网IPv4地址
        :param master: 是否主节点(True代表主节点)
        :param subnet_id: 子网id
        :param shared_vpc_id: 如果是共享VPC，需传递
        """
        self.title = title
        self.fixed_ip = fixed_ip
        self.master = master
        self.subnet_id = subnet_id
        self.shared_vpc_id = shared_vpc_id
        self.check_param()

    def set_title(self, title):
        """
        :param title: 网卡名称, 传递的话长度2~64, 不支持中文
        """
        self.title = title

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
        """
        self.fixed_ip = fixed_ip

    def set_shared_vpc_id(self, shared_vpc_id):
        """
        :param shared_vpc_id: 如果是共享VPC，需传递
        """
        self.shared_vpc_id = shared_vpc_id

    def get_dic(self):
        obj_dict = dict()
        if self.title is not None:
            obj_dict["title"] = self.title
        if self.fixed_ip is not None:
            obj_dict["fixedIP"] = self.fixed_ip
        if self.master is not None:
            obj_dict["master"] = self.master
        if self.subnet_id is not None:
            obj_dict["subnetID"] = self.subnet_id
        if self.shared_vpc_id is not None:
            obj_dict["sharedVpcID"] = self.shared_vpc_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.master is None:
            raise Exception("master can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")


class V4PaasEbmCreateInstanceRequestParam(object):

    def __init__(self, channel_info, client_token, region_id, instance_name, hostname, device_type, image_uuid, password, vpc_id, ext_ip, network_card_list, order_count, az_name=None, system_volume_raid_uuid=None, data_volume_raid_uuid=None, security_group_id=None, ip_type=None, band_width=None, public_ip=None, disk_list=None, project_id=None):
        """
        :param channel_info: 混合云历史版本非必填
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param az_name: 可用区名称，如果是4.0资源池，必须提供可用区名称
        :param instance_name: 物理机名称，长度为2-31位
        :param hostname: 主机名：长度6到64位，可以为字母数字和中划线，首字符不能为中划线和数字，不能以中划线结尾
        :param device_type: 物理机套餐类型
        :param image_uuid: 物理机镜像id
        :param password: 密码 -长度8到30位，必须包含大小写字母和（数字或者特殊字符,并且^不可用），且不能包含两位以上连续数字，如012、789等
        :param system_volume_raid_uuid: 如果有本地系统盘则必填
        :param data_volume_raid_uuid: 如果有本地数据盘则必填
        :param vpc_id: 主网卡网络ID
        :param security_group_id: 套餐smartNicExist为true可支持安全组
        :param ext_ip: 取值范围:[1=自动分配,0=不使用,2=使用已有]
        :param ip_type: 取值范围:[ipv4=v4地址]，默认值:ipv4
        :param band_width: 取值范围:[1~2000]，默认值:100
        :param public_ip: 弹性公网IP的id
        :param disk_list: 套餐中supportCloud为true表示支持云盘 注意:此参数为数组
        :param network_card_list: 网卡 注意:此参数为数组
        :param order_count: 购买数量
        :param project_id: 企业项目ID
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.instance_name = instance_name
        self.hostname = hostname
        self.device_type = device_type
        self.image_uuid = image_uuid
        self.password = password
        self.system_volume_raid_uuid = system_volume_raid_uuid
        self.data_volume_raid_uuid = data_volume_raid_uuid
        self.vpc_id = vpc_id
        self.security_group_id = security_group_id
        self.ext_ip = ext_ip
        self.ip_type = ip_type
        self.band_width = band_width
        self.public_ip = public_ip
        self.disk_list = disk_list
        self.network_card_list = network_card_list
        self.order_count = order_count
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，如果是4.0资源池，必须提供可用区名称
        """
        self.az_name = az_name

    def set_system_volume_raid_uuid(self, system_volume_raid_uuid):
        """
        :param system_volume_raid_uuid: 如果有本地系统盘则必填
        """
        self.system_volume_raid_uuid = system_volume_raid_uuid

    def set_data_volume_raid_uuid(self, data_volume_raid_uuid):
        """
        :param data_volume_raid_uuid: 如果有本地数据盘则必填
        """
        self.data_volume_raid_uuid = data_volume_raid_uuid

    def set_security_group_id(self, security_group_id):
        """
        :param security_group_id: 套餐smartNicExist为true可支持安全组
        """
        self.security_group_id = security_group_id

    def set_ip_type(self, ip_type):
        """
        :param ip_type: 取值范围:[ipv4=v4地址]，默认值:ipv4
        """
        self.ip_type = ip_type

    def set_band_width(self, band_width):
        """
        :param band_width: 取值范围:[1~2000]，默认值:100
        """
        self.band_width = band_width

    def set_public_ip(self, public_ip):
        """
        :param public_ip: 弹性公网IP的id
        """
        self.public_ip = public_ip

    def set_disk_list(self, disk_list):
        """
        :param disk_list: 套餐中supportCloud为true表示支持云盘
        """
        self.disk_list = disk_list

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.channel_info is None:
            raise Exception("channel_info can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_name is None:
            raise Exception("instance_name can not None")
        if self.hostname is None:
            raise Exception("hostname can not None")
        if self.device_type is None:
            raise Exception("device_type can not None")
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
        if self.order_count is None:
            raise Exception("order_count can not None")

