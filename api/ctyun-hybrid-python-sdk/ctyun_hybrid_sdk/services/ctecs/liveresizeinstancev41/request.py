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


class LiveResizeInstanceV41Request(CTYunRequest):
    """
    该接口提供云主机热变配功能，即开机状态实现变更规格   
    准备工作：   
      构造请求：在调用前需要了解如何构造请求，详情查看构造请求   
      认证鉴权：openapi请求需要进行加密调用，详细查看认证鉴权   
    注意事项：   
      确认当前云主机是否可进行热变配，您可以通过接口查询云主机支持的热变配规格信息获取当前云主机是否可以进行热变配，以及可以热变配规格信息   
       
    热变配当前支持规格和镜像信息为（不同资源池下的镜像和规格支持情况不同，以查询云主机支持热变配规格信息接口的返回值为准）：   
    支持的云主机镜像：   
      CentOS：CentOS 7.6 64位、CentOS 7.8 64位、CentOS 7.9 64位、CentOS 8.0 64位、CentOS 8.1 64位、CentOS 8.2 64位、CentOS 8.4 64位   
      CTyunOS：CTyunOS 2.0.1-21.06.4 64位、CTyunOS 3-23.01 64位   
      KylinOS：KylinOS V10 SP1 64位、KylinOS V10 SP2 64位   
      其他：openEuler 22.03 SP2 64位、UnionTechOS V20 1050u1e 64位   
       
    支持的云主机规格：   
      除二代机以外的规格且vcpu≥32   
       
    #### 接口约束   
    1. 只支持升级规格，且不支持跨代升配（例如，原本云主机规格为m6.large.8，不可以变配为m7.xlarge.8）   
    2. 对于存量的云主机（2023年12月31日以前创建的云主机），无法使用当前功能   
    3. 同代升配能否支持取决于numa拓扑，以及CPU和内存均不能变小且至少有一个变大。   
    4. 当前云主机处于开机状态   
    5. 云主机已挂载的云硬盘状态不能处于“镜像制作中”
    """

    def __init__(self, request_param):
        super(LiveResizeInstanceV41Request, self).__init__("/v4/ecs/live-resize", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
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


class LiveResizeInstanceV41RequestParam(object):

    def __init__(self, region_id, instance_id, flavor_id, ):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param flavor_id: 云主机规格ID
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.flavor_id = flavor_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")

