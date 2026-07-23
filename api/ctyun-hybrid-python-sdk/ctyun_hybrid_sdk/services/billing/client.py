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


class BillingClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('billing-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(BillingClient, self).__init__(credential, config, 'billing', '0.1.0', logger, signer)

    def query_regin_discounts(self, query_regin_discounts_request_param):
        """
        /v1/billing/queryReginDiscounts
        获取资源池特价
        """
        return self.send(query_regin_discounts_request_param)

    def query_product_detail(self, query_product_detail_request_param):
        """
        /v1/billing/queryProductDetail
        根据serviceTag和resourceType获取产品信息   
    2.2.6.3 接口注册发布
        """
        return self.send(query_product_detail_request_param)

    def query_bill_detail(self, query_bill_detail_request_param):
        """
        /queryBillDetail
        该接口为查询账单详情接口， 对应页面运营中心/账单明细， 返回数据一致
        """
        return self.send(query_bill_detail_request_param)

    def qry_on_demand_bill_detail_prod_cycle_id(self, qry_on_demand_bill_detail_prod_cycle_id_request_param):
        """
        /qryOnDemandBillDetailProdCycleId
        51. 账单明细产品+账期（按需）
        """
        return self.send(qry_on_demand_bill_detail_prod_cycle_id_request_param)

    def create_sale_relation_strategys(self, create_sale_relation_strategys_request_param):
        """
        /v1/billing/createSaleRelationStrategys
        销售品批量关联计价策略
        """
        return self.send(create_sale_relation_strategys_request_param)

    def query_bill_financial_statement(self, query_bill_financial_statement_request_param):
        """
        /queryBillFinancialStatement
        该接口为查询财务统计接口， 对应页面运营中心/财务统计，与前端数据一致
        """
        return self.send(query_bill_financial_statement_request_param)

    def query_product_detail_by_id(self, query_product_detail_by_id_request_param):
        """
        /v1/billing/queryProductDetailByID
        2.2.6.3 接口注册发布
        """
        return self.send(query_product_detail_by_id_request_param)

    def qry_on_demand_bill_detail_res_cycle_id(self, qry_on_demand_bill_detail_res_cycle_id_request_param):
        """
        /qryOnDemandBillDetailResCycleId
        52. 账单明细资源+账期（按需）
        """
        return self.send(qry_on_demand_bill_detail_res_cycle_id_request_param)

    def query_product_attr_values(self, query_product_attr_values_request_param):
        """
        /v1/billing/queryProductAttrValues
        获取产品属性值列表
        """
        return self.send(query_product_attr_values_request_param)

    def query_product_global_settings(self, query_product_global_settings_request_param):
        """
        /v1/billing/queryProductGlobalSettings
        获取混合云管中，产品计量计费总开关配置的状态（页面修改后接口实时生效）
        """
        return self.send(query_product_global_settings_request_param)

    def query_product_relation_products(self, query_product_relation_products_request_param):
        """
        /v1/billing/queryProductRelationProducts
        获取产品关联产品信息
        """
        return self.send(query_product_relation_products_request_param)

    def query_product_catalogs(self, query_product_catalogs_request_param):
        """
        /v1/billing/queryProductCatalogs
        产品目录列表接口
        """
        return self.send(query_product_catalogs_request_param)

    def query_pricing_unit(self, query_pricing_unit_request_param):
        """
        /v1/billing/queryPricingUnit
        获取产品计价单元
        """
        return self.send(query_pricing_unit_request_param)

    def query_products(self, query_products_request_param):
        """
        /v1/billing/queryProducts
        产品列表
        """
        return self.send(query_products_request_param)

    def query_account_bill_by_account_id(self, query_account_bill_by_account_id_request_param):
        """
        /queryAccountBillByAccountId
        47. 账户账单查询
        """
        return self.send(query_account_bill_by_account_id_request_param)

    def query_product_strategys(self, query_product_strategys_request_param):
        """
        /v1/billing/queryProductStrategys
        获取单产品下定价策略列表
        """
        return self.send(query_product_strategys_request_param)

    def query_vdc_discounts(self, query_vdc_discounts_request_param):
        """
        /v1/billing/queryVdcDiscounts
        获取VDC特价
        """
        return self.send(query_vdc_discounts_request_param)

    def create_product_attr_value(self, create_product_attr_value_request_param):
        """
        /v1/billing/createProductAttrValue
        创建产品属性值
        """
        return self.send(create_product_attr_value_request_param)

    def bill_qry_on_demand_bill_detail_res_detail(self, bill_qry_on_demand_bill_detail_res_detail_request_param):
        """
        /billQryOnDemandBillDetailResDetail
        50. 账单明细资源+明细(按需)
        """
        return self.send(bill_qry_on_demand_bill_detail_res_detail_request_param)

    def query_product_catalog_detail(self, query_product_catalog_detail_request_param):
        """
        /v1/billing/queryProductCatalogDetail
        产品目录详情
        """
        return self.send(query_product_catalog_detail_request_param)

    def query_relation_product_sales(self, query_relation_product_sales_request_param):
        """
        /v1/billing/queryRelationProductSales
        获取主产品关联的上架产品的所有销售品
        """
        return self.send(query_relation_product_sales_request_param)

    def create_sale_relation_regins(self, create_sale_relation_regins_request_param):
        """
        /v1/billing/createSaleRelationRegins
        销售品批量关联资源池
        """
        return self.send(create_sale_relation_regins_request_param)

    def query_relation_sales(self, query_relation_sales_request_param):
        """
        /v1/billing/queryRelationSales
        获取关联销售品列表
        """
        return self.send(query_relation_sales_request_param)

    def query_sales(self, query_sales_request_param):
        """
        /v1/billing/querySales
        获取销售品列表
        """
        return self.send(query_sales_request_param)

    def query_product_relation_regins(self, query_product_relation_regins_request_param):
        """
        /v1/billing/queryProductRelationRegins
        获取产品关联可用区
        """
        return self.send(query_product_relation_regins_request_param)

    def sync_sales(self, sync_sales_request_param):
        """
        /v1/billing/syncSales
        同步销售品
        """
        return self.send(sync_sales_request_param)

    def query_product_attrs(self, query_product_attrs_request_param):
        """
        /v1/billing/queryProductAttrs
        获取产品属性列表
        """
        return self.send(query_product_attrs_request_param)

    def qry_cycle_bill_detail_prod_cycle_id(self, qry_cycle_bill_detail_prod_cycle_id_request_param):
        """
        /qryCycleBillDetailProdCycleId
        49. 账单明细产品+账期（包周期）
        """
        return self.send(qry_cycle_bill_detail_prod_cycle_id_request_param)
