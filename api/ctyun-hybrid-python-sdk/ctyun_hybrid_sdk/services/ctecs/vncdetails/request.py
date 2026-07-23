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


class VncDetailsRequest(CTYunRequest):
    """
    查询一台云主机的Web管理终端地址。   
    #### 调用VNC OpenAPI接口获取Token   
    * 调用接口获取Token信息， token 信息就是websocket协议访问地址。   
    1. 使用noVNC等client进行访问，以noVNC为例，具体操作步骤如下：   
       
      -  本地启动noVNC服务，打开vnc页面；   
      -  点击左侧`⚙`，打开`高级`-`WebSocket`，在`主机`中，填写协议的地址   
      -  点击右侧连接按钮，即可访问   
       
    2.若要直接使用返回信息进行vnc远程登录，需保证调用方所在的浏览器中可访问到云管系统登录地址，并使用拼接后的完整地址访问：   
       
    完整访问地址为：wss://云管系统登录地址ip:端口+该接口返回的所有内容；   
       
    协议使用wss/ws取决于是云管访问是https还是http；   
       
    拼接的完整地址示例：wss://10.246.81.250:40117/osnmvnc1/ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE3Njc3NzgsImlhdCI6MTc0MTc2NDE3OCwidXNlcl9pZCI6IjYwNGFiOTdmYjg0NDYxMWU5MzViOWI3OTYxZmIyMTc5IiwicHJvamVjdF9pZCI6IjEzNTE2MWMyYTZkNzkwYzg0YzczYTQ3MDI0MjJlZGNmIiwiZG9tYWluX2lkIjoiZGVmYXVsdCIsInJvbGVzIjpbInVzZXIiXSwiY29uc3VtZXJfaWQiOiIiLCJpc3N1ZWRfYXQiOiIyMDI1LTAzLTEyVDA3OjIyOjU4LjAwMDAwMFoiLCJleHBpcmVfYXQiOiIyMDI1LTAzLTEyVDA4OjIyOjU4LjAwMDAwMFoiLCJNZXRob2QiOlsicGFzc3dvcmQiXX0.fdqxwwXDEAVSXUbu2m3D06hMwqK49mABYAXSKGcxCPQ&instanceId=6cf210e3-7f20-84f7-4eb3-a3b6399f42a3   
       
    接口调通之后会返回VNC的登录页面。   
       
    若调用websocket接口返回403，可在调用接口时headers里增加如下参数：   
    Pragma: no-cache   
    Cache-Control: no-cache   
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36   
    Origin: https://云管系统登录地址ip:端口   
    Accept-Encoding: gzip, deflate, br, zstd   
    
    """

    def __init__(self, request_param):
        super(VncDetailsRequest, self).__init__("/v4/ecs/vnc/details", "GET", "ctecs", "")
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
        if self.parameters.instance_id is not None:
            query_param["instanceID"] = self.parameters.instance_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class VncDetailsRequestParam(object):

    def __init__(self, region_id, instance_id, ):
        """
        :param region_id: 资源池信息
        :param instance_id: 实例ID
        """
        self.region_id = region_id
        self.instance_id = instance_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")

