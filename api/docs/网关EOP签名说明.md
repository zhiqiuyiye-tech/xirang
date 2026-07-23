# 网关EOP签名说明


### 天翼云公有云签名

#### 构造请求

* 本节介绍REST API请求的组成，以调用云主机产品的"根据regionID查询用户资源"举例说明如何调用该API。

* 请求示例

```
POST https://ctecs-xxx.ctapi.ctyun.local/v4/region/customerResources?prodInstId=11&startTime=2021-04-04T06:01:46ZHTTP/1.1
Content-Type:application/json
ctyun-eop-request-id:0ffb9b07-d5a8-4e19-b3ce-12dfb9705a1d
Eop-Authorization:4a4bdc57e06542199b5f98d4cd107be2 Headers=ctyun-eop-request-id;eop-date Signature=b2WEo4nh9ewn6SWOP0ii5g8L0z9CT5gprpDWntlCX9I=
Eop-date:20221107T093029Z
```
* 请求URI
```
{URI-scheme}://{Endpoint}/{resource-path}?{query-string}
```

|参数	|描述|
|----|-----|
|URI-scheme|	表示用于传输请求的协议，当前所有API均采用HTTPS协议|
|Endpoint|	指定承载REST服务端点的服务器域名或IP，不同服务不同区域的Endpoint不同，您可以从地区和终端节点获取。例如云主机产品服务在某个区域的Endpoint为“ctecs-xxx.ctapi.ctyun.cn”|
|resource-path|	资源路径，即API访问路径。从具体API的URI模块获取，例如"根据regionID查询用户资源"API的resource-path为“/v4/region/customerResources”|
|query-string|	查询参数，是可选部分，并不是每个API都有查询参数。查询参数前面需要带一个“?”，形式为“参数名=参数取值”，例如“?limit=10”，表示查询不超过10条数据|

* 示例：

云主机-根据regionID查询用户资源，则需使用云主机产品在对应区域的Endpoint（ctecs-xxx.ctapi.ctyun.cn），并在"根据regionID查询用户资源"的URI部分找到resource-path（/v4/region/customerResources），拼接起来如下所示。

https://ctecs-xxx.ctapi.ctyun.local/v4/region/customerResources

说明： 为方便查看，在每个具体API的URI部分，只给出resource-path部分，并将请求方法写在一起。这是因为URI-scheme都是HTTPS，而Endpoint在同一个区域也相同，所以简洁起见将这两部分省略。

{resource-path}资源路径，使用编码的规范URI示例：

前：
/v4/region/customerResources api/code
后：
/v4/region/customerResources%20api/code
说明：

资源路径{resource-path}是从HTTP Host结束到查询字符串参数（如果有）的问号字符（“?”）中间的部分。 需要根据RFC3986标准化URI路径规范移除冗余和相对路径部分。路径中每个部分都必须进行URI编码。

{query-string}查询参数，使用规范查询字符串示例：

前：
prodInstId=11&startTime=2021-04-04T06:01:46Z
后：
prodInstId=11&startTime=2021-04-04T06%3A01%3A46Z
说明：

{query-string}为键值对，使用等号字符(=)拼接。值需进行URI编码，同样需要满足RFC3986关于URL编码规范的定义要求。键则不需要。对没有值的参数使用空字符串。

在每个参数值后追加与字符(&)，列表中最后一个值除外。

使用 %XY 对所有其他字符进行百分比编码，其中“X”和“Y”为十六进制字符（0-9和大写字母A-F）。例如，空格字符必须编码为 %20（不像某些编码方案那样使用“+”)，扩展UTF-8字符必须采用格式 %XY%ZA%BC。

RFC3986规范的具体要求：

字符A-Z、a-z、0-9 以及字符-、_、.、~不编码。

对其它ASCII码字符进行编码。编码格式为%加上16进制的ASCII码。例如半角双引号（"）将被编码为%22。空格编码成%20，而不是加号（+）。

非ASCII码通过UTF-8编码。

* 请求方法

|方法|	说明|
|----|----|
|GET |	请求服务器返回指定资源|
|PUT	|请求服务器更新指定资源|
|POST	|请求服务器新增资源或执行特殊操作|
|DELETE|	请求服务器删除指定资源，如删除对象等|
|HEAD	|请求服务器资源头部|
|PATCH|	请求服务器更新资源的部分内容 ,当资源不存在的时候，PATCH可能会去创建一个新的资源。|

在"根据regionID查询用户资源"的URI部分，您可以看到其请求方法为“POST”，则其请求为：

POST https://ctecs-xxx.ctapi.ctyun.cn/v4/region/customerResources

请求消息头

|名称|	描述|	是否必选|	示例|
|---|---|----|---|
|Content-Type|	消息体的类型	|是|	application/json|
|ctyun-eop-request-id|	流水号（32位随机数）|	是|	0ffb9b07-d5a8-4e19-b3ce-12dfb9705a1d|
|Eop-Authorization|	签名认证信息|	是| 4a4bdc57e06542199b5f98d4cd107be2 Headers=ctyun-eop-request-id;eop-date Signature=b2WEo4nh9ewn6SWOP0ii5g8L0z9CT5gprpDWntlCX9I=|
|Eop-date|	时间，15分钟有效期(实际传时间为北京东八区UTC+8时间。TZ仅为格式，非UTC时间。)|	是|	20221107T093029Z|

* Eop-Authorization签名认证信息：

* 步骤一：构造代签字符串sigture
sigture=需要进行签名的Header排序后的组合列表+"\n"+encode的query+"\n"+toHex(sha256(原封的body))

|名称 |描述|
|---|---|
|需要进行签名的Header排序后的组合列表|	将ctyun-eop-request-id、eop-date以 “header_name:header_value”的形式、以“\n”作为每个header的结尾符、以英文字母表作为header_name的排序依据将它们拼接起来。注意：EOP强制要求ctyun-eop-request-id、eop-date必须进行签名。其他字段是否需要签名看自身需求。例子(假设你需要将ctyun-eop-request-id、eop-date、host都要签名)：ctyun-eop-request-id:123456789\neop-date:20210531T100101Z\n|
|encode的query|	query以&作为拼接，key和value以=连接，值需要encode，query参数全部都需要进行签名|
|toHex(sha256(原封的body))| 传进来的body参数进行sha256摘要，对摘要出来的结果转十六进制|

>sigture示例1（假设query为空、需要进行签名的Header排序后的组合列表为“ctyun-eop-request-id:27cfe4dc-e640-45f6-92ca-492ca73e8680\neop-date:20220525T160752Z\n”、body参数做sha256摘要后转十六进制为e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855）： ctyun-eop-request-id:27cfe4dc-e640-45f6-92ca-492ca73e8680\neop-date:20220525T160752Z\n\n\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855


>sigture示例2（假设query不为空、需要进行签名的Header排序后的组合列表为“ctyun-eop-request-id:27cfe4dc-e640-45f6-92ca-492ca73e8680\neop-date:20220525T160752Z\n”、body参数做sha256摘要后转十六进制为e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855）： ctyun-eop-request-id:27cfe4dc-e640-45f6-92ca-492ca73e8680\neop-date:20220525T160930Z\n\naa=1&bb=2\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

* 步骤二：构造动态秘钥kdate

1.使用eop-date作为数据，sk作为密钥，算出ktime。
2.使用ak作为数据，ktime作为密钥，算出kAk。
3.使用eop-date的年月日值作为数据，kAk作为密钥，算出kdate。
|名称|	描述|
|---|---|
|eop-date|	yyyyMMdd'T'HHmmss'Z'(20211221T163614Z)(年月日T时分秒Z)(实际传时间为北京东八区UTC+8时间，TZ仅为格式，非UTC时间)|
|ktime|	使用eop-date作为数据，sk作为密钥，算出ktime。ktime=hmacSHA256(eop-date,sk)|
|kAk|	使用ak作为数据，ktime作为密钥，算出kAk。kAk=hmacSHA256(ak,ktime)|
|kdate|	使用eop-date的年月日值作为数据，kAk作为密钥，算出kdate|

* 步骤三：构造signature
使用kdate作为密钥、sigture作为数据，将其得到的结果进行base64编码得出signature

|名称	|描述|
|---|---|
|signature|	hmacSHA256(sigture,kdate)将上一步的结果进行base64加密得出signature|

* 步骤四：构造Eop-Authorization
1.构造Headers。
2.得到Eop-Authorization。
Eop-Authorization:ak Headers=xxx Signature=xxx。

|名称|描述|
|---|---|
|Headers|将需要进行签名的请求头字段以 “header_name”的形式、以“;”作为间隔符、以英文字母表作为header_name的排序依据将它们拼接起来。例子(假设你需要将ctyun-eop-request-id、eop-date都要签名)：Headers=ctyun-eop-request-id;eop-date|
|Eop-Authorization|	Eop-Authorization:ak Headers=xxx Signature=xxx。注意，ak、Headers、Signature之间以空格隔开。例如：Eop-Authorization:ak Headers=ctyun-eop-request-id;eop-date Signature=NlMHOhk5bVfZ9MwDSSJydcZjjENmDtpNYigJGVb。注意：如果你需要进行签名的Header不止默认的ctyun-eop-request-id和eop-date，那么你需要在http_client的请求头部中加上，并且Eop-Authorization中也需要增加|

