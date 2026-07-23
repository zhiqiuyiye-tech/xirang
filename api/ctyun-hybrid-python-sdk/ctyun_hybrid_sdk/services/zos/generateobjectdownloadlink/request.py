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


class GenerateObjectDownloadLinkRequest(CTYunRequest):
    """
    生成对象临时下载链接
    """

    def __init__(self, request_param):
        super(GenerateObjectDownloadLinkRequest, self).__init__("/v4/oss/generate-object-download-link", "POST", "zos", "application/json")
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
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
        if self.parameters.version_id is not None:
            body_param["versionID"] = self.parameters.version_id
        if self.parameters.expires_in is not None:
            body_param["expiresIn"] = self.parameters.expires_in
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


class GenerateObjectDownloadLinkRequestParam(object):

    def __init__(self, region_id, bucket, key, version_id=None, expires_in=None):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param key: 对象名
        :param version_id: 版本id
        :param expires_in: url 过期时间，默认 3600s(输入0为默认3600)
        """
        self.region_id = region_id
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.expires_in = expires_in

    def set_version_id(self, version_id):
        """
        :param version_id: 版本id
        """
        self.version_id = version_id

    def set_expires_in(self, expires_in):
        """
        :param expires_in: url 过期时间，默认 3600s(输入0为默认3600)
        """
        self.expires_in = expires_in

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.key is None:
            raise Exception("key can not None")

