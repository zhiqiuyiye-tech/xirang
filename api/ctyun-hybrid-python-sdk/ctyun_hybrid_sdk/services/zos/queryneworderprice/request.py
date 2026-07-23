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


class QueryNewOrderPriceRequest(CTYunRequest):
    """
    ZOS资源包询价
    """

    def __init__(self, request_param):
        super(QueryNewOrderPriceRequest, self).__init__("/v4/oss/new-order/query-price", "POST", "zos", "application/json")
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
        if self.parameters.pkg_type is not None:
            body_param["pkgType"] = self.parameters.pkg_type
        if self.parameters.pkg_spec_type is not None:
            body_param["pkgSpecType"] = self.parameters.pkg_spec_type
        if self.parameters.pkg_spec is not None:
            body_param["pkgSpec"] = self.parameters.pkg_spec
        if self.parameters.cycle_cnt is not None:
            body_param["cycleCnt"] = self.parameters.cycle_cnt
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.order_num is not None:
            body_param["orderNum"] = self.parameters.order_num
        if self.parameters.storage_class is not None:
            body_param["storageClass"] = self.parameters.storage_class
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


class QueryNewOrderPriceRequestParam(object):

    def __init__(self, region_id, pkg_type, pkg_spec_type, pkg_spec, cycle_cnt, cycle_type, order_num, storage_class, ):
        """
        :param region_id: 区域 ID
        :param pkg_type: 可选参数如下：①zosSize（ZOS存储空间包）、②zosMzSize（ZOS多AZ存储空间包，仅支持STANDARD（标准存储）和STANDARD_IA（低频存储））、③zosBytesSend（ZOS流出流量资源包)、④zosRequest（ZOS请求次数包）、⑤zosRetrievalFlow（ZOS数据取回流量包，仅支持storageClass为STANDARD_IA（低频存储）和 GLACIER（归档存储））、⑥zosRetrievalFrequency（ZOS数据取回次数包，仅支持storageClass为STANDARD_IA（低频存储）和 GLACIER（归档存储））
        :param pkg_spec_type: （公有云参数，私有云暂不支持，入参是什么都为自定义规格）可选参数如下：①fixed（固定规格）②defined（自定义规格）
        :param pkg_spec: 单位：GB。当pkgType选择为请求次数包zosRequest和数据取回次数包zosRetrievalFrequency时，单位为：万次。范围限制1-9999
        :param cycle_cnt: 最大订购月数：36，最大订购年数：3
        :param cycle_type: 可选参数如下：①month（按月订购）、②year（按年订购）
        :param order_num: 范围限制1-50
        :param storage_class: 可选参数如下：①STANDARD（标准存储）、②STANDARD_IA（低频存储）、③GLACIER（归档存储）
        """
        self.region_id = region_id
        self.pkg_type = pkg_type
        self.pkg_spec_type = pkg_spec_type
        self.pkg_spec = pkg_spec
        self.cycle_cnt = cycle_cnt
        self.cycle_type = cycle_type
        self.order_num = order_num
        self.storage_class = storage_class

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.pkg_type is None:
            raise Exception("pkg_type can not None")
        if self.pkg_spec_type is None:
            raise Exception("pkg_spec_type can not None")
        if self.pkg_spec is None:
            raise Exception("pkg_spec can not None")
        if self.cycle_cnt is None:
            raise Exception("cycle_cnt can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.order_num is None:
            raise Exception("order_num can not None")
        if self.storage_class is None:
            raise Exception("storage_class can not None")

