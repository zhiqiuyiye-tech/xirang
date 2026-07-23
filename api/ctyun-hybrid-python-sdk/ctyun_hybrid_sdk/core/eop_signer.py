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

import base64
import datetime
import time
import hashlib
import hmac
import uuid
from urllib.parse import quote, unquote_plus
from ctyun_hybrid_sdk.core.logger import get_default_logger, INFO, ERROR

class EopSigner(object):

    def __init__(self, logger):
        self.__logger = logger

    def sign(self, query, headers, body, credential, now=None, request_id=None):
        access_key = credential.access_key
        secret_key = credential.secret_key
        # 生成一个表示日期和时间的ISO8601格式的字符串
        if now is None:
            now = self.__now()
        hybrid_date = now.strftime('%Y%m%dT%H%M%SZ')

        # randomStr = "f774b1ad-73af-48ee-a64b-738f071e473c"
        if request_id is None:
            request_id = str(uuid.uuid4())
        # 将ctyun-hybrid-request-id和hybrid-date加入头信息
        if headers is None:
            headers = {}
        headers["Ctyun-Eop-Request-Id"] = request_id
        headers["Eop-Date"] = hybrid_date
        after_query = self.__normalize_query_string(query)

        if body is None:
            body = ""
        calculate_content_hash = self.__sha256_hash(body)

        header = "Ctyun-Eop-Request-Id;Eop-Date"
        header_list = header.split(";")
        header_list.sort(key=str.upper)

        sign_header = ""
        for header_name in header_list:
            header_name = header_name.strip()
            if header_name in headers:
                sign_header += f"{header_name.lower()}:{headers[header_name]}\n"

        string_to_sign = sign_header + "\n" + after_query + "\n" + calculate_content_hash
        signature = self.__sign(string_to_sign, hybrid_date, access_key, secret_key)
        auth = f"{access_key} Headers={header.lower()} Signature={signature}"
        headers["Eop-Authorization"] = auth
        return headers

    def __sign(self, string_to_sign, eop_data,  access_key, secret_key):
        # build key time
        crypto_date = eop_data[:8]
        k_time = self.__sign_hmac(secret_key.encode("utf-8"), eop_data)
        k_ak = self.__sign_hmac(k_time, access_key)
        k_data = self.__sign_hmac(k_ak, crypto_date)
        signature = self.__sign_hmac(k_data,string_to_sign)
        return str(base64.b64encode(signature), 'utf-8')

    def __sign_hmac(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def __now(self):
        return datetime.datetime.now().astimezone()
       # this is for utc time support
       # return datetime.datetime.fromtimestamp(time.time())

    def __sha256_hash(self, val):
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __normalize_query_string(self, query):
        params = []
        if isinstance(query, str):
            for s in query.split('&'):
                if len(s) <= 0:
                    continue
                query_list = []
                for val in s.split('='):
                    query_list.append(self.__urlencode(self.__urldecode(val)))
                params.append(query_list)
        elif isinstance(query, dict):
            for key in query.keys():

                value = query[key]
                if value is None:
                    continue
                if isinstance(value, list):
                    for val in value:
                        query_list = [self.__urlencode(self.__urldecode(key)), self.__urlencode(self.__urldecode(val))]
                        params.append(query_list)
                else:
                    query_list = [self.__urlencode(self.__urldecode(key)),
                                  self.__urlencode(self.__urldecode(query[key]))]
                    params.append(query_list)
        normalized_array = []
        for p in sorted(params):
            if p[0] == '':
                continue
            elif len(p) == 2:
                normalized_array.append('%s=%s' % (p[0], p[1]))
            elif len(p) > 2:
                normalized_array.append('%s=%s' % (p[0], '%3D'.join(p[1:])))
        if len(normalized_array) == 0:
            return ""
        normalized_array.sort()
        normalized = "&".join(normalized_array)
        normalized = normalized.replace("%2C", ",")
        self.__logger.log(INFO, f"EopSigner normalized query string: {normalized}")
        return normalized

    def __urlencode(self, value):
        process_value = str(value)
        return quote(process_value, '~')

    def __urlencode_ignore_slashes(self, value):
        process_value = str(value)
        return quote(process_value, '/~')

    def __urldecode(self, value):
        process_value = str(value)
        return unquote_plus(process_value)
