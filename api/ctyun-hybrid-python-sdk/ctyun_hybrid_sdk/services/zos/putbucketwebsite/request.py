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


class PutBucketWebsiteRequest(CTYunRequest):
    """
    若传入参数redirectAllRequestsTo，则indexDocument, errorDocument, routingRules不生效。
    """

    def __init__(self, request_param):
        super(PutBucketWebsiteRequest, self).__init__("/v4/oss/put-bucket-website", "POST", "zos", "application/json")
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
        if self.parameters.website_configuration is not None:
            if type(self.parameters.website_configuration) is dict:
                website_configuration_dict_value = self.parameters.website_configuration
            else:
                website_configuration_dict_value = self.parameters.website_configuration.get_dic()
            body_param["websiteConfiguration"] = website_configuration_dict_value
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


class WebsiteConfiguration(object):

    def __init__(self, redirect_all_requests_to=None, index_document=None, error_document=None, routing_rules=None):
        """
        :param redirect_all_requests_to: 重定向所有请求配置
        :param index_document: 索引文档配置
        :param error_document: 错误文档配置
        :param routing_rules: 重定向规则配置
        """
        self.redirect_all_requests_to = redirect_all_requests_to
        self.index_document = index_document
        self.error_document = error_document
        self.routing_rules = routing_rules

    def set_redirect_all_requests_to(self, redirect_all_requests_to):
        """
        :param redirect_all_requests_to: 重定向所有请求配置
        """
        self.redirect_all_requests_to = redirect_all_requests_to

    def set_index_document(self, index_document):
        """
        :param index_document: 索引文档配置
        """
        self.index_document = index_document

    def set_error_document(self, error_document):
        """
        :param error_document: 错误文档配置
        """
        self.error_document = error_document

    def set_routing_rules(self, routing_rules):
        """
        :param routing_rules: 重定向规则配置
        """
        self.routing_rules = routing_rules

    def get_dic(self):
        obj_dict = dict()
        if self.redirect_all_requests_to is not None:
            if type(self.redirect_all_requests_to) is dict:
                obj_dict["redirectAllRequestsTo"] = self.redirect_all_requests_to
            else:
                obj_dict["redirectAllRequestsTo"] = self.redirect_all_requests_to.get_dic()
        if self.index_document is not None:
            if type(self.index_document) is dict:
                obj_dict["indexDocument"] = self.index_document
            else:
                obj_dict["indexDocument"] = self.index_document.get_dic()
        if self.error_document is not None:
            if type(self.error_document) is dict:
                obj_dict["errorDocument"] = self.error_document
            else:
                obj_dict["errorDocument"] = self.error_document.get_dic()
        if self.routing_rules is not None:
            routing_rules_array = []
            for item in self.routing_rules:
                if type(item) is dict:
                    routing_rules_array.append(item)
                else:
                    routing_rules_array.append(item.get_dic())
            obj_dict["routingRules"] = routing_rules_array
        return obj_dict


class RedirectAllRequestsTo(object):

    def __init__(self, host_name, protocol=None):
        """
        :param host_name: 在重定向请求中使用的主机名
        :param protocol: 指定重定向所有请求的目标协议，值为 http 或 https
        """
        self.host_name = host_name
        self.protocol = protocol
        self.check_param()

    def set_protocol(self, protocol):
        """
        :param protocol: 指定重定向所有请求的目标协议，值为 http 或 https
        """
        self.protocol = protocol

    def get_dic(self):
        obj_dict = dict()
        if self.host_name is not None:
            obj_dict["hostName"] = self.host_name
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.host_name is None:
            raise Exception("host_name can not None")


class IndexDocument(object):

    def __init__(self, suffix, ):
        """
        :param suffix: 指定索引文档的对象键后缀
        """
        self.suffix = suffix
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.suffix is not None:
            obj_dict["suffix"] = self.suffix
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.suffix is None:
            raise Exception("suffix can not None")


class ErrorDocument(object):

    def __init__(self, key, ):
        """
        :param key: 指定通用错误文档的对象键
        """
        self.key = key
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.key is None:
            raise Exception("key can not None")


class RoutingRule(object):

    def __init__(self, redirect, condition=None):
        """
        :param condition: 重定向规则的条件配置
        :param redirect: 重定向规则的具体重定向目标配置
        """
        self.condition = condition
        self.redirect = redirect
        self.check_param()

    def set_condition(self, condition):
        """
        :param condition: 重定向规则的条件配置
        """
        self.condition = condition

    def get_dic(self):
        obj_dict = dict()
        if self.condition is not None:
            if type(self.condition) is dict:
                obj_dict["condition"] = self.condition
            else:
                obj_dict["condition"] = self.condition.get_dic()
        if self.redirect is not None:
            if type(self.redirect) is dict:
                obj_dict["redirect"] = self.redirect
            else:
                obj_dict["redirect"] = self.redirect.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.redirect is None:
            raise Exception("redirect can not None")


class Condition(object):

    def __init__(self, http_error_code_returned_equals=None, key_prefix_equals=None):
        """
        :param http_error_code_returned_equals: 指定重定向规则的错误码匹配条件；http错误代码，输入能转为int类型
        :param key_prefix_equals: 指定重定向规则的错误码匹配条件
        """
        self.http_error_code_returned_equals = http_error_code_returned_equals
        self.key_prefix_equals = key_prefix_equals

    def set_http_error_code_returned_equals(self, http_error_code_returned_equals):
        """
        :param http_error_code_returned_equals: 指定重定向规则的错误码匹配条件；http错误代码，输入能转为int类型
        """
        self.http_error_code_returned_equals = http_error_code_returned_equals

    def set_key_prefix_equals(self, key_prefix_equals):
        """
        :param key_prefix_equals: 指定重定向规则的错误码匹配条件
        """
        self.key_prefix_equals = key_prefix_equals

    def get_dic(self):
        obj_dict = dict()
        if self.http_error_code_returned_equals is not None:
            obj_dict["httpErrorCodeReturnedEquals"] = self.http_error_code_returned_equals
        if self.key_prefix_equals is not None:
            obj_dict["keyPrefixEquals"] = self.key_prefix_equals
        return obj_dict


class Redirect(object):

    def __init__(self, host_name=None, replace_key_with=None, protocol=None, replace_key_prefix_with=None, http_redirect_code=None):
        """
        :param host_name: 在重定向请求中使用的主机名
        :param replace_key_with: 指定重定向规则的具体重定向目标的对象键，替换方式为替换整个原始请求的对象键
        :param protocol: 指定重定向规则的目标协议，值为 http 或 https
        :param replace_key_prefix_with: 在重定向请求中使用的对象关键前缀
        :param http_redirect_code: 指定重定向规则；响应中要使用的HTTP重定向代码，输入能转为int类型
        """
        self.host_name = host_name
        self.replace_key_with = replace_key_with
        self.protocol = protocol
        self.replace_key_prefix_with = replace_key_prefix_with
        self.http_redirect_code = http_redirect_code

    def set_host_name(self, host_name):
        """
        :param host_name: 在重定向请求中使用的主机名
        """
        self.host_name = host_name

    def set_replace_key_with(self, replace_key_with):
        """
        :param replace_key_with: 指定重定向规则的具体重定向目标的对象键，替换方式为替换整个原始请求的对象键
        """
        self.replace_key_with = replace_key_with

    def set_protocol(self, protocol):
        """
        :param protocol: 指定重定向规则的目标协议，值为 http 或 https
        """
        self.protocol = protocol

    def set_replace_key_prefix_with(self, replace_key_prefix_with):
        """
        :param replace_key_prefix_with: 在重定向请求中使用的对象关键前缀
        """
        self.replace_key_prefix_with = replace_key_prefix_with

    def set_http_redirect_code(self, http_redirect_code):
        """
        :param http_redirect_code: 指定重定向规则；响应中要使用的HTTP重定向代码，输入能转为int类型
        """
        self.http_redirect_code = http_redirect_code

    def get_dic(self):
        obj_dict = dict()
        if self.host_name is not None:
            obj_dict["hostName"] = self.host_name
        if self.replace_key_with is not None:
            obj_dict["replaceKeyWith"] = self.replace_key_with
        if self.protocol is not None:
            obj_dict["protocol"] = self.protocol
        if self.replace_key_prefix_with is not None:
            obj_dict["replaceKeyPrefixWith"] = self.replace_key_prefix_with
        if self.http_redirect_code is not None:
            obj_dict["httpRedirectCode"] = self.http_redirect_code
        return obj_dict


class PutBucketWebsiteRequestParam(object):

    def __init__(self, bucket, region_id, website_configuration, ):
        """
        :param bucket: 存储空间名
        :param region_id: 资源池ID
        :param website_configuration: 指定默认服务端加密配置
        """
        self.bucket = bucket
        self.region_id = region_id
        self.website_configuration = website_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.website_configuration is None:
            raise Exception("website_configuration can not None")

