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


class PutBucketVersioningRequest(CTYunRequest):
    """
    开启合规保留的桶无法关闭桶版本控制
    """

    def __init__(self, request_param):
        super(PutBucketVersioningRequest, self).__init__("/v4/oss/put-bucket-versioning", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.versioning_configuration is not None:
            if type(self.parameters.versioning_configuration) is dict:
                versioning_configuration_dict_value = self.parameters.versioning_configuration
            else:
                versioning_configuration_dict_value = self.parameters.versioning_configuration.get_dic()
            body_param["versioningConfiguration"] = versioning_configuration_dict_value
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


class VersioningConfiguration(object):

    def __init__(self, status, ):
        """
        :param status: 存储空间的版本状态，值是 Enabled 或 Suspended
        """
        self.status = status
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")


class PutBucketVersioningRequestParam(object):

    def __init__(self, region_id, bucket, versioning_configuration, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param versioning_configuration: 版本信息
        """
        self.region_id = region_id
        self.bucket = bucket
        self.versioning_configuration = versioning_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.versioning_configuration is None:
            raise Exception("versioning_configuration can not None")

