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


class CommonClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('common-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CommonClient, self).__init__(credential, config, 'common', '0.1.0', logger, signer)

    def query_order_uuid_v41(self, query_order_uuid_v41_request_param):
        """
        /v4/order/query-uuid
        订单状态：目前仅支持完成-3/施工失败-5/开通中-14   
    资源类型：返回主资源类型。如果多子订单为批开则返回第一个子订单的资源类型，如果多子订单不同主资源类型(VM/EIP退订这种)则以VM为主
        """
        return self.send(query_order_uuid_v41_request_param)

    def job_list(self, job_list_request_param):
        """
        /v4/job/list
        查询job列表
        """
        return self.send(job_list_request_param)

    def query_available_zone(self, query_available_zone_request_param):
        """
        /v4/resource/query-available-zone
        将废弃,原因：未匹配公有云 建议使用:/v4/region/get-zones   
    补充返回参数中id的说明：V2没有数字zoneId属性，目前是根据UUID，将uuid按照’-‘分隔，并且取前两个数据，组成的16进制字符串，转换成int64生成的。即，e334a588-260e-43dc-aa29-887a8e616328 转换成 e334a588260e， 然后将e334a588260e转成int64，请勿拿此id执行查询操作   
       
    
        """
        return self.send(query_available_zone_request_param)

    def iaas_common_job_detail(self, iaas_common_job_detail_request_param):
        """
        /v4/job/detail
        job详情
        """
        return self.send(iaas_common_job_detail_request_param)

    def iaas_check_demand(self, iaas_check_demand_request_param):
        """
        /v4/region/check-demand
        查询用户可用的产品是否可售，支持云主机、云硬盘、弹性公网IP产品的可售查询。   
    如果当前用户所属vdc未开启配额，直接返回满足条件   
       
    ## 接口约束   
       
    渠道用户产品未售罄可售，   
       
    非渠道用户产品未售罄且用户当前配额有余量可售。   
    原有存量接口仍然可用,   
    存量接口：POST /v4/region/check-demand   
       
       
    ## 参数约束   
    productType传ecs时，flavorID和specName有一个必须为必填项，如果都传，以flavorID为准   
       
    productType传ebs时，ebsSize为必填项   
       
    productType传eip时，eipAmount不是必填项，不填默认1
        """
        return self.send(iaas_check_demand_request_param)

    def iaas_get_summary(self, iaas_get_summary_request_param):
        """
        /v4/region/get-summary
        查询资源池概况，比如地域，多az信息，支持的cpu架构，资源池占用类型，资源池版本信息等   
    开发未对齐原因：混合云资源池返回值不支持省、市等字段
        """
        return self.send(iaas_get_summary_request_param)

    def iaas_get_zones(self, iaas_get_zones_request_param):
        """
        /v4/region/get-zones
        查询单个资源池的可用区信息   
       
    ### 接口约束   
       
    仅对支持多可用区的资源池有效
        """
        return self.send(iaas_get_zones_request_param)

    def iaas_region_list_regions(self, iaas_region_list_regions_request_param):
        """
        /v4/region/list-regions
        查询租户可见的资源池列表。仅查询4.0多可用区的资源池   
       
    该接口所属rbac模块
        """
        return self.send(iaas_region_list_regions_request_param)

    def query_available_resource_pool(self, query_available_resource_pool_request_param):
        """
        /v4/resource/query-available-resource-pool
        将废弃,原因：未匹配公有云 建议使用:/v4/region/list-regions
        """
        return self.send(query_available_resource_pool_request_param)

    def query_new_order_price_v42(self, query_new_order_price_v42_request_param):
        """
        /v4/order/new-query-price
        购买云产品时询价接口，支持云主机、云硬盘、弹性公网IP产品的包年/包月或按量订单的询价功能
        """
        return self.send(query_new_order_price_v42_request_param)

    def get_region_total_remain_metric(self, get_region_total_remain_metric_request_param):
        """
        /v4/region/get-total-remain-metric
        获取单资源池的总量和剩余量
        """
        return self.send(get_region_total_remain_metric_request_param)

    def iaas_get_products(self, iaas_get_products_request_param):
        """
        /v4/region/get-products
        查询一个资源池支持的云产品信息列表，以及云产品的产品特性信息。   
       
    ## 接口约束: 2.2.1 以下版本只支持云盘产品信息返回，2.2.1 版本以上支持返回云盘产品信息，oss，hpfs和sfs支持信息返回。   
    
        """
        return self.send(iaas_get_products_request_param)

    def region_check_demand(self, region_check_demand_request_param):
        """
        /v4/region/check-demand
        约束：云主机规格资源池4.0区分az，product=ecs时请给azName字段赋值   
    spec对象中云主机规格参数：flavorID、specName。product=ecs时两者传其中一个即可   
    spec对象中磁盘规格参数: size。product=ebs时必传
        """
        return self.send(region_check_demand_request_param)

    def iaas_get_vdc_quota(self, iaas_get_vdc_quota_request_param):
        """
        /v4/region/getVdcQuota
        VDC配额和已用配额查询   
    备注：   
    1. 补充返回参数中id的说明：V2没有数字ID属性，目前是根据UUID，将uuid按照’-‘分隔，并且取前两个数据，组成的16进制字符串，转换成int64生成的。即，e334a588-260e-43dc-aa29-887a8e616328 转换成 e334a588260e， 然后将e334a588260e转成int64，请勿拿此id执行查询操作   
    2. vdc开启配额后才返回配额信息   
    
        """
        return self.send(iaas_get_vdc_quota_request_param)

    def query_resource(self, query_resource_request_param):
        """
        /v4/resource/list
        从25.630 v2.2.3版本后支持
        """
        return self.send(query_resource_request_param)
