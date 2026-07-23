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


class SendFileRequest(CTYunRequest):
    """
    调用此接口可以上传文件到弹性云主机、物理机内部   
    说明：仅支持批量上传文件到弹性云主机或物理机内部，不支持混合上传，仅支持Linux系统   
       
    接口约束   
    1）弹性云主机、物理机必须处于运行状态；   
    2）弹性云主机、物理机中必须安装天翼云云助手且服务处于运行状态。
    """

    def __init__(self, request_param):
        super(SendFileRequest, self).__init__("/v4/cloud-assistant/send-file", "POST", "ctecs", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.instance_ids is not None:
            body_param["instanceIDs"] = self.parameters.instance_ids
        if self.parameters.file_name is not None:
            body_param["fileName"] = self.parameters.file_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.file_content is not None:
            body_param["fileContent"] = self.parameters.file_content
        if self.parameters.target_directory is not None:
            body_param["targetDirectory"] = self.parameters.target_directory
        if self.parameters.file_owner is not None:
            body_param["fileOwner"] = self.parameters.file_owner
        if self.parameters.file_group is not None:
            body_param["fileGroup"] = self.parameters.file_group
        if self.parameters.file_mode is not None:
            body_param["fileMode"] = self.parameters.file_mode
        if self.parameters.overwrite is not None:
            body_param["overwrite"] = self.parameters.overwrite
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


class SendFileRequestParam(object):

    def __init__(self, region_id, instance_ids, file_name, file_content, target_directory, project_id=None, description=None, file_owner=None, file_group=None, file_mode=None, overwrite=None):
        """
        :param region_id: 资源池ID
        :param project_id: 混合云企业项目id，不传在默认企业项目下查询实例
        :param instance_ids: 待下发文件的弹性云主机、物理机ID列表, 使用 , 分割
        :param file_name: 文件名称，长度2~63个字符，仅支持中文、大小写字母、数字、横线(-)、下划线(_)和小数点(.)
        :param description: 描述，长度不超过512个字符
        :param file_content: 加密后的文件内容，base64编码之前长度不可超过24KB
        :param target_directory: 下发文件的目标路径，最长128个字符，仅支持中文、大小写字母、数字、横线(-)、下划线(_)、小数点(.)、英文冒号(:)、斜杠(/)和反斜杠(\\\\) （需转义后）。
        :param file_owner: 文件所属用户，只针对linux实例，默认root，最长32个字符
        :param file_group: 文件用户组，只针对linux实例，默认root，最长32个字符
        :param file_mode: 文件权限，只针对linux实例，默认0644，最长255个字符
        :param overwrite: 是否覆盖，如果目标路径下同名文件已经存在，true：覆盖，false：不覆盖。默认false
        """
        self.region_id = region_id
        self.project_id = project_id
        self.instance_ids = instance_ids
        self.file_name = file_name
        self.description = description
        self.file_content = file_content
        self.target_directory = target_directory
        self.file_owner = file_owner
        self.file_group = file_group
        self.file_mode = file_mode
        self.overwrite = overwrite

    def set_project_id(self, project_id):
        """
        :param project_id: 混合云企业项目id，不传在默认企业项目下查询实例
        """
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述，长度不超过512个字符
        """
        self.description = description

    def set_file_owner(self, file_owner):
        """
        :param file_owner: 文件所属用户，只针对linux实例，默认root，最长32个字符
        """
        self.file_owner = file_owner

    def set_file_group(self, file_group):
        """
        :param file_group: 文件用户组，只针对linux实例，默认root，最长32个字符
        """
        self.file_group = file_group

    def set_file_mode(self, file_mode):
        """
        :param file_mode: 文件权限，只针对linux实例，默认0644，最长255个字符
        """
        self.file_mode = file_mode

    def set_overwrite(self, overwrite):
        """
        :param overwrite: 是否覆盖，如果目标路径下同名文件已经存在，true：覆盖，false：不覆盖。默认false
        """
        self.overwrite = overwrite

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_ids is None:
            raise Exception("instance_ids can not None")
        if self.file_name is None:
            raise Exception("file_name can not None")
        if self.file_content is None:
            raise Exception("file_content can not None")
        if self.target_directory is None:
            raise Exception("target_directory can not None")

