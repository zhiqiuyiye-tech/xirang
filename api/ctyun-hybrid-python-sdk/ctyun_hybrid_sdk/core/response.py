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


class CtYunResponse(object):

    def __int__(self):
        self.request_id = None
        self.returnObj = None
        self.statusCode = None
        self.errorCode = None
        self.message = None
        self.description = None

    def __getitem__(self, key):
        return getattr(self, key)

    # TODO THIS NEED MAP CONTENT TYPE AND RETURN DATA
    def fill_json_value(self, resp):
        return json.loads(resp, object_hook=self.load_hook)

    def load_hook(self, resp_dict):
        self.statusCode = resp_dict.get('statusCode')
        error_code = resp_dict.get('errorCode')
        if error_code is not None:
            self.errorCode = error_code
        result = resp_dict.get('returnObj')
        if self.statusCode == 800 and result is not None:
            self.returnObj = resp_dict['returnObj']
        self.message = resp_dict.get("message")
        self.description = resp_dict.get("description")
        trace_id = resp_dict.get("traceID")
        if trace_id is not None and trace_id != "":
            self.request_id = trace_id
        return resp_dict


