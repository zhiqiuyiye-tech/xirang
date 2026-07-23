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


class ConfigCreateRequest(CTYunRequest):
    """
    创建一个弹性伸缩配置
    """

    def __init__(self, request_param):
        super(ConfigCreateRequest, self).__init__("/v4/scaling/config-create", "POST", "scaling", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.band_width is not None:
            body_param["bandWidth"] = self.parameters.band_width
        if self.parameters.use_floatings is not None:
            body_param["useFloatings"] = self.parameters.use_floatings
        if self.parameters.billing_mode is not None:
            body_param["billingMode"] = self.parameters.billing_mode
        if self.parameters.login_mode is not None:
            body_param["loginMode"] = self.parameters.login_mode
        if self.parameters.username is not None:
            body_param["username"] = self.parameters.username
        if self.parameters.spec_name is not None:
            body_param["specName"] = self.parameters.spec_name
        if self.parameters.volumes is not None:
            volumes = []
            if isinstance(self.parameters.volumes, list):
                for item in self.parameters.volumes:
                    if type(item) is dict:
                        volumes.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        volumes.append(item_dict_value)
            else:
                volumes.append(self.parameters.volumes.get_dic())
            body_param["volumes"] = volumes
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.key_pair_id is not None:
            body_param["keyPairID"] = self.parameters.key_pair_id
        if self.parameters.security_group_id_list is not None:
            body_param["securityGroupIDList"] = self.parameters.security_group_id_list
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
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


class Volume(object):

    def __init__(self, volume_type, volume_size, flag, dispatch_type=None, dss_cluster_id=None, dss_pool_id=None, pool_id=None):
        """
        :param volume_type: 磁盘类型： SATA/SAS/SSD/SATA-KUNPENG/SATA-HAIGUANG/SAS-KUNPENG/SAS-HAIGUANG/SSD-genric。不同资源池可配置的volumeType有差异，详细请参考云硬盘
        :param volume_size: 磁盘大小,取值范围[10-32768]，单位GB
        :param flag: 本参数表示标志。<br>取值范围：<br>1：系统盘。<br>2：数据盘。<br>系统盘限制为1块。
        :param dispatch_type: 存储池分配类型: 0-自动分配，1-指定分配
        :param dss_cluster_id: 存储专属集群ID（不传表示不指定专属集群）
        :param dss_pool_id: 专属集群存储池ID（与 dssClusterID 配套使用）
        :param pool_id: 非专属集群存储池ID（不传表示由底层调度）
        """
        self.volume_type = volume_type
        self.volume_size = volume_size
        self.flag = flag
        self.dispatch_type = dispatch_type
        self.dss_cluster_id = dss_cluster_id
        self.dss_pool_id = dss_pool_id
        self.pool_id = pool_id
        self.check_param()

    def set_dispatch_type(self, dispatch_type):
        """
        :param dispatch_type: 存储池分配类型: 0-自动分配，1-指定分配
        """
        self.dispatch_type = dispatch_type

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

    def get_dic(self):
        obj_dict = dict()
        if self.volume_type is not None:
            obj_dict["volumeType"] = self.volume_type
        if self.volume_size is not None:
            obj_dict["volumeSize"] = self.volume_size
        if self.flag is not None:
            obj_dict["flag"] = self.flag
        if self.dispatch_type is not None:
            obj_dict["dispatchType"] = self.dispatch_type
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
        if self.volume_type is None:
            raise Exception("volume_type can not None")
        if self.volume_size is None:
            raise Exception("volume_size can not None")
        if self.flag is None:
            raise Exception("flag can not None")


class ConfigCreateRequestParam(object):

    def __init__(self, region_id, name, image_id, use_floatings, login_mode, spec_name, volumes, az_name=None, band_width=None, billing_mode=None, username=None, password=None, key_pair_id=None, security_group_id_list=None, user_data=None):
        """
        :param region_id: 资源池id
        :param az_name: 可用区ID，4.0必传
        :param name: 伸缩配置名称（长度最大15，最小2；不能重复）
        :param image_id: 镜像id
        :param band_width: 带宽 单位：Mbps,billingMode 为1时，必填    范围1-3000(公有云支持，混合云不支持，忽略)
        :param use_floatings: 是否使用弹性IP 不使用（1） 自动分配（2）;int 16;
        :param billing_mode: 计费方式：按带宽计费（1），  按流量计费（2）  useFloatings为2时（混合云目前不支持忽略）;int 16;
        :param login_mode: 登陆方式 密码（1） 秘钥对（2）;int 16;
        :param username: 用户名 ,  loginMode为1时，必填;长度最大 64
        :param spec_name: 规格名称；长度最大 64
        :param volumes: 磁盘类型和大小列表，元素为Volume | [{"volumeType":"SATA", "volumeSize":40,"flag":1}] ,至少得有一个系统盘    注意:此参数为数组
        :param password: 密码  ,     loginMode为1时，必填；（长度在8～30个字符，必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\）
        :param key_pair_id: 秘钥对ID ,       loginMode为2时，必填
        :param security_group_id_list: 安全组ID，3.0必传 注意:此参数为数组
        :param user_data: 用户自定义数据,需要以Base64方式编码  
        """
        self.region_id = region_id
        self.az_name = az_name
        self.name = name
        self.image_id = image_id
        self.band_width = band_width
        self.use_floatings = use_floatings
        self.billing_mode = billing_mode
        self.login_mode = login_mode
        self.username = username
        self.spec_name = spec_name
        self.volumes = volumes
        self.password = password
        self.key_pair_id = key_pair_id
        self.security_group_id_list = security_group_id_list
        self.user_data = user_data

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区ID，4.0必传
        """
        self.az_name = az_name

    def set_band_width(self, band_width):
        """
        :param band_width: 带宽 单位：Mbps,billingMode 为1时，必填    范围1-3000(公有云支持，混合云不支持，忽略)
        """
        self.band_width = band_width

    def set_billing_mode(self, billing_mode):
        """
        :param billing_mode: 计费方式：按带宽计费（1），  按流量计费（2）  useFloatings为2时（混合云目前不支持忽略）;int 16;
        """
        self.billing_mode = billing_mode

    def set_username(self, username):
        """
        :param username: 用户名 ,  loginMode为1时，必填;长度最大 64
        """
        self.username = username

    def set_password(self, password):
        """
        :param password: 密码  ,     loginMode为1时，必填；（长度在8～30个字符，必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\）
        """
        self.password = password

    def set_key_pair_id(self, key_pair_id):
        """
        :param key_pair_id: 秘钥对ID ,       loginMode为2时，必填
        """
        self.key_pair_id = key_pair_id

    def set_security_group_id_list(self, security_group_id_list):
        """
        :param security_group_id_list: 安全组ID，3.0必传
        """
        self.security_group_id_list = security_group_id_list

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据,需要以Base64方式编码  
        """
        self.user_data = user_data

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")
        if self.use_floatings is None:
            raise Exception("use_floatings can not None")
        if self.login_mode is None:
            raise Exception("login_mode can not None")
        if self.spec_name is None:
            raise Exception("spec_name can not None")
        if self.volumes is None:
            raise Exception("volumes can not None")

