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


class SfsCreateQueryPricesRequest(CTYunRequest):
    """
    未与公有云对齐：   
    公有云使用volumeType确定弹性文件类型进行询价；【该字段目前不起作用，请使用sfsType和sfsProtocol】   
    V2通过sfsType[文件系统类型]和sfsProtocol[协议类型]确定一个销售品后进行询价；
    """

    def __init__(self, request_param):
        super(SfsCreateQueryPricesRequest, self).__init__("/v4/sfs/new-order/query-prices", "POST", "sfs", "application/json")
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
        if self.parameters.order_num is not None:
            body_param["orderNum"] = self.parameters.order_num
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.cycle_cnt is not None:
            body_param["cycleCnt"] = self.parameters.cycle_cnt
        if self.parameters.volume_type is not None:
            body_param["volumeType"] = self.parameters.volume_type
        if self.parameters.sfs_type is not None:
            body_param["sfsType"] = self.parameters.sfs_type
        if self.parameters.sfs_protocol is not None:
            body_param["sfsProtocol"] = self.parameters.sfs_protocol
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


class SfsCreateQueryPricesRequestParam(object):

    def __init__(self, region_id, order_num, cycle_type, sfs_size, cycle_cnt, sfs_type, sfs_protocol, volume_type=None):
        """
        :param region_id: 资源池ID
        :param order_num: 最大订购数:50
        :param cycle_type: month/year
        :param sfs_size: 100-327680GB
        :param cycle_cnt: 最大订购月数:60；最大订购年数：5
        :param volume_type: 标准型hdd, 性能型nvme, 标准专属型hdd_e
        :param sfs_type: capacity-标准型,performance-性能型
        :param sfs_protocol: nfs/cifs/nfs,cifs
        """
        self.region_id = region_id
        self.order_num = order_num
        self.cycle_type = cycle_type
        self.sfs_size = sfs_size
        self.cycle_cnt = cycle_cnt
        self.volume_type = volume_type
        self.sfs_type = sfs_type
        self.sfs_protocol = sfs_protocol

    def set_volume_type(self, volume_type):
        """
        :param volume_type: 标准型hdd, 性能型nvme, 标准专属型hdd_e
        """
        self.volume_type = volume_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.order_num is None:
            raise Exception("order_num can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.cycle_cnt is None:
            raise Exception("cycle_cnt can not None")
        if self.sfs_type is None:
            raise Exception("sfs_type can not None")
        if self.sfs_protocol is None:
            raise Exception("sfs_protocol can not None")

