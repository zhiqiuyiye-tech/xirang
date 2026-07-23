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


class IaasGetVdcQuotaRequest(CTYunRequest):
    """
    VDC配额和已用配额查询   
    备注：   
    1. 补充返回参数中id的说明：V2没有数字ID属性，目前是根据UUID，将uuid按照’-‘分隔，并且取前两个数据，组成的16进制字符串，转换成int64生成的。即，e334a588-260e-43dc-aa29-887a8e616328 转换成 e334a588260e， 然后将e334a588260e转成int64，请勿拿此id执行查询操作   
    2. vdc开启配额后才返回配额信息   
    
    """

    def __init__(self, request_param):
        super(IaasGetVdcQuotaRequest, self).__init__("/v4/region/getVdcQuota", "GET", "common", "")
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
        if self.parameters.vdc_id is not None:
            query_param["vdcId"] = self.parameters.vdc_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IaasGetVdcQuotaRequestParam(object):

    def __init__(self, region_id, vdc_id, ):
        """
        :param region_id: 资源池ID   
         
        :param vdc_id: 组织id
        """
        self.region_id = region_id
        self.vdc_id = vdc_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vdc_id is None:
            raise Exception("vdc_id can not None")

