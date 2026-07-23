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


class CtmessageClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctmessage-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtmessageClient, self).__init__(credential, config, 'ctmessage', '0.1.0', logger, signer)

    def open_api_put_email_gateway_info(self, open_api_put_email_gateway_info_request_param):
        """
        /v4/message/email/update
        1. 仅支持SMTP协议邮件服务器;   
    2. status字段为true时，tls默认值为false，其他所有配置字段为必传字段；
        """
        return self.send(open_api_put_email_gateway_info_request_param)

    def open_api_put_sms_gateway_info(self, open_api_put_sms_gateway_info_request_param):
        """
        /v4/message/sms/update
        1. status为false时，其他参数无效，可设置为空；
        """
        return self.send(open_api_put_sms_gateway_info_request_param)

    def send_message_by_template(self, send_message_by_template_request_param):
        """
        /v4/message/send-message
        注: 9901-其他消息暂时未定义模板   
    detailParam参数不同类型的消息对应参数不同，所有参数类型均使用字符串类型，具体如下：   
    产品消息，消息详细类型:1001,1002,1003,1004,1005:   
    regionID -- 资源池ID   
    productType -- 产品类型   
    productTypeName -- 产品类型名称   
    resourceID -- 资源ID   
    resourceUUID -- 资源UUID   
    resourceName -- 资源名称   
    resourceOwner -- 资源所属人用户名称   
    运维消息，消息详细类型:2001, 2002:   
    regionID -- 资源池ID   
    productType -- 产品类型   
    productTypeName -- 产品类型名称   
    resourceName -- 资源名称   
    resourceOwner -- 资源所属人用户名称   
    alarmLevel -- 告警级别,1-提示,2-一般,3-严重,4-灾难   
    alarmRuleID -- 告警规则ID   
    alarmRuleName -- 告警规则名称,   
    currentValue -- 当前告警值   
    resourceID -- 资源ID   
    resourceUUID -- 资源UUID   
    monitorType -- 监控类型   
    平台消息，详细消息类型：3001，3002，3011. 3012:   
    resourceID -- 资源ID   
    resourceName -- 资源名称   
    其中，产品类型productType和产品类型名称productTypeName枚举见产品资源中心产品编码与产品名称，固定值   
    工单消息，详细消息类型: 4001，4002：    
    regionID -- 资源池ID，   
    resourceID -- 工单ID,    
    resourceName -- 工单名称   
     resourceOwner -- 提单人，   
    workOrderType-工单类型；   
    4002:    
    approvalResult-工单审批结果
        """
        return self.send(send_message_by_template_request_param)

    def open_api_get_email_gateway_info(self, open_api_get_email_gateway_info_request_param):
        """
        /v4/message/email/info
        1. 响应中的password为加密后的字符串，需要按照特定的对称加密规则进行解密得到密码原文；
        """
        return self.send(open_api_get_email_gateway_info_request_param)

    def open_api_send_test_email(self, open_api_send_test_email_request_param):
        """
        /v4/message/email/test
        发送测试邮件
        """
        return self.send(open_api_send_test_email_request_param)

    def open_api_get_sms_gateway_info(self, open_api_get_sms_gateway_info_request_param):
        """
        /v4/message/sms/info
        获取短信网关配置
        """
        return self.send(open_api_get_sms_gateway_info_request_param)
