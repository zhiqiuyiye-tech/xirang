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


class CreateEipAddressGroupOpenApiRequest(CTYunRequest):
    """
    创建ip地址组
    """

    def __init__(self, request_param):
        super(CreateEipAddressGroupOpenApiRequest, self).__init__("/v4/eipPool", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.provider is not None:
            body_param["provider"] = self.parameters.provider
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.vdc_ids is not None:
            body_param["vdcIDs"] = self.parameters.vdc_ids
        if self.parameters.segments is not None:
            segments = []
            if isinstance(self.parameters.segments, list):
                for item in self.parameters.segments:
                    if type(item) is dict:
                        segments.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        segments.append(item_dict_value)
            else:
                segments.append(self.parameters.segments.get_dic())
            body_param["segments"] = segments
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


class Segment(object):

    def __init__(self, start, end, segment_uuid=None):
        """
        :param start: 
        :param end: 
        :param segment_uuid: 
        """
        self.start = start
        self.end = end
        self.segment_uuid = segment_uuid
        self.check_param()

    def set_segment_uuid(self, segment_uuid):
        """
        :param segment_uuid: 
        """
        self.segment_uuid = segment_uuid

    def get_dic(self):
        obj_dict = dict()
        if self.start is not None:
            obj_dict["start"] = self.start
        if self.end is not None:
            obj_dict["end"] = self.end
        if self.segment_uuid is not None:
            obj_dict["segmentUuid"] = self.segment_uuid
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.start is None:
            raise Exception("start can not None")
        if self.end is None:
            raise Exception("end can not None")


class CreateEipAddressGroupOpenApiRequestParam(object):

    def __init__(self, name, provider, region_id, segments, description=None, vdc_ids=None):
        """
        :param name: 名称
        :param provider: 
        :param description: 
        :param region_id: 
        :param vdc_ids:  注意:此参数为数组
        :param segments:  注意:此参数为数组
        """
        self.name = name
        self.provider = provider
        self.description = description
        self.region_id = region_id
        self.vdc_ids = vdc_ids
        self.segments = segments

    def set_description(self, description):
        """
        :param description: 
        """
        self.description = description

    def set_vdc_ids(self, vdc_ids):
        """
        :param vdc_ids: 
        """
        self.vdc_ids = vdc_ids

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.provider is None:
            raise Exception("provider can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.segments is None:
            raise Exception("segments can not None")

