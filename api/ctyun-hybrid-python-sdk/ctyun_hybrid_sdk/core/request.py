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


class CTYunRequest(object):

    def __init__(self, url, method, service, content_type, header=None):
        self.url = url
        self.method = method
        self.service = service
        self.content_type = content_type
        self.header = header

    def get_body_param(self):
        return dict()

    def get_query_param(self):
        return dict()

    def get_path_param(self):
        return dict()
