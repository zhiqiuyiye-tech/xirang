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


class GetEcsFlavorsRequest(CTYunRequest):
    """
    查询资源池虚机规格信息 请使用/v4/ecs/flavor/list
    """

    def __init__(self, request_param):
        super(GetEcsFlavorsRequest, self).__init__("/v4/common/get-ecs-flavors", "GET", "ctecs", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.series is not None:
            query_param["series"] = self.parameters.series
        if self.parameters.dec_id is not None:
            query_param["decID"] = self.parameters.dec_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetEcsFlavorsRequestParam(object):

    def __init__(self, region_id, az_name=None, series=None, dec_id=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称(单AZ资源池可不传，多AZ资源池不传返回所有az的规格)
        :param series: 规格系列
        :param dec_id: 专属云ID，支持过滤专属云支持的规格
        """
        self.region_id = region_id
        self.az_name = az_name
        self.series = series
        self.dec_id = dec_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(单AZ资源池可不传，多AZ资源池不传返回所有az的规格)
        """
        self.az_name = az_name

    def set_series(self, series):
        """
        :param series: 规格系列
        """
        self.series = series

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 专属云ID，支持过滤专属云支持的规格
        """
        self.dec_id = dec_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

