# coding=utf8

# coding=utf8

# Copyright 2023 CTYUN.COM
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


import json
import traceback
import requests
from urllib import parse
from ctyun_hybrid_sdk.core import const
from ctyun_hybrid_sdk.core.eop_signer import EopSigner
from ctyun_hybrid_sdk.core.hybrid_signer import HybridSigner
from ctyun_hybrid_sdk.core.version import VERSION
from urllib.parse import quote, unquote_plus
from ctyun_hybrid_sdk.core.exception import ClientException
from ctyun_hybrid_sdk.core.response import CtYunResponse
from ctyun_hybrid_sdk.core.logger import get_default_logger, INFO, ERROR
from ctyun_hybrid_sdk.core.util import byte_to_str


class CTYunClient(object):

    def __init__(self, credential, config, service_name, revision, logger, signer=None):
        self.__config = config
        self.__service_name = service_name
        self.__credential = credential
        self.__revision = revision
        self.__logger = logger
        if logger is None:
            self.__logger = get_default_logger()
        if signer is None or signer == "eop":
            self.__signer = EopSigner(self.__logger)
        elif signer == "hybrid":
            self.__signer = HybridSigner(self.__logger)
        else:
            self.__signer = EopSigner(self.__logger)

    def send(self, request):
        if self.__config is None:
            raise ClientException('Miss config object')
        if self.__credential is None:
            raise ClientException('Miss credential object')
        if request is None:
            raise ClientException('Miss request object')
        if request.parameters is None:
            raise ClientException('Miss parameters in request')
        try:
            header = self.__merge_headers(request.header, request.content_type)

            url = self.__build_url(request)
            query = request.get_query_param()
            body = self.__build_body(request)
            self.__logger.log(INFO, 'url=' + url)
            self.__logger.log(INFO, 'body=' + body)
            self.__signer.sign(query=query, headers=header, body=body, credential=self.__credential)
            self.__logger.log(INFO, header)
            if query is not None and isinstance(query, dict):
                url = self.__build_query_url(url, query)
            if self.__service_name is not None and self.__service_name !="":
                header['x-ctyun-service'] = self.__service_name
            if self.__config.scheme == const.SCHEME_HTTPS:
                # if use set skip tls verify in config, will skip tls verify
                resp = requests.request(request.method, url, data=body, headers=header,
                                    timeout=self.__config.timeout,verify=self.__config.cert_verify )
            else:
                resp = requests.request(request.method, url, data=body, headers=header,
                                    timeout=self.__config.timeout )
            self.__logger.log(INFO, resp.content)

            return self.__process_response(request.method, resp)
        except Exception as expt:
            msg = traceback.format_exc()
            self.__logger.log(ERROR, msg)
            raise expt

    def __merge_headers(self, request_header, content_type):
        headers = dict()
        if request_header is not None and isinstance(request_header, dict):
            for key, value in request_header.items():
                headers[key] = value
        headers['User-Agent'] = 'CtyunSdkPython/%s %s/%s' % (VERSION, self.__service_name, self.__revision)
        if content_type is not None and content_type != '':
            headers['Content-Type'] = content_type
        else:
            headers['Content-Type'] = 'application/json'
        self.__logger.log(INFO, headers)
        return headers

    def __build_body(self, request):
        body_param = request.get_body_param()
        if isinstance(body_param, dict):
            if const.CONTENT_TYPE_JSON in str.lower(request.content_type):
                return json.dumps(body_param)
            elif const.CONTENT_TYPE_FORM in str.lower(request.content_type):
                return self.__build_form_body(body_param)
        if isinstance(body_param, str):
            return body_param
        return json.dumps(body_param)

    def __build_form_body(self, body_param_dic):
        data = parse.urlencode(body_param_dic)
        return data

    def __build_url(self, request):
        path_param = request.get_path_param()
        url = request.url
        if path_param is not None and isinstance(path_param, dict):
            for key in path_param:
                if url.find("{" + key + "}") != -1:
                    continue
                str.replace(url, "{" + key + "}", path_param[key])
        request_url = self.__config.scheme + "://" + self.__config.endpoint + url
        return request_url

    def __build_query_url(self, url, query):
        query_array = []
        query_string = ''
        for key in query:
            value = query[key]
            key_value = self.__url_decode(key)
            if value is None:
                continue
            if isinstance(value, list):
                for v in value:
                    query_array.append('%s=%s' % (self.__url_encode(key_value),  self.__url_encode(self.__url_decode(str(v)))))
            elif isinstance(value, dict):
                for k in value:
                    v = value[k]
                    k_decode = self.__url_decode(k)
                    query_array.append('%s=%s' % (self.__url_encode(key_value + "." + k_decode),  self.__url_encode(self.__url_decode(str(v)))))
            else:
                query_array.append('%s=%s' % (self.__url_encode(key_value),  self.__url_encode(self.__url_decode(str(value)))))
        if len(query_array) > 0:
            query_string = "&".join(query_array)
        return url + "?" + query_string

    def __url_encode(self, value):
        process_value = str(value)
        return quote(process_value, '~')

    def __url_decode(self, value):
        process_value = str(value)
        return unquote_plus(process_value)

    def __process_response(self, method, response):
        ctyun_resp = CtYunResponse()
        content_length = response.headers.get(const.HEADER_CONTENT_LEN)
        request_id = response.headers.get(const.HEADER_REQUEST_ID)
        if request_id is None or request_id == '':
            request_id = response.headers.get(const.HYBRID_REQUEST_ID)
            ctyun_resp.request_id = ''
        if request_id is None or request_id == '':
            request_id = response.headers.get(const.HYBRID_REQUEST_TRACE_ID)
        if request_id is None or request_id == '':
            ctyun_resp.request_id = request_id
        else:
            ctyun_resp.request_id = request_id
        if method == const.METHOD_HEAD or response.status_code in (204, 304) or content_length == '0':
            ctyun_resp.statusCode = 800
            ctyun_resp.errorCode = "success"
            ctyun_resp.message = "success"
            ctyun_resp.description = "success"
        else:
            ctyun_resp.fill_json_value(byte_to_str(response.content))
        return ctyun_resp
