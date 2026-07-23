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


class SwitchAzStatusRequest(CTYunRequest):
    """
    切换可用区状态
    """

    def __init__(self, request_param):
        super(SwitchAzStatusRequest, self).__init__("/v1/azs/switch-status", "PUT", "hybridregion", "application/json")
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
        if self.parameters.azs is not None:
            azs = []
            if isinstance(self.parameters.azs, list):
                for item in self.parameters.azs:
                    if type(item) is dict:
                        azs.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        azs.append(item_dict_value)
            else:
                azs.append(self.parameters.azs.get_dic())
            body_param["azs"] = azs
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


class Az(object):

    def __init__(self, az_id, status, ):
        """
        :param az_id: 
        :param status: 
        """
        self.az_id = az_id
        self.status = status
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.az_id is not None:
            obj_dict["azID"] = self.az_id
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.az_id is None:
            raise Exception("az_id can not None")
        if self.status is None:
            raise Exception("status can not None")


class SwitchAzStatusRequestParam(object):

    def __init__(self, azs, ):
        """
        :param azs: 支持批量修改，azID 不存在则跳过 注意:此参数为数组
        """
        self.azs = azs

    def check_param(self):
        """
        the param required check
        """
        if self.azs is None:
            raise Exception("azs can not None")

