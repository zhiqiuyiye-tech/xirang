# ctyun-hybrid-python-sdk

# 简介 #

欢迎使用天翼私有云开发者Python工具套件（Python SDK）。使用天翼私有云Python SDK，您无需复杂编程就可以访问天翼私有云提供的各种服务。

为了方便您理解SDK中的一些概念和参数的含义，使用SDK前建议您先查看[天翼私有云IaaS Openapi文档](https://apifox.com/apidoc/shared-b270f09d-bebe-4f21-a97e-a1e9d46a074f)。要了解每个API的具体参数和含义，请参考程序注释或具体API的文档描述。

# 环境准备 #
1. 天翼私有云Python SDK适用于 Python 3 以上版本，暂时无法支持Python 2.7。
2. 在开始调用天翼私有云Open API之前，需提前在天翼私有云个人中心-> 我的凭证中获取accesskey和secretKey密钥对（简称AK/SK），如页面没有请联系管理员创建。AK/SK信息请妥善保管，如果遗失可能会造成非法用户使用此信息操作您在天翼私有云上的资源，给你造成数据和财产损失。

# SDK使用方法 #
目前暂时无法通过Pip公网仓库进行发布SDK,请您编译此项目，直接使用 ` python setup.py install ` 或者 如果使用` pip install -i https://pypi.tuna.tsinghua.edu.cn/simple .`（可以不配置镜像源） 安装此包到本地进行使用
 
SDK使用中的任何问题，欢迎您联系天翼私有云团队进行反馈，在这里感谢各位的支持。

**注意：**

- 天翼私有云并没有提供其他下载方式，请务必使用上述官方获取方式！

- 每支云产品都有自己的Client，当调用该产品API时，需使用该产品的Client。例如：使用云主机的CtecsClient只能调用云主机（ctecs）的接口。

# 调用SDK #
Python SDK的调用主要分为4步：

1. 设置accessKey和secretKey
2. 创建Client
3. 设置请求参数
4. 执行请求得到响应

以下是创建云硬盘实例详情的调用示例

```python
# coding=utf-8
import json
from ctyun_hybrid_sdk.services.ebs.ebsnew.request import EbsNewRequestParam, EbsNewRequest
from ctyun_hybrid_sdk.services.ebs.client import EbsClient
from ctyun_hybrid_sdk.core.credential import Credential
from ctyun_hybrid_sdk.core.config import Config 
from ctyun_hybrid_sdk.core.const import SCHEME_HTTPS, SCHEME_HTTP

if __name__ == '__main__':
    
    # 设置请求的ak sk
    ak = "xxx"
    sk = "xxx"
    credential = Credential(access_key=ak,  secret_key=sk)
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="1.1.1.1:9080",scheme=SCHEME_HTTP,timeout= 10 )
    # 创建client
    client = EbsClient(credential,config)
    # 初始化请求参数
    requestParam = EbsNewRequestParam(client_token="test123",region_id="2022guizhou_syj",az_name="cn-xinan1-2A", name="ebs-newspec-test0211v91-lisj", disk_mode="VBD",
                                              disk_type="SAS", on_demand=True, disk_size=10, cycle_count=1 )
    request = EbsNewRequest(requestParam)
    # 设置私有header
    request.header["xxx"] = "1000001079"
    # 进行请求获取返回值
    resp = client.ebs_new(request)
    # 打印返回值
    print(json.dumps(resp.__dict__, ensure_ascii=False))
```

如果需要设置额外的header，则按照如下方式：
```python
    request.header["xxx"]="1000000617"
```

* 如果你的私有云环境使用的是 `apache shenyu` 网关(具体使用那个网关请联系混合云团队),需要使用如下配置变更使用的验签方法：

```python
    credential = Credential(access_key=ak, secret_key=sk)
    # 设置访问网关地址，协议是HTTPS 还是HTTP ，和超时时间
    config = Config(endpoint="203.193.231.238:31062", scheme=SCHEME_HTTP, timeout=10)
    vpc_client = CtvpcClient(credential, config,signer="hybrid")
```