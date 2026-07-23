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


class ModifyCommandRequest(CTYunRequest):
    """
    调用此接口可以修改用户自己创建的云助手命令内容、命令参数等信息
    """

    def __init__(self, request_param):
        super(ModifyCommandRequest, self).__init__("/v4/cloud-assistant/modify-command", "POST", "ctecs", "application/json")
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
        if self.parameters.command_name is not None:
            body_param["commandName"] = self.parameters.command_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.command_type is not None:
            body_param["commandType"] = self.parameters.command_type
        if self.parameters.command_content is not None:
            body_param["commandContent"] = self.parameters.command_content
        if self.parameters.working_directory is not None:
            body_param["workingDirectory"] = self.parameters.working_directory
        if self.parameters.timeout is not None:
            body_param["timeout"] = self.parameters.timeout
        if self.parameters.enabled_parameter is not None:
            body_param["enabledParameter"] = self.parameters.enabled_parameter
        if self.parameters.default_parameter is not None:
            default_parameter = []
            if isinstance(self.parameters.default_parameter, list):
                for item in self.parameters.default_parameter:
                    if type(item) is dict:
                        default_parameter.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        default_parameter.append(item_dict_value)
            else:
                default_parameter.append(self.parameters.default_parameter.get_dic())
            body_param["defaultParameter"] = default_parameter
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


class DefaultParameter(object):

    def __init__(self, key, value, description=None):
        """
        :param key: 参数名，字符数上限64，可选范围a-z、A-Z、0-9、-和_，传多个key-value时key值不允许重复
        :param value: 参数值，最长24576个字符
        :param description: 参数描述
        """
        self.key = key
        self.value = value
        self.description = description
        self.check_param()

    def set_description(self, description):
        """
        :param description: 参数描述
        """
        self.description = description

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.value is not None:
            obj_dict["value"] = self.value
        if self.description is not None:
            obj_dict["description"] = self.description
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.key is None:
            raise Exception("key can not None")
        if self.value is None:
            raise Exception("value can not None")


class ModifyCommandRequestParam(object):

    def __init__(self, region_id, command_id, command_name=None, description=None, command_type=None, command_content=None, working_directory=None, timeout=None, enabled_parameter=None, default_parameter=None):
        """
        :param region_id: 资源池ID
        :param command_id: 命令ID
        :param command_name: 命令名称，长度不超过64个字符，仅支持中文、大小写字母、数字、横线(-)、下划线()和小数点(.)不允许重复
        :param description: 命令描述，长度不超过128个字符
        :param command_type: 命令类型，取值范围： Shell：适用于Linux云主机、物理机的Shell命令； Bat：适用于Windows云主机的Bat命令； PowerShell：适用于Windows云主机的PowerShell命令； Python：适用于Python命令
        :param command_content: 加密后的命令内容，base64编码之前长度不可超过24KB
        :param working_directory: 命令在实例中运行目录。Linux系统默认路径为 /tmp;Windows系统默认路径为C:/Windows/System32 说明：若在Windows系统云主机下执行Python脚本命令，需传Python安装全路径。最长128个字符，仅支持中文、大小写字母、数字、横线(-)、下划线(_)、小数点(.)、英文冒号(:)、斜杠(/)和反斜杠(\\\\) （需转义后）。
        :param timeout: 命令超时时间，默认值60秒，范围在10-86400秒
        :param enabled_parameter: 是否启用自定义参数，若传true，则必须传defaultParameter，若enabledParameter为false，则defaultParameter可不传，最多20个key-value
        :param default_parameter: 启用自定义参数功能时，自定义参数的默认取值，json 格式string数组 注意:此参数为数组
        """
        self.region_id = region_id
        self.command_id = command_id
        self.command_name = command_name
        self.description = description
        self.command_type = command_type
        self.command_content = command_content
        self.working_directory = working_directory
        self.timeout = timeout
        self.enabled_parameter = enabled_parameter
        self.default_parameter = default_parameter

    def set_command_name(self, command_name):
        """
        :param command_name: 命令名称，长度不超过64个字符，仅支持中文、大小写字母、数字、横线(-)、下划线()和小数点(.)不允许重复
        """
        self.command_name = command_name

    def set_description(self, description):
        """
        :param description: 命令描述，长度不超过128个字符
        """
        self.description = description

    def set_command_type(self, command_type):
        """
        :param command_type: 命令类型，取值范围： Shell：适用于Linux云主机、物理机的Shell命令； Bat：适用于Windows云主机的Bat命令； PowerShell：适用于Windows云主机的PowerShell命令； Python：适用于Python命令
        """
        self.command_type = command_type

    def set_command_content(self, command_content):
        """
        :param command_content: 加密后的命令内容，base64编码之前长度不可超过24KB
        """
        self.command_content = command_content

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

    def set_enabled_parameter(self, enabled_parameter):
        """
        :param enabled_parameter: 是否启用自定义参数，若传true，则必须传defaultParameter，若enabledParameter为false，则defaultParameter可不传，最多20个key-value
        """
        self.enabled_parameter = enabled_parameter

    def set_default_parameter(self, default_parameter):
        """
        :param default_parameter: 启用自定义参数功能时，自定义参数的默认取值，json 格式string数组
        """
        self.default_parameter = default_parameter

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.command_id is None:
            raise Exception("command_id can not None")

