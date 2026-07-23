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


class PutBucketRefererRequest(CTYunRequest):
    """
    防盗链设置
    """

    def __init__(self, request_param):
        super(PutBucketRefererRequest, self).__init__("/v4/oss/put-bucket-referer", "POST", "zos", "application/json")
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
        if self.parameters.referer_list is not None:
            body_param["refererList"] = self.parameters.referer_list
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


class PutBucketRefererRequestParam(object):

    def __init__(self, region_id, bucket, referer_list, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param referer_list: 保存Referer访问白名单地址的容器，地址字符串大小写敏感，支持多字符通配符 "\\*" 以及单字符通配符 "?"，此容器具有覆盖行为，若覆盖为空数组 []，将清空此白名单。地址也允许为空字符串 "" 注意:此参数为数组
        """
        self.region_id = region_id
        self.bucket = bucket
        self.referer_list = referer_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.referer_list is None:
            raise Exception("referer_list can not None")

