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


class GroupBindVdcOpenApiRequest(CTYunRequest):
    """
    ip地址组绑定vdc
    """

    def __init__(self, request_param):
        super(GroupBindVdcOpenApiRequest, self).__init__("/v4/eipPool/bindVdc", "PUT", "ctvpc", "application/json")
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
        if self.parameters.eip_address_group_id is not None:
            body_param["eipAddressGroupID"] = self.parameters.eip_address_group_id
        if self.parameters.vdc_ids is not None:
            body_param["vdcIDs"] = self.parameters.vdc_ids
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


class GroupBindVdcOpenApiRequestParam(object):

    def __init__(self, eip_address_group_id, vdc_ids, ):
        """
        :param eip_address_group_id: eip地址族id
        :param vdc_ids: 需要绑定的全量vdcID 注意:此参数为数组
        """
        self.eip_address_group_id = eip_address_group_id
        self.vdc_ids = vdc_ids

    def check_param(self):
        """
        the param required check
        """
        if self.eip_address_group_id is None:
            raise Exception("eip_address_group_id can not None")
        if self.vdc_ids is None:
            raise Exception("vdc_ids can not None")

