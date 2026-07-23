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


class EcsCreateRequest(CTYunRequest):
    """
    支持创建一台按量付费或包年包月的云主机   
    注意：   
    1.系统盘参数syshd大小必须大于等于镜像的大小。   
    2.子网类型不能为裸机属子网。   
    3. 因对接方原因，instanceName允许重复   
    
    """

    def __init__(self, request_param):
        super(EcsCreateRequest, self).__init__("/v4/ecs/create", "POST", "ctecs", "application/json")
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
        if self.parameters.vm_name is not None:
            body_param["vmName"] = self.parameters.vm_name
        if self.parameters.display_name is not None:
            body_param["displayName"] = self.parameters.display_name
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
        if self.parameters.flavor_name is not None:
            body_param["flavorName"] = self.parameters.flavor_name
        if self.parameters.image_public is not None:
            body_param["imagePublic"] = self.parameters.image_public
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.syshd_type is not None:
            body_param["syshdType"] = self.parameters.syshd_type
        if self.parameters.syshd is not None:
            body_param["syshd"] = self.parameters.syshd
        if self.parameters.sys_volume_id is not None:
            body_param["sysVolumeID"] = self.parameters.sys_volume_id
        if self.parameters.dss_cluster_id is not None:
            body_param["dssClusterID"] = self.parameters.dss_cluster_id
        if self.parameters.dss_pool_id is not None:
            body_param["dssPoolID"] = self.parameters.dss_pool_id
        if self.parameters.pool_id is not None:
            body_param["poolID"] = self.parameters.pool_id
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
        if self.parameters.vpc is not None:
            body_param["vpc"] = self.parameters.vpc
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
        if self.parameters.ip_type is not None:
            body_param["ipType"] = self.parameters.ip_type
        if self.parameters.band_width is not None:
            body_param["bandWidth"] = self.parameters.band_width
        if self.parameters.ipv6_address is not None:
            body_param["ipv6Address"] = self.parameters.ipv6_address
        if self.parameters.public_ip is not None:
            body_param["publicIP"] = self.parameters.public_ip
        if self.parameters.affinity_group is not None:
            body_param["affinityGroup"] = self.parameters.affinity_group
        if self.parameters.key_pair_id is not None:
            body_param["keyPairID"] = self.parameters.key_pair_id
        if self.parameters.root_password is not None:
            body_param["rootPassword"] = self.parameters.root_password
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
        if self.parameters.dec_id is not None:
            body_param["decID"] = self.parameters.dec_id
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


class Disk(object):

    def __init__(self, title, type, size, disk_mode=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None):
        """
        :param disk_mode: （暂不支持，传参不生效）云硬盘属性，取值范围: [FCSAN、ISCSI、VBD]，默认值为VBD
        :param title: 磁盘名称 ，长度2~63,不支持中文
        :param type: 云硬盘类型，取值范围： SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        :param size: 磁盘容量大小单位为GiB，取值范围[10-32768]，单位GB
        :param dss_cluster_id: 专属集群ID
        :param dss_pool_id: 专属集群存储池ID
        :param pool_id: 非专属集群存储池ID
        """
        self.disk_mode = disk_mode
        self.title = title
        self.type = type
        self.size = size
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.check_param()

    def set_disk_mode(self, disk_mode):
        """
        :param disk_mode: （暂不支持，传参不生效）云硬盘属性，取值范围: [FCSAN、ISCSI、VBD]，默认值为VBD
        """
        self.disk_mode = disk_mode

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
        if self.title is None:
            raise Exception("title can not None")
        if self.type is None:
            raise Exception("type can not None")
        if self.size is None:
            raise Exception("size can not None")


class NetworkCard(object):

    def __init__(self, master, subnet_id, fixed_ip=None, title=None, mtu=None):
        """
        :param fixed_ip: 内网IPv4地址
        :param title: （v2暂不支持）长度2~32，支持拉丁字母、中文、数字、下划线、连字符，中文或英文字母开头，不能以http:或https:开头
        :param master: 是否主网卡，取值范围： true：主网卡， false：扩展网卡
        :param subnet_id: 子网id 
        :param mtu: 没传MTU默认值要是1500
        """
        self.fixed_ip = fixed_ip
        self.title = title
        self.master = master
        self.subnet_id = subnet_id
        self.mtu = mtu
        self.check_param()

    def set_fixed_ip(self, fixed_ip):
        """
        :param fixed_ip: 内网IPv4地址
        """
        self.fixed_ip = fixed_ip

    def set_title(self, title):
        """
        :param title: （v2暂不支持）长度2~32，支持拉丁字母、中文、数字、下划线、连字符，中文或英文字母开头，不能以http:或https:开头
        """
        self.title = title

    def set_mtu(self, mtu):
        """
        :param mtu: 没传MTU默认值要是1500
        """
        self.mtu = mtu

    def get_dic(self):
        obj_dict = dict()
        if self.fixed_ip is not None:
            obj_dict["fixedIP"] = self.fixed_ip
        if self.title is not None:
            obj_dict["title"] = self.title
        if self.master is not None:
            obj_dict["master"] = self.master
        if self.subnet_id is not None:
            obj_dict["subnetID"] = self.subnet_id
        if self.mtu is not None:
            obj_dict["mtu"] = self.mtu
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.master is None:
            raise Exception("master can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")


class EcsCreateRequestParam(object):

    def __init__(self, client_token, region_id, vm_name, display_name, vpc, network_card_list, ext_ip, az_name=None, flavor_id=None, flavor_name=None, image_public=None, image_id=None, syshd_type=None, syshd=None, sys_volume_id=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None, disk_list=None, on_demand=None, sec_group_list=None, ip_type=None, band_width=None, ipv6_address=None, public_ip=None, affinity_group=None, key_pair_id=None, root_password=None, cycle_count=None, cycle_type=None, auto_renew_status=None, user_data=None, project_id=None, dec_id=None, order_count=None):
        """
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时；（私有云为保证历史版本兼容性，允许不传）
        :param region_id: 资源池ID
        :param az_name: 4.0资源池必填，当多可用区时支持随机分配可用区，本字段填写random
        :param vm_name: 云主机名称，不同操作系统下，云主机名称规则有差异。 Windows：长度为2-15个字符（当创建两台及两台以上的云主机时名称长度为2-10个字符），允许使用大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字； 其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2-59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param display_name: 长度为2-63字符
        :param flavor_id: 注：同一规格名称在不同资源池不同可用区的规格ID是不同的，调用前需确认规格ID是否归属当前资源池，多可用区资源池确认是否归属当前可用区
        :param flavor_name: 注：当创建云主机随机分配可用区时，规格名称为必填项，规格ID无效。当采用确定可用区时，规格ID和规格名称两者均可使用，必填其中一个，当两个都填写以规格ID为准。
        :param image_public: （暂不支持，传参不生效）镜像类型，取值范围: 0：私有镜像， 1：公有镜像， 2：共享镜像， 3：安全镜像， 4：甄选镜像
        :param image_id: sysVolumeID为空时必填
        :param syshd_type: sysVolumeID为空时必填，取值范围: SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        :param syshd: sysVolumeID为空时必填，取值范围[40-32768]
        :param sys_volume_id: 填写该参数，syshdType、syshd不可填，不填写该参数，syshdType、syshd都必填
        :param dss_cluster_id: 系统盘指定专属集群
        :param dss_pool_id: 系统盘指定专属集群存储池
        :param pool_id: 系统盘指定非专属集群存储池
        :param disk_list: 最大支持20块数据盘 注意:此参数为数组
        :param vpc: 虚拟私有云ID 
        :param on_demand: sysVolumeID为空时必填，取值范围：   
         false：按周期，   
         true：按需，   
         按周期创建云主机需要同时指定cycleCount和cycleType参数   
         sysVolumeID不为空时，云主机计费类型和已有云硬盘保持一致
        :param sec_group_list: 安全组ID列表，默认使用默认安全组，无默认安全组情况下请填写该参数（共享vpc场景下必传） 注意:此参数为数组
        :param network_card_list: 最大支持7张网卡 注意:此参数为数组
        :param ext_ip: 是否使用弹性公网IP，取值范围: 0：不使用， 1：自动分配，自动分配需指定带宽大小， 2：使用已有   
         注1：当extIP=1时，bandWidth必填   
         当extIP=2时，必须传publicIP
        :param ip_type: 弹性IP版本，取值范围: ipv4：v4地址， ipv6：v6地址， 默认选择ipv4
        :param band_width: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        :param ipv6_address: pv6地址的ID（多可用区类资源池暂不支持）	
        :param public_ip: 弹性公网IP的ID
        :param affinity_group: 云主机亲和组ID 
        :param key_pair_id: 密钥对ID 
        :param root_password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年，sysVolumeID不为空时该参数无效
        :param cycle_type: （按周期必传）表示订购周期类型，取值范围： MONTH：按月， YEAR：按年， 最长订购周期为5年；   
         sysVolumeID不为空时该参数无效
        :param auto_renew_status: （暂不支持，传参不生效）是否自动续订 ，取值范围： 0：不续费， 1：自动续费， 按月购买：自动续订周期为1个月， 按年购买：自动续订周期为1年
        :param user_data: 用户自定义数据,需要以Base64方式编码,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param project_id: 企业项目ID
        :param dec_id: 计算专属云ID
        :param order_count: 订购数量，不传默认是1
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.vm_name = vm_name
        self.display_name = display_name
        self.flavor_id = flavor_id
        self.flavor_name = flavor_name
        self.image_public = image_public
        self.image_id = image_id
        self.syshd_type = syshd_type
        self.syshd = syshd
        self.sys_volume_id = sys_volume_id
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.disk_list = disk_list
        self.vpc = vpc
        self.on_demand = on_demand
        self.sec_group_list = sec_group_list
        self.network_card_list = network_card_list
        self.ext_ip = ext_ip
        self.ip_type = ip_type
        self.band_width = band_width
        self.ipv6_address = ipv6_address
        self.public_ip = public_ip
        self.affinity_group = affinity_group
        self.key_pair_id = key_pair_id
        self.root_password = root_password
        self.cycle_count = cycle_count
        self.cycle_type = cycle_type
        self.auto_renew_status = auto_renew_status
        self.user_data = user_data
        self.project_id = project_id
        self.dec_id = dec_id
        self.order_count = order_count

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

    def set_image_public(self, image_public):
        """
        :param image_public: （暂不支持，传参不生效）镜像类型，取值范围: 0：私有镜像， 1：公有镜像， 2：共享镜像， 3：安全镜像， 4：甄选镜像
        """
        self.image_public = image_public

    def set_image_id(self, image_id):
        """
        :param image_id: sysVolumeID为空时必填
        """
        self.image_id = image_id

    def set_syshd_type(self, syshd_type):
        """
        :param syshd_type: sysVolumeID为空时必填，取值范围: SATA：普通IO， SAS：高IO， SSD：超高IO， SSD-genric：通用型SSD， FAST-SSD：极速型SSD
        """
        self.syshd_type = syshd_type

    def set_syshd(self, syshd):
        """
        :param syshd: sysVolumeID为空时必填，取值范围[40-32768]
        """
        self.syshd = syshd

    def set_sys_volume_id(self, sys_volume_id):
        """
        :param sys_volume_id: 填写该参数，syshdType、syshd不可填，不填写该参数，syshdType、syshd都必填
        """
        self.sys_volume_id = sys_volume_id

    def set_dss_cluster_id(self, dss_cluster_id):
        """
        :param dss_cluster_id: 系统盘指定专属集群
        """
        self.dss_cluster_id = dss_cluster_id

    def set_dss_pool_id(self, dss_pool_id):
        """
        :param dss_pool_id: 系统盘指定专属集群存储池
        """
        self.dss_pool_id = dss_pool_id

    def set_pool_id(self, pool_id):
        """
        :param pool_id: 系统盘指定非专属集群存储池
        """
        self.pool_id = pool_id

    def set_disk_list(self, disk_list):
        """
        :param disk_list: 最大支持20块数据盘
        """
        self.disk_list = disk_list

    def set_on_demand(self, on_demand):
        """
        :param on_demand: sysVolumeID为空时必填，取值范围：   
         false：按周期，   
         true：按需，   
         按周期创建云主机需要同时指定cycleCount和cycleType参数   
         sysVolumeID不为空时，云主机计费类型和已有云硬盘保持一致
        """
        self.on_demand = on_demand

    def set_sec_group_list(self, sec_group_list):
        """
        :param sec_group_list: 安全组ID列表，默认使用默认安全组，无默认安全组情况下请填写该参数（共享vpc场景下必传）
        """
        self.sec_group_list = sec_group_list

    def set_ip_type(self, ip_type):
        """
        :param ip_type: 弹性IP版本，取值范围: ipv4：v4地址， ipv6：v6地址， 默认选择ipv4
        """
        self.ip_type = ip_type

    def set_band_width(self, band_width):
        """
        :param band_width: 带宽大小单位为Mbit/s，取值范围:[1~2000]
        """
        self.band_width = band_width

    def set_ipv6_address(self, ipv6_address):
        """
        :param ipv6_address: pv6地址的ID（多可用区类资源池暂不支持）	
        """
        self.ipv6_address = ipv6_address

    def set_public_ip(self, public_ip):
        """
        :param public_ip: 弹性公网IP的ID
        """
        self.public_ip = public_ip

    def set_affinity_group(self, affinity_group):
        """
        :param affinity_group: 云主机亲和组ID 
        """
        self.affinity_group = affinity_group

    def set_key_pair_id(self, key_pair_id):
        """
        :param key_pair_id: 密钥对ID 
        """
        self.key_pair_id = key_pair_id

    def set_root_password(self, root_password):
        """
        :param root_password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等
        """
        self.root_password = root_password

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年，sysVolumeID不为空时该参数无效
        """
        self.cycle_count = cycle_count

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: （按周期必传）表示订购周期类型，取值范围： MONTH：按月， YEAR：按年， 最长订购周期为5年；   
         sysVolumeID不为空时该参数无效
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

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 计算专属云ID
        """
        self.dec_id = dec_id

    def set_order_count(self, order_count):
        """
        :param order_count: 订购数量，不传默认是1
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
        if self.vm_name is None:
            raise Exception("vm_name can not None")
        if self.display_name is None:
            raise Exception("display_name can not None")
        if self.vpc is None:
            raise Exception("vpc can not None")
        if self.network_card_list is None:
            raise Exception("network_card_list can not None")
        if self.ext_ip is None:
            raise Exception("ext_ip can not None")

