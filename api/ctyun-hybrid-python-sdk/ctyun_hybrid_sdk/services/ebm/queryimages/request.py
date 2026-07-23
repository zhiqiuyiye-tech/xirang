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


class QueryImagesRequest(CTYunRequest):
    """
    通过参数查询物理机可支持的镜像，查询条件 imageUUID，osName，osVersion不支持   
       
    bits返回类型与v1未对齐
    """

    def __init__(self, request_param):
        super(QueryImagesRequest, self).__init__("/v4/ebm/image-list", "GET", "ebm", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.device_type is not None:
            query_param["deviceType"] = self.parameters.device_type
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.image_uuid is not None:
            query_param["imageUUID"] = self.parameters.image_uuid
        if self.parameters.os_name is not None:
            query_param["osName"] = self.parameters.os_name
        if self.parameters.os_version is not None:
            query_param["osVersion"] = self.parameters.os_version
        if self.parameters.os_type is not None:
            query_param["osType"] = self.parameters.os_type
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryImagesRequestParam(object):

    def __init__(self, region_id, device_type, az_name=None, image_uuid=None, os_name=None, os_version=None, os_type=None, page_no=None, page_size=None):
        """
        :param region_id: 区域ID
        :param device_type: 设备类型
        :param az_name: 可用区(4.0必传)
        :param image_uuid: 镜像id-不支持
        :param os_name: 操作系统名词-不支持
        :param os_version: 操作系统版本-不支持
        :param os_type: 操作系统类型
        :param page_no: 页码
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.region_id = region_id
        self.device_type = device_type
        self.az_name = az_name
        self.image_uuid = image_uuid
        self.os_name = os_name
        self.os_version = os_version
        self.os_type = os_type
        self.page_no = page_no
        self.page_size = page_size

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区(4.0必传)
        """
        self.az_name = az_name

    def set_image_uuid(self, image_uuid):
        """
        :param image_uuid: 镜像id-不支持
        """
        self.image_uuid = image_uuid

    def set_os_name(self, os_name):
        """
        :param os_name: 操作系统名词-不支持
        """
        self.os_name = os_name

    def set_os_version(self, os_version):
        """
        :param os_version: 操作系统版本-不支持
        """
        self.os_version = os_version

    def set_os_type(self, os_type):
        """
        :param os_type: 操作系统类型
        """
        self.os_type = os_type

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_type is None:
            raise Exception("device_type can not None")

