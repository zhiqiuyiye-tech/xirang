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


class PutBucketEncryptionRequest(CTYunRequest):
    """
    设置存储空间默认加密配置
    """

    def __init__(self, request_param):
        super(PutBucketEncryptionRequest, self).__init__("/v4/oss/put-bucket-encryption", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.server_side_encryption_configuration is not None:
            if type(self.parameters.server_side_encryption_configuration) is dict:
                server_side_encryption_configuration_dict_value = self.parameters.server_side_encryption_configuration
            else:
                server_side_encryption_configuration_dict_value = self.parameters.server_side_encryption_configuration.get_dic()
            body_param["serverSideEncryptionConfiguration"] = server_side_encryption_configuration_dict_value
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


class ServerSideEncryptionConfiguration(object):

    def __init__(self, rules, ):
        """
        :param rules: 一个特殊的服务端加密配置规则信息
        """
        self.rules = rules
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.rules is not None:
            rules_array = []
            for item in self.rules:
                if type(item) is dict:
                    rules_array.append(item)
                else:
                    rules_array.append(item.get_dic())
            obj_dict["rules"] = rules_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.rules is None:
            raise Exception("rules can not None")


class Rule(object):

    def __init__(self, apply_server_side_encryption_by_default, ):
        """
        :param apply_server_side_encryption_by_default: 指定默认的服务端加密会应用于新对象上传至存储桶时。若是在上传对象时请求中未指定任何加密信息，则存储桶默认加密将会应用
        """
        self.apply_server_side_encryption_by_default = apply_server_side_encryption_by_default
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.apply_server_side_encryption_by_default is not None:
            if type(self.apply_server_side_encryption_by_default) is dict:
                obj_dict["applyServerSideEncryptionByDefault"] = self.apply_server_side_encryption_by_default
            else:
                obj_dict["applyServerSideEncryptionByDefault"] = self.apply_server_side_encryption_by_default.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.apply_server_side_encryption_by_default is None:
            raise Exception("apply_server_side_encryption_by_default can not None")


class ApplyServerSideEncryptionByDefault(object):

    def __init__(self, sse_algorithm, kms_master_key_id=None):
        """
        :param sse_algorithm: 加密算法，仅支持 AES256 或 aws:kms
        :param kms_master_key_id: 若加密算法选用的是aws:kms，则此项必填，按照cmkuuid:keyspec:userid模式配置，其中cmkuuid是CMKID，keyspec是指定生成的数据密钥长度，userid是用户id；若是AES256算法，则此项可不填，若填，则字符长度需为32
        """
        self.sse_algorithm = sse_algorithm
        self.kms_master_key_id = kms_master_key_id
        self.check_param()

    def set_kms_master_key_id(self, kms_master_key_id):
        """
        :param kms_master_key_id: 若加密算法选用的是aws:kms，则此项必填，按照cmkuuid:keyspec:userid模式配置，其中cmkuuid是CMKID，keyspec是指定生成的数据密钥长度，userid是用户id；若是AES256算法，则此项可不填，若填，则字符长度需为32
        """
        self.kms_master_key_id = kms_master_key_id

    def get_dic(self):
        obj_dict = dict()
        if self.sse_algorithm is not None:
            obj_dict["SSEAlgorithm"] = self.sse_algorithm
        if self.kms_master_key_id is not None:
            obj_dict["KMSMasterKeyID"] = self.kms_master_key_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.sse_algorithm is None:
            raise Exception("sse_algorithm can not None")


class PutBucketEncryptionRequestParam(object):

    def __init__(self, bucket, region_id, server_side_encryption_configuration, ):
        """
        :param bucket: 存储空间名
        :param region_id: 
        :param server_side_encryption_configuration: 指定默认服务端加密配置
        """
        self.bucket = bucket
        self.region_id = region_id
        self.server_side_encryption_configuration = server_side_encryption_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.server_side_encryption_configuration is None:
            raise Exception("server_side_encryption_configuration can not None")

