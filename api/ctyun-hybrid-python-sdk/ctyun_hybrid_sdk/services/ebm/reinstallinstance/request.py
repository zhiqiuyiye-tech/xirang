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


class ReinstallInstanceRequest(CTYunRequest):
    """
    物理机重装系统,**注意**： 混合云redoRaid不支持
    """

    def __init__(self, request_param):
        super(ReinstallInstanceRequest, self).__init__("/v4/ebm/rebuild", "POST", "ebm", "application/json")
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
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.host_name is not None:
            body_param["hostName"] = self.parameters.host_name
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.image_uuid is not None:
            body_param["imageUUID"] = self.parameters.image_uuid
        if self.parameters.system_volume_raid_uuid is not None:
            body_param["systemVolumeRaidUUID"] = self.parameters.system_volume_raid_uuid
        if self.parameters.data_volume_raid_uuid is not None:
            body_param["dataVolumeRaidUUID"] = self.parameters.data_volume_raid_uuid
        if self.parameters.redo_raid is not None:
            body_param["redoRaid"] = self.parameters.redo_raid
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
        if self.parameters.key_name is not None:
            body_param["keyName"] = self.parameters.key_name
        if self.parameters.mtu is not None:
            body_param["mtu"] = self.parameters.mtu
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


class ReinstallInstanceRequestParam(object):

    def __init__(self, region_id, instance_uuid, host_name, password, image_uuid, az_name=None, system_volume_raid_uuid=None, data_volume_raid_uuid=None, redo_raid=None, user_data=None, key_name=None, mtu=None):
        """
        :param region_id: 区域ID
        :param az_name: 可用区
        :param instance_uuid: 实例uuid
        :param host_name: hostname，linux系统2到63位长度；windows系统2-15位长度；允许使用大小写字母、数字、连字符'-'，必须以字母开头（大小写均可），不能连续使用'-'，'-'不能用于结尾，不能仅使用数字；
        :param password: 密码 -长度8到30位，必须包含大小写字母和（数字或者特殊字符,并且^不可用），且不能包含两位以上连续数字，如012、789等
        :param image_uuid: 镜像UUID
        :param system_volume_raid_uuid: 系统盘raid类型，如果有本地系统盘则必填
        :param data_volume_raid_uuid: 数据盘raid类型，如果有本地数据盘则必填
        :param redo_raid: 是否重新做raid，如果有本地盘必填--暂未提供（未与公有云对齐）
        :param user_data: 用户自定义数据,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        :param key_name: 密钥对名词
        :param mtu: 设置网卡MTU：包括主网卡和扩展网卡，取值范围[1500,8000]   
         目前只支持ctyunos，centos，kylinos
        """
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid = instance_uuid
        self.host_name = host_name
        self.password = password
        self.image_uuid = image_uuid
        self.system_volume_raid_uuid = system_volume_raid_uuid
        self.data_volume_raid_uuid = data_volume_raid_uuid
        self.redo_raid = redo_raid
        self.user_data = user_data
        self.key_name = key_name
        self.mtu = mtu

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_system_volume_raid_uuid(self, system_volume_raid_uuid):
        """
        :param system_volume_raid_uuid: 系统盘raid类型，如果有本地系统盘则必填
        """
        self.system_volume_raid_uuid = system_volume_raid_uuid

    def set_data_volume_raid_uuid(self, data_volume_raid_uuid):
        """
        :param data_volume_raid_uuid: 数据盘raid类型，如果有本地数据盘则必填
        """
        self.data_volume_raid_uuid = data_volume_raid_uuid

    def set_redo_raid(self, redo_raid):
        """
        :param redo_raid: 是否重新做raid，如果有本地盘必填--暂未提供（未与公有云对齐）
        """
        self.redo_raid = redo_raid

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据,需要以Base64方式编码,Base64编码后的长度限制为1-16384字符
        """
        self.user_data = user_data

    def set_key_name(self, key_name):
        """
        :param key_name: 密钥对名词
        """
        self.key_name = key_name

    def set_mtu(self, mtu):
        """
        :param mtu: 设置网卡MTU：包括主网卡和扩展网卡，取值范围[1500,8000]   
         目前只支持ctyunos，centos，kylinos
        """
        self.mtu = mtu

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.host_name is None:
            raise Exception("host_name can not None")
        if self.password is None:
            raise Exception("password can not None")
        if self.image_uuid is None:
            raise Exception("image_uuid can not None")

