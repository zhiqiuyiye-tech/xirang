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


class V4SfsRegionStoragetypeRequest(CTYunRequest):
    """
    用于展示弹性文件下列信息：   
    （1）所支持的协议类型   
    （2）所支持的弹性文件类型   
    （3）资源池下的az列表
    """

    def __init__(self, request_param):
        super(V4SfsRegionStoragetypeRequest, self).__init__("/v4/sfs/region/storagetype", "GET", "sfs", "application/json")
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
        if self.parameters.sfs_type is not None:
            body_param["sfsType"] = self.parameters.sfs_type
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class V4SfsRegionStoragetypeRequestParam(object):

    def __init__(self, region_id, sfs_type=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param sfs_type: 文件系统类型，取值范围：performance-性能型、capacity-标准型、hdd_e-标准型专属。不传表示查询所有类型
        :param page_no: 页码
        :param page_size: 分页查询时每页包含的地域数
        """
        self.region_id = region_id
        self.sfs_type = sfs_type
        self.page_no = page_no
        self.page_size = page_size

    def set_sfs_type(self, sfs_type):
        """
        :param sfs_type: 文件系统类型，取值范围：performance-性能型、capacity-标准型、hdd_e-标准型专属。不传表示查询所有类型
        """
        self.sfs_type = sfs_type

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页包含的地域数
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

