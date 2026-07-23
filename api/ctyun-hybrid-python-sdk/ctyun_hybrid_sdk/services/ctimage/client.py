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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class CtimageClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctimage-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtimageClient, self).__init__(credential, config, 'ctimage', '0.1.0', logger, signer)

    def iaas_detail_image(self, iaas_detail_image_request_param):
        """
        /v4/ctcloud/iaas_ctimage/detail_image
        根据镜像 ID，查询一份镜像的详细信息。
        """
        return self.send(iaas_detail_image_request_param)

    def iso_image_create(self, iso_image_create_request_param):
        """
        /v4/image/create-from-iso
        创建iso镜像
        """
        return self.send(iso_image_create_request_param)

    def detail_image(self, detail_image_request_param):
        """
        /v4/image/detail
        根据镜像 ID，查询一份镜像的详细信息。
        """
        return self.send(detail_image_request_param)

    def create_image_from_ecs_snapshot(self, create_image_from_ecs_snapshot_request_param):
        """
        /v4/image/create-from-ecs-snapshot
        云主机快照创建系统盘镜像
        """
        return self.send(create_image_from_ecs_snapshot_request_param)

    def create_ecs_system_disk_image(self, create_ecs_system_disk_image_request_param):
        """
        /v4/image/create
        创建私有系统盘镜像   
    接口约束：   
    云主机为关机或者云行中，系统盘为已挂载，非中间态
        """
        return self.send(create_ecs_system_disk_image_request_param)

    def share_private_image(self, share_private_image_request_param):
        """
        /v4/image/shared-image/create
        公有云文档是传共享镜像的接受人的名称，混合云只支持共享镜像的接受项目的id
        """
        return self.send(share_private_image_request_param)

    def delete_private_image_import_task(self, delete_private_image_import_task_request_param):
        """
        /v4/image/delete
        无operationId   
    删除一份自定义镜像
        """
        return self.send(delete_private_image_import_task_request_param)

    def export_private_image(self, export_private_image_request_param):
        """
        /v4/image/export
        导出私有镜像   
    开发未对齐原因：混合云返回镜像链接，公有云无返回参数   
    首次是导出下发，导出成功后会返回正常url
        """
        return self.send(export_private_image_request_param)

    def create_by_image_file(self, create_by_image_file_request_param):
        """
        /v4/image/create-from-file
        镜像文件创建镜像
        """
        return self.send(create_by_image_file_request_param)

    def reject_shared_image(self, reject_shared_image_request_param):
        """
        /v4/image/shared-image/reject
        无operationId
        """
        return self.send(reject_shared_image_request_param)

    def accept_shared_image(self, accept_shared_image_request_param):
        """
        /v4/image/shared-image/accept
        无operationId
        """
        return self.send(accept_shared_image_request_param)

    def iaas_ctimage_import_image(self, iaas_ctimage_import_image_request_param):
        """
        /v4/image/import
        使用指定的存在对象存储（原生版）Ⅰ 型的镜像文件来创建一份私有镜像。   
    开发未对齐原因：混合云异步执行会返回任务ID，公有云无返回结果
        """
        return self.send(iaas_ctimage_import_image_request_param)

    def show_shared_list(self, show_shared_list_request_param):
        """
        /v4/image/show-shared-list
        在您将一份私有镜像共享给其他项目之后，此接口可用于查询该私有镜像的共享列表
        """
        return self.send(show_shared_list_request_param)

    def unshare_private_image(self, unshare_private_image_request_param):
        """
        /v4/image/shared-image/delete
        公有云文档是传共享镜像的接受人的名称，混合云只支持共享镜像的接受项目的id
        """
        return self.send(unshare_private_image_request_param)

    def query_shared_image_hybrid(self, query_shared_image_hybrid_request_param):
        """
        /v4/image/query-shared-images
        开发未对齐原因：按照最初提供的Excel和混合云对接开发的，一直未找到公有云接口   
    
        """
        return self.send(query_shared_image_hybrid_request_param)

    def list_images(self, list_images_request_param):
        """
        /v4/image/list
        根据镜像可见类型等，查询可以使用的镜像资源。
        """
        return self.send(list_images_request_param)

    def create_ecs_data_disk_image(self, create_ecs_data_disk_image_request_param):
        """
        /v4/image/create-from-data-disk
        前置条件：数据盘镜像要求数据盘为in-use或available状态   
    无operationId
        """
        return self.send(create_ecs_data_disk_image_request_param)
