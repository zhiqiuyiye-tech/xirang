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


class RenameSFSRequest(CTYunRequest):
    """
    文件系统重命名
    """

    def __init__(self, request_param):
        super(RenameSFSRequest, self).__init__("/v4/sfs/rename-sfs", "POST", "sfs", "application/json")
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
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.sfs_name is not None:
            body_param["sfsName"] = self.parameters.sfs_name
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


class RenameSFSRequestParam(object):

    def __init__(self, region_id, sfs_uid, sfs_name, ):
        """
        :param region_id: 资源池ID
        :param sfs_uid: 兼容云管ID和底层UID
        :param sfs_name: 不与现有名称重复；命名规则：长度2~63字符，支持使用字母、数字、中划线(-)，只能以字母开头、以数字或字母结尾
        """
        self.region_id = region_id
        self.sfs_uid = sfs_uid
        self.sfs_name = sfs_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")
        if self.sfs_name is None:
            raise Exception("sfs_name can not None")

