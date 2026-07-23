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


class RebuildInstanceRequest(CTYunRequest):
    """
    该接口提供用户重装一台云主机功能，通过填写相应云主机ID、镜像ID，您可以调用[imageID](https://www.ctyun.cn/document/10026730/10040588)查看最新的天翼云具体资源池的镜像列表和密码对云主机进行重装。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    2. 云主机不能存在快照
    """

    def __init__(self, request_param):
        super(RebuildInstanceRequest, self).__init__("/v4/ecs/rebuild-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.user_data is not None:
            body_param["userData"] = self.parameters.user_data
        if self.parameters.instance_name is not None:
            body_param["instanceName"] = self.parameters.instance_name
        if self.parameters.monitor_service is not None:
            body_param["monitorService"] = self.parameters.monitor_service
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class RebuildInstanceRequestParam(object):

    def __init__(self, region_id, instance_id, password, image_id=None, user_data=None, instance_name=None, monitor_service=None, client_token=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机id
        :param image_id: 不填默认以原镜像进行重装
        :param password: 用户密码，满足以下规则： 长度在8～30个字符； 必须包含大写字母、小写字母、数字以及特殊符号中的三项； 特殊符号可选：()`~!@#$%^&*_-+=｜{}[]:;'<>,.?/\\且不能以斜线号 / 开头； 不能包含3个及以上连续字符； Linux镜像不能包含镜像用户名（root）、用户名的倒序（toor）、用户名大小写变化（如RoOt、rOot等）； Windows镜像不能包含镜像用户名（Administrator）、用户名大小写变化（adminiSTrator等）
        :param user_data: 用户自定义数据，需要以Base64方式编码，Base64编码后的长度限制为1-16384字符。注：非多可用区类型资源池暂不支持该参数
        :param instance_name: （私有云不支持）不可以使用已存在的云主机名称。不同操作系统下，云主机名称规则有差异。云主机名称，不可以使用已存在的云主机名称。不同操作系统下，云主机名称规则有差异。 Windows：长度为2-15个字符（当创建两台及两台以上的云主机时名称长度为2-10个字符），允许使用大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字； 其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2-59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        :param monitor_service: （私有云暂不支持）支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启）
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.image_id = image_id
        self.password = password
        self.user_data = user_data
        self.instance_name = instance_name
        self.monitor_service = monitor_service
        self.client_token = client_token

    def set_image_id(self, image_id):
        """
        :param image_id: 不填默认以原镜像进行重装
        """
        self.image_id = image_id

    def set_user_data(self, user_data):
        """
        :param user_data: 用户自定义数据，需要以Base64方式编码，Base64编码后的长度限制为1-16384字符。注：非多可用区类型资源池暂不支持该参数
        """
        self.user_data = user_data

    def set_instance_name(self, instance_name):
        """
        :param instance_name: （私有云不支持）不可以使用已存在的云主机名称。不同操作系统下，云主机名称规则有差异。云主机名称，不可以使用已存在的云主机名称。不同操作系统下，云主机名称规则有差异。 Windows：长度为2-15个字符（当创建两台及两台以上的云主机时名称长度为2-10个字符），允许使用大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能仅使用数字； 其他操作系统：长度为2-64字符（当创建两台及两台以上的云主机时名称长度为2-59个字符），允许使用点（.）分隔字符成多段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾，也不能仅使用数字。
        """
        self.instance_name = instance_name

    def set_monitor_service(self, monitor_service):
        """
        :param monitor_service: （私有云暂不支持）支持通过该参数指定云主机在创建后是否开启详细监控，取值范围： false（不开启）， true（开启）
        """
        self.monitor_service = monitor_service

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.password is None:
            raise Exception("password can not None")

