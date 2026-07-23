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


class CdaGatewayDeleteRequest(CTYunRequest):
    """
    入参示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"regionID"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"nm8",</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"gatewayName"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"d5hrh7wcbzgx1107testzz"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>   
       
    <span class="colour" style="color:rgb(0, 0, 0)">返回参数示例：</span>   
    <span class="colour" style="color:rgb(0, 0, 0)"></span>{   
        "returnObj": {   
            "data": null,   
            "errorMsg": null,   
            "result": "1"   
        },   
        "statusCode": 800   
    }<span class="colour" style="color:rgb(0, 0, 0)"></span>
    """

    def __init__(self, request_param):
        super(CdaGatewayDeleteRequest, self).__init__("/v4/cda/gateway/delete", "POST", "cda", "application/json")
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
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
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


class CdaGatewayDeleteRequestParam(object):

    def __init__(self, gateway_name, region_id=None):
        """
        :param region_id: 资源池id，非必填，无实际作用，以网关名称为主
        :param gateway_name: 专线网关名称
        """
        self.region_id = region_id
        self.gateway_name = gateway_name

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池id，非必填，无实际作用，以网关名称为主
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")

