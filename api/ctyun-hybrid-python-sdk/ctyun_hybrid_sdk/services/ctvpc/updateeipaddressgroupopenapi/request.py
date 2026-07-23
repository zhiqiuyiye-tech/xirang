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


class UpdateEipAddressGroupOpenApiRequest(CTYunRequest):
    """
    修改ip地址组
    """

    def __init__(self, request_param):
        super(UpdateEipAddressGroupOpenApiRequest, self).__init__("/v4/eipPool", "PUT", "ctvpc", "application/json")
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
        if self.parameters.eip_address_group_id is not None:
            body_param["eipAddressGroupID"] = self.parameters.eip_address_group_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class UpdateEipAddressGroupOpenApiRequestParam(object):

    def __init__(self, eip_address_group_id, name=None, description=None, segments=None):
        """
        :param name: 名称
        :param eip_address_group_id: 
        :param description: 
        :param segments: 只支持增量添加，不支持删减 注意:此参数为数组
        """
        self.name = name
        self.eip_address_group_id = eip_address_group_id
        self.description = description
        self.segments = segments

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 
        """
        self.description = description

    def set_segments(self, segments):
        """
        :param segments: 只支持增量添加，不支持删减
        """
        self.segments = segments

    def check_param(self):
        """
        the param required check
        """
        if self.eip_address_group_id is None:
            raise Exception("eip_address_group_id can not None")

