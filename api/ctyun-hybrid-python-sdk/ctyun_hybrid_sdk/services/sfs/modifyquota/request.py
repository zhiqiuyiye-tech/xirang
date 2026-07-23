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


class ModifyQuotaRequest(CTYunRequest):
    """
    quotaSize：配额设置如10MB 10GB形式，长度至少为3位，最后两位为单位；quotaSize不能设置为0（即：取消限制）
    """

    def __init__(self, request_param):
        super(ModifyQuotaRequest, self).__init__("/v4/sfs/modify-quota", "POST", "sfs", "application/json")
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
        if self.parameters.uid is not None:
            body_param["UID"] = self.parameters.uid
        if self.parameters.quota_sub_dir_name is not None:
            body_param["quotaSubDirName"] = self.parameters.quota_sub_dir_name
        if self.parameters.quota_size is not None:
            body_param["quotaSize"] = self.parameters.quota_size
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


class ModifyQuotaRequestParam(object):

    def __init__(self, region_id, uid, quota_sub_dir_name, quota_size, ):
        """
        :param region_id: 资源池ID
        :param uid: 兼容了云管ID和底层UUID
        :param quota_sub_dir_name: 长度为1-20字符 支持中文、英文（大小写）、数字、下划线（_）、连字符（-）,不支持特殊字符开头 不支持连续连字符（--）
        :param quota_size: 单位支持MB/GB/TB，格式如100MB，容量需为整数型
        """
        self.region_id = region_id
        self.uid = uid
        self.quota_sub_dir_name = quota_sub_dir_name
        self.quota_size = quota_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.uid is None:
            raise Exception("uid can not None")
        if self.quota_sub_dir_name is None:
            raise Exception("quota_sub_dir_name can not None")
        if self.quota_size is None:
            raise Exception("quota_size can not None")

