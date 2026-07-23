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


class QueryNewOrderPriceV42Request(CTYunRequest):
    """
    购买云产品时询价接口，支持云主机、云硬盘、弹性公网IP产品的包年/包月或按量订单的询价功能
    """

    def __init__(self, request_param):
        super(QueryNewOrderPriceV42Request, self).__init__("/v4/order/new-query-price", "POST", "common", "application/json")
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
        if self.parameters.az_id is not None:
            body_param["azID"] = self.parameters.az_id
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.count is not None:
            body_param["count"] = self.parameters.count
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.flavor_name is not None:
            body_param["flavorName"] = self.parameters.flavor_name
        if self.parameters.image_uuid is not None:
            body_param["imageUUID"] = self.parameters.image_uuid
        if self.parameters.sys_disk_type is not None:
            body_param["sysDiskType"] = self.parameters.sys_disk_type
        if self.parameters.sys_disk_size is not None:
            body_param["sysDiskSize"] = self.parameters.sys_disk_size
        if self.parameters.disks is not None:
            disks = []
            if isinstance(self.parameters.disks, list):
                for item in self.parameters.disks:
                    if type(item) is dict:
                        disks.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        disks.append(item_dict_value)
            else:
                disks.append(self.parameters.disks.get_dic())
            body_param["disks"] = disks
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.disk_type is not None:
            body_param["diskType"] = self.parameters.disk_type
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
        if self.parameters.disk_mode is not None:
            body_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.nat_type is not None:
            body_param["natType"] = self.parameters.nat_type
        if self.parameters.ip_pool_bandwidth is not None:
            body_param["ipPoolBandwidth"] = self.parameters.ip_pool_bandwidth
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

    def __init__(self, disk_type, disk_size, ):
        """
        :param disk_type: 磁盘类型
        :param disk_size: 磁盘大小
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


class QueryNewOrderPriceV42RequestParam(object):

    def __init__(self, region_id, resource_type, count, az_id=None, on_demand=None, cycle_type=None, cycle_count=None, flavor_name=None, image_uuid=None, sys_disk_type=None, sys_disk_size=None, disks=None, bandwidth=None, disk_type=None, disk_size=None, disk_mode=None, nat_type=None, ip_pool_bandwidth=None):
        """
        :param region_id: 资源池ID
        :param az_id: [私有云]可用区ID(私有云新增，多AZ资源池如果未传azID，默认第一个)
        :param resource_type: 资源类型(VM/EBS/IP/IP_POOL/NAT)
        :param count: 订购数量
        :param on_demand: 是否按需资源，true 按需 / false 包周期
        :param cycle_type: 订购周期类型(MONTH/YEAR)，当onDemand为false时为必填
        :param cycle_count: 订购周期大小，当onDemand为false时为必填
        :param flavor_name: 云主机规格，当resourceType为VM时必填
        :param image_uuid: 云主机镜像UUID，当resourceType为VM时必填
        :param sys_disk_type: 云主机系统盘类型，当resourceType为VM时必填
        :param sys_disk_size: 云主机系统盘大小，当resourceType为VM时必填
        :param disks: 数据盘信息，当resourceType为VM选填，订购云主机时如果成套订购数据盘时需要该字段 注意:此参数为数组
        :param bandwidth: 带宽大小，当resourceType为IP时必填；当resourceType为VM时，如果成套订购弹性公网IP时需要该字段
        :param disk_type: 磁盘类型，当resourceType为EBS时必填
        :param disk_size: 磁盘大小，当resourceType为EBS时必填
        :param disk_mode: 磁盘模式(VBD/ISCSI/FCSAN)，当resourceType为EBS时必填，resourceType为VM时默认为VBD
        :param nat_type: nat规格(small/medium/large/xlarge)，当resourceType为NAT时必填
        :param ip_pool_bandwidth: 共享带宽大小，当resourceType为IP_POOL时必填
        """
        self.region_id = region_id
        self.az_id = az_id
        self.resource_type = resource_type
        self.count = count
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.flavor_name = flavor_name
        self.image_uuid = image_uuid
        self.sys_disk_type = sys_disk_type
        self.sys_disk_size = sys_disk_size
        self.disks = disks
        self.bandwidth = bandwidth
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.disk_mode = disk_mode
        self.nat_type = nat_type
        self.ip_pool_bandwidth = ip_pool_bandwidth

    def set_az_id(self, az_id):
        """
        :param az_id: [私有云]可用区ID(私有云新增，多AZ资源池如果未传azID，默认第一个)
        """
        self.az_id = az_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: 是否按需资源，true 按需 / false 包周期
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 订购周期类型(MONTH/YEAR)，当onDemand为false时为必填
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购周期大小，当onDemand为false时为必填
        """
        self.cycle_count = cycle_count

    def set_flavor_name(self, flavor_name):
        """
        :param flavor_name: 云主机规格，当resourceType为VM时必填
        """
        self.flavor_name = flavor_name

    def set_image_uuid(self, image_uuid):
        """
        :param image_uuid: 云主机镜像UUID，当resourceType为VM时必填
        """
        self.image_uuid = image_uuid

    def set_sys_disk_type(self, sys_disk_type):
        """
        :param sys_disk_type: 云主机系统盘类型，当resourceType为VM时必填
        """
        self.sys_disk_type = sys_disk_type

    def set_sys_disk_size(self, sys_disk_size):
        """
        :param sys_disk_size: 云主机系统盘大小，当resourceType为VM时必填
        """
        self.sys_disk_size = sys_disk_size

    def set_disks(self, disks):
        """
        :param disks: 数据盘信息，当resourceType为VM选填，订购云主机时如果成套订购数据盘时需要该字段
        """
        self.disks = disks

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽大小，当resourceType为IP时必填；当resourceType为VM时，如果成套订购弹性公网IP时需要该字段
        """
        self.bandwidth = bandwidth

    def set_disk_type(self, disk_type):
        """
        :param disk_type: 磁盘类型，当resourceType为EBS时必填
        """
        self.disk_type = disk_type

    def set_disk_size(self, disk_size):
        """
        :param disk_size: 磁盘大小，当resourceType为EBS时必填
        """
        self.disk_size = disk_size

    def set_disk_mode(self, disk_mode):
        """
        :param disk_mode: 磁盘模式(VBD/ISCSI/FCSAN)，当resourceType为EBS时必填，resourceType为VM时默认为VBD
        """
        self.disk_mode = disk_mode

    def set_nat_type(self, nat_type):
        """
        :param nat_type: nat规格(small/medium/large/xlarge)，当resourceType为NAT时必填
        """
        self.nat_type = nat_type

    def set_ip_pool_bandwidth(self, ip_pool_bandwidth):
        """
        :param ip_pool_bandwidth: 共享带宽大小，当resourceType为IP_POOL时必填
        """
        self.ip_pool_bandwidth = ip_pool_bandwidth

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.count is None:
            raise Exception("count can not None")

