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


class PutBucketCorsRequest(CTYunRequest):
    """
    跨域资源共享更新
    """

    def __init__(self, request_param):
        super(PutBucketCorsRequest, self).__init__("/v4/oss/put-bucket-cors", "POST", "zos", "application/json")
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
        if self.parameters.cors_configuration is not None:
            if type(self.parameters.cors_configuration) is dict:
                cors_configuration_dict_value = self.parameters.cors_configuration
            else:
                cors_configuration_dict_value = self.parameters.cors_configuration.get_dic()
            body_param["CORSConfiguration"] = cors_configuration_dict_value
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


class CORSConfiguration(object):

    def __init__(self, cors_rules, ):
        """
        :param cors_rules: 为指定bucket配置的所有跨域规则的集合 不设置传[]
        """
        self.cors_rules = cors_rules
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.cors_rules is not None:
            cors_rules_array = []
            for item in self.cors_rules:
                if type(item) is dict:
                    cors_rules_array.append(item)
                else:
                    cors_rules_array.append(item.get_dic())
            obj_dict["CORSRules"] = cors_rules_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.cors_rules is None:
            raise Exception("cors_rules can not None")


class CORSRule(object):

    def __init__(self, allowed_origins, allowed_methods, allowed_headers=None, expose_headers=None, max_age_seconds=None):
        """
        :param allowed_origins: 来源
        :param allowed_methods: "GET", "POST", "PUT", "DELETE", "HEAD"
        :param allowed_headers: 允许Headers
        :param expose_headers: 暴露Headers
        :param max_age_seconds: (0为不设置)
        """
        self.allowed_origins = allowed_origins
        self.allowed_methods = allowed_methods
        self.allowed_headers = allowed_headers
        self.expose_headers = expose_headers
        self.max_age_seconds = max_age_seconds
        self.check_param()

    def set_allowed_headers(self, allowed_headers):
        """
        :param allowed_headers: 允许Headers
        """
        self.allowed_headers = allowed_headers

    def set_expose_headers(self, expose_headers):
        """
        :param expose_headers: 暴露Headers
        """
        self.expose_headers = expose_headers

    def set_max_age_seconds(self, max_age_seconds):
        """
        :param max_age_seconds: (0为不设置)
        """
        self.max_age_seconds = max_age_seconds

    def get_dic(self):
        obj_dict = dict()
        if self.allowed_origins is not None:
            obj_dict["allowedOrigins"] = self.allowed_origins
        if self.allowed_methods is not None:
            obj_dict["allowedMethods"] = self.allowed_methods
        if self.allowed_headers is not None:
            obj_dict["allowedHeaders"] = self.allowed_headers
        if self.expose_headers is not None:
            obj_dict["exposeHeaders"] = self.expose_headers
        if self.max_age_seconds is not None:
            obj_dict["maxAgeSeconds"] = self.max_age_seconds
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.allowed_origins is None:
            raise Exception("allowed_origins can not None")
        if self.allowed_methods is None:
            raise Exception("allowed_methods can not None")


class PutBucketCorsRequestParam(object):

    def __init__(self, region_id, bucket, cors_configuration, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param cors_configuration: 跨域资源共享参数
        """
        self.region_id = region_id
        self.bucket = bucket
        self.cors_configuration = cors_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.cors_configuration is None:
            raise Exception("cors_configuration can not None")

