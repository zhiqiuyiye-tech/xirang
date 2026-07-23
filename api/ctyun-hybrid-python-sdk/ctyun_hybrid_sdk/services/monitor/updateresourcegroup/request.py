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


class UpdateResourceGroupRequest(CTYunRequest):
    """
    调用此接口可更新资源分组，支持全量字段修改。   
       
    接口约束   
    1. 资源分组名称不可重复。2. 资源分组创建类型不能修改。3. 其他参见请求参数说明。
    """

    def __init__(self, request_param):
        super(UpdateResourceGroupRequest, self).__init__("/v4.1/monitor/update-resource-group", "POST", "monitor", "application/json")
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
        if self.parameters.res_group_id is not None:
            body_param["resGroupID"] = self.parameters.res_group_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.desc is not None:
            body_param["desc"] = self.parameters.desc
        if self.parameters.create_type is not None:
            body_param["createType"] = self.parameters.create_type
        if self.parameters.resource_list is not None:
            resource_list = []
            if isinstance(self.parameters.resource_list, list):
                for item in self.parameters.resource_list:
                    if type(item) is dict:
                        resource_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        resource_list.append(item_dict_value)
            else:
                resource_list.append(self.parameters.resource_list.get_dic())
            body_param["resourceList"] = resource_list
        if self.parameters.project_info is not None:
            if type(self.parameters.project_info) is dict:
                project_info_dict_value = self.parameters.project_info
            else:
                project_info_dict_value = self.parameters.project_info.get_dic()
            body_param["projectInfo"] = project_info_dict_value
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


class Resource(object):

    def __init__(self, service, dimension, resources, ):
        """
        :param service: 云监控服务。取值范围：   
         ecs：云主机；   
         pms：物理机；   
         ph：宿主机；   
         scaling：弹性伸缩；   
         ippool：弹性IP；   
         elb：弹性负载均衡；   
         cda：专线网关；   
         physical_line：物理专线；   
         pushgateway_hpfs：并行文件服务
        :param dimension: 云监控维度。取值范围：   
         ecs：云主机；   
         pms：物理机；   
         ph：宿主机；   
         scaling：弹性伸缩；   
         ippool：弹性IP；   
         elb：弹性负载均衡；   
         cda_virtual_gateway：专线网关；   
         physical_line：物理专线；   
         pushgateway_hpfs：并行文件服务
        :param resources: 
        """
        self.service = service
        self.dimension = dimension
        self.resources = resources
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.service is not None:
            obj_dict["service"] = self.service
        if self.dimension is not None:
            obj_dict["dimension"] = self.dimension
        if self.resources is not None:
            resources_array = []
            for item in self.resources:
                if type(item) is dict:
                    resources_array.append(item)
                else:
                    resources_array.append(item.get_dic())
            obj_dict["resources"] = resources_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.service is None:
            raise Exception("service can not None")
        if self.dimension is None:
            raise Exception("dimension can not None")
        if self.resources is None:
            raise Exception("resources can not None")


class ProjectInfo(object):

    def __init__(self, project_id, project_products, ):
        """
        :param project_id: 
        :param project_products: 
        """
        self.project_id = project_id
        self.project_products = project_products
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.project_id is not None:
            obj_dict["projectID"] = self.project_id
        if self.project_products is not None:
            project_products_array = []
            for item in self.project_products:
                if type(item) is dict:
                    project_products_array.append(item)
                else:
                    project_products_array.append(item.get_dic())
            obj_dict["projectProducts"] = project_products_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.project_id is None:
            raise Exception("project_id can not None")
        if self.project_products is None:
            raise Exception("project_products can not None")


class ProjectProduct(object):

    def __init__(self, service, dimension, ):
        """
        :param service: 本参数表示服务。取值范围： ecs：云主机。 evs：云硬盘。 pms：物理机。 ...
        :param dimension: 本参数表示告警维度。取值范围： ecs：云主机。 disk：磁盘。 pms：物理机。 ...
        """
        self.service = service
        self.dimension = dimension
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.service is not None:
            obj_dict["service"] = self.service
        if self.dimension is not None:
            obj_dict["dimension"] = self.dimension
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.service is None:
            raise Exception("service can not None")
        if self.dimension is None:
            raise Exception("dimension can not None")


class UpdateResourceGroupRequestParam(object):

    def __init__(self, region_id, res_group_id, name, desc=None, create_type=None, resource_list=None, project_info=None):
        """
        :param region_id: 资源池ID
        :param res_group_id: 资源分组ID
        :param name: 长度为2-63个字符，中文、英文（大小写）、数字、点号 (.)、下划线(_)、半角冒号 (:)、连字符 (-)，不支持连续字符--
        :param desc: 描述
        :param create_type: 本参数表示创建方式，默认值：instance。取值范围：   
         instance：实例创建。   
         project：企业项目创建。   
         根据以上范围取值。   
         注意：资源分组创建类型不能修改，要与创建时的创建类型保持一致。
        :param resource_list: 创建方式为实例创建时的资源列表，创建方式（createType）为instance时，resourceList为必填参数，资源列表中的元素resourceListObj的个数不超过20个。 注意:此参数为数组
        :param project_info: 创建方式为企业项目创建时的企业项目信息， 创建方式（createType）为project时，projectInfo为必填参数。暂不支持
        """
        self.region_id = region_id
        self.res_group_id = res_group_id
        self.name = name
        self.desc = desc
        self.create_type = create_type
        self.resource_list = resource_list
        self.project_info = project_info

    def set_desc(self, desc):
        """
        :param desc: 描述
        """
        self.desc = desc

    def set_create_type(self, create_type):
        """
        :param create_type: 本参数表示创建方式，默认值：instance。取值范围：   
         instance：实例创建。   
         project：企业项目创建。   
         根据以上范围取值。   
         注意：资源分组创建类型不能修改，要与创建时的创建类型保持一致。
        """
        self.create_type = create_type

    def set_resource_list(self, resource_list):
        """
        :param resource_list: 创建方式为实例创建时的资源列表，创建方式（createType）为instance时，resourceList为必填参数，资源列表中的元素resourceListObj的个数不超过20个。
        """
        self.resource_list = resource_list

    def set_project_info(self, project_info):
        """
        :param project_info: 创建方式为企业项目创建时的企业项目信息， 创建方式（createType）为project时，projectInfo为必填参数。暂不支持
        """
        self.project_info = project_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.res_group_id is None:
            raise Exception("res_group_id can not None")
        if self.name is None:
            raise Exception("name can not None")

