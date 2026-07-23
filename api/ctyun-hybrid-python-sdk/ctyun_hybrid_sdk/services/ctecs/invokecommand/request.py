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


class InvokeCommandRequest(CTYunRequest):
    """
    调用此接口为一台或多台弹性云主机或物理机触发一条云助手命令   
    说明：仅支持批量为弹性云主机或物理机触发云助手命令，不支持混合触发   
       
    接口约束   
    1.弹性云主机、物理机必须处于运行状态   
    2.弹性云主机、物理机中必须安装天翼云云助手且服务处于运行状态
    """

    def __init__(self, request_param):
        super(InvokeCommandRequest, self).__init__("/v4/cloud-assistant/invoke-command", "POST", "ctecs", "application/json")
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
        if self.parameters.command_id is not None:
            body_param["commandID"] = self.parameters.command_id
        if self.parameters.working_directory is not None:
            body_param["workingDirectory"] = self.parameters.working_directory
        if self.parameters.timeout is not None:
            body_param["timeout"] = self.parameters.timeout
        if self.parameters.parameter is not None:
            body_param["parameter"] = self.parameters.parameter
        if self.parameters.instance_ids is not None:
            body_param["instanceIDs"] = self.parameters.instance_ids
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


class InvokeCommandRequestParam(object):

    def __init__(self, region_id, command_id, instance_ids, working_directory=None, timeout=None, parameter=None):
        """
        :param region_id: 资源池ID
        :param command_id: 命令ID
        :param working_directory: 命令在实例中运行目录。Linux系统默认路径为 /tmp;Windows系统默认路径为C:/Windows/System32 说明：若在Windows系统云主机下执行Python脚本命令，需传Python安装全路径。最长128个字符，仅支持中文、大小写字母、数字、横线(-)、下划线(_)、小数点(.)、英文冒号(:)、斜杠(/)和反斜杠(\\\\) （需转义后）。
        :param timeout: 命令超时时间，默认值60秒，范围在10-86400秒
        :param parameter: 动态键值对，Map of String,自定义参数，说明：key仅支持大小写字母(A-a)、数字(0-9)、横线(-)和下划线(_)，key和value均只支持string
        :param instance_ids: 待执行命令的弹性云主机、物理机ID列表, 使用英文 , 分割（当前仅支持同时下发弹性云主机ID或同时下发物理机ID，不支持混合下发）
        """
        self.region_id = region_id
        self.command_id = command_id
        self.working_directory = working_directory
        self.timeout = timeout
        self.parameter = parameter
        self.instance_ids = instance_ids

    def set_working_directory(self, working_directory):
        """
        :param working_directory: 命令在实例中运行目录。Linux系统默认路径为 /tmp;Windows系统默认路径为C:/Windows/System32 说明：若在Windows系统云主机下执行Python脚本命令，需传Python安装全路径。最长128个字符，仅支持中文、大小写字母、数字、横线(-)、下划线(_)、小数点(.)、英文冒号(:)、斜杠(/)和反斜杠(\\\\) （需转义后）。
        """
        self.working_directory = working_directory

    def set_timeout(self, timeout):
        """
        :param timeout: 命令超时时间，默认值60秒，范围在10-86400秒
        """
        self.timeout = timeout

    def set_parameter(self, parameter):
        """
        :param parameter: 动态键值对，Map of String,自定义参数，说明：key仅支持大小写字母(A-a)、数字(0-9)、横线(-)和下划线(_)，key和value均只支持string
        """
        self.parameter = parameter

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.command_id is None:
            raise Exception("command_id can not None")
        if self.instance_ids is None:
            raise Exception("instance_ids can not None")

