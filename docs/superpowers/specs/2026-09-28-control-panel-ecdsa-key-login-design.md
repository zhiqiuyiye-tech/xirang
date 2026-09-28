# 控制面板 ECDSA P-256 私钥文件登录设计

- 日期：2026-09-28
- 状态：已审阅/冻结（实现 Baseline）

## 目标与信任边界

将现有管理员密码登录替换为 ECDSA P-256 挑战签名登录。系统只保留一个 `admin` 账号；所有操作者共用一份私钥文件，因此不提供多用户、角色或个人级审计归因。

部署只能使用 HTTP，入口通过内网 IP 白名单限制。浏览器在非 localhost 的 HTTP 页面不能依赖 `crypto.subtle`，因此前端随项目发布固定版本的 P-256 JavaScript 加密库。HTTP 的安全边界明确如下：

- 被动监听者能看到 HTTP 请求/响应、初始化密码和会话 Cookie；拿到 Cookie 后，可以在会话过期或版本撤销前以完整管理员权限操作。一次性签名 nonce 不能保护 HTTP Session。
- 在首次登记期间，监听者还可截获初始化密码并用自己的密钥竞争首次登记；新密钥 PoP 只证明登记者持有其候选私钥，不能证明其是合法操作者。因此首次登记必须在受控内网窗口完成，并在部署 Secret 初始化后尽快执行。
- 被动监听者不能仅凭 challenge 和签名推导长期私钥，也不能重放已消费的 challenge。
- 主动中间人可以替换页面或 JavaScript，在用户选择私钥文件时读取并外传私钥；HTTP 下无法通过应用层密码学阻止这一点。白名单和内网隔离只缩小暴露面，不等同于 TLS。

## 管理员认证状态

`admin.auth_state` 使用以下状态：

- `PASSWORD_BOOTSTRAP`：尚未登记公钥；`public_key_pem` 与 `public_key_fingerprint` 必须为 `NULL`，`password_hash` 必须是可验证的 bcrypt 哈希；只有首次登记接口允许验证密码。
- `KEY_ACTIVE`：公钥有效；`public_key_pem` 必须是可解析的规范 P-256 SPKI PEM，指纹必须与规范 DER 的 SHA-256 一致，`password_hash` 必须为 `__DISABLED_AFTER_KEY_BOOTSTRAP__`；密码登录和引导接口均关闭。
- `RECOVERY_PENDING`：仅允许作为离线恢复后的启动过渡态；公钥与指纹必须为 `NULL`，`password_hash` 必须为 `__PENDING_INIT__`。此状态不能提供任何 HTTP 服务；启动恢复后转为 `PASSWORD_BOOTSTRAP`。

管理员记录必须严格符合上述字段组合。服务在创建 HTTP listener 前检查并拒绝任何不一致、无效公钥或未知状态；`ADMIN_INIT_PASSWORD` 缺失/为空时，配置加载必须在 HTTP 服务启动前失败，包括 `KEY_ACTIVE` 状态，因为它是唯一离线恢复凭据。首次建库时，启动 seed 逻辑把 `__PENDING_INIT__` 哈希替换成该 Secret 的 bcrypt 哈希并设置为 `PASSWORD_BOOTSTRAP`；恢复启动按下文转换。

## 数据迁移

一次性迁移需要：

- 在 `admin` 表增加 `auth_state`、可空的规范化 `public_key_pem` 和 `public_key_fingerprint`。既有账号迁移后为 `PASSWORD_BOOTSTRAP`，保留当前密码哈希以支持首次登记。
- 新增 `auth_challenges`：`challenge_id`、`nonce`、`purpose`、`auth_version`、`key_fingerprint`、`new_key_fingerprint`、`client_ip`、`created_at`、`expires_at`、`consumed_at`。
- 对既有 admin 只递增一次 `auth_version`，撤销升级前签发的全部会话。
- 为挑战过期时间与客户端 IP 建索引。每次创建挑战时清理过期记录，并清理超过 24 小时的已消费记录。
- 当前版本只支持单进程、单副本和本地持久化 SQLite；Helm/原始部署必须保持 `replicas: 1`，不支持共享 SQLite 文件的多副本或水平扩展。
- `db.Open` 在运行任何迁移前执行 `SELECT sqlite_version()` 并要求 runtime `>= 3.35.0`，以保证 `UPDATE ... RETURNING` 可用；缺少或低于要求时启动失败。当前 `modernc.org/sqlite v1.54.0` 实际查询结果为 `3.53.3`。

## 密钥与签名协议

### 编码与指纹

- 私钥文件为未加密的 PKCS#8 PEM（`BEGIN PRIVATE KEY`）。文件只由浏览器生成/读取，不上传给服务端；用户必须经受控渠道保存和分发。
- 服务端对收到的公钥 PEM 解码，解析 SubjectPublicKeyInfo，强制验证为 `*ecdsa.PublicKey` 且曲线为 P-256；随后重新编码成规范 DER/PEM 后入库。
- 公钥指纹是规范 SPKI DER 的 SHA-256 小写十六进制值。指纹可在状态页展示并写入审计记录，不包含秘密。
- `challenge_id` 固定为 16 个随机字节，nonce 固定为 32 个随机字节；两者都使用 RFC 4648 base64url 无填充规范编码，分别为 22 和 43 个字符。服务端拒绝非规范编码。
- ECDSA 签名为固定 64 字节 `r || s`：`r`、`s` 各是 32 字节无符号大端数，左侧补零。JSON 中使用无填充 base64url，长度必须为 86 个字符。服务端检查 `1 <= r,s < curve.N` 后调用 `ecdsa.Verify`。不强制 Low-S；一次性 challenge 已限制重放，Low-S 不是本协议的必要条件。

### 消息摘要

所有参与签名的字符串均为 UTF-8，行分隔符固定为单字节 LF (`\n`)，版本号为无前导零的十进制整数，指纹为上文的小写十六进制。消息只做一次 SHA-256，得到的 32 字节 digest 直接交给 ECDSA-P-256 的 digest 签名/验证接口；不得再做第二次哈希。

- 登录：`xirang-control-panel-login-v1\n<challenge_id>\n<nonce>\n<auth_version>\n<key_fingerprint>`，由当前私钥签名。
- 首次登记：`xirang-control-panel-bootstrap-v1\n<challenge_id>\n<nonce>\n<auth_version>\n<new_key_fingerprint>`，由待登记的新私钥签名，作为新密钥持有证明。
- 轮换授权：`xirang-control-panel-key-rotate-v1\n<challenge_id>\n<nonce>\n<auth_version>\n<key_fingerprint>\n<new_key_fingerprint>`，由当前私钥签名。
- 新密钥持有证明：`xirang-control-panel-new-key-proof-v1\n<challenge_id>\n<nonce>\n<auth_version>\n<new_key_fingerprint>`，由待登记的新私钥签名。

每类消息使用独立的 domain prefix。Challenge 的服务端 `purpose` 检查必须与消息 prefix 同时匹配，不能把一种用途的 challenge 用在另一种接口。

## Challenge 状态机

挑战有效期为 2 分钟，服务端用 `crypto/rand` 生成随机 ID 和 nonce，并在 SQLite 记录其用途、签发时 `auth_version`、当前/目标密钥指纹和客户端 IP。`client_ip` 只用于来源限流、pending 计数与审计，不参与签名消息、challenge 认证条件或 Session 绑定；改变客户端 IP 本身不能使有效签名失效。

创建 challenge、清理旧记录、统计当前来源及全局未完成 challenge 数、判断上限和插入新行必须在同一个 SQLite 写事务中完成，使用立即取得写锁的事务模式或等价原子 SQL，避免并发请求同时越过 pending 上限。当前版本仅支持一个服务进程和单副本 SQLite。

| 用途 | 签发条件 | 绑定字段 | 消费方式 |
|---|---|---|---|
| `LOGIN` | `KEY_ACTIVE` | 当前 `auth_version` 与 `key_fingerprint` | 当前私钥签名有效后签发会话 |
| `BOOTSTRAP` | `PASSWORD_BOOTSTRAP` | 当前 `auth_version` 与候选 `new_key_fingerprint` | 初始化密码和新私钥持有证明均有效后登记 |
| `KEY_ROTATE` | 已认证且 `KEY_ACTIVE` | 当前 `auth_version`、当前指纹与候选新指纹 | 当前私钥签名和新私钥持有证明均有效后 CAS 更新 |

消费必须是单条原子条件更新（可用 SQLite `UPDATE ... RETURNING`）：只在 ID、用途、未消费、未过期条件全部满足时设置 `consumed_at` 并取回 challenge 数据。随后比较 challenge 中的 `auth_version`/指纹与当前数据库值，再验证签名。任何签名失败也保持 challenge 已消费。禁止先 `SELECT`、验证成功后再更新消费状态。

每个接口 body 限制为 8 KiB；公钥 PEM 限制为 2 KiB，浏览器私钥文件限制为 16 KiB；挑战 ID、nonce、签名均严格验证固定长度和 canonical base64url。

## 首次登记流程

1. `GET /api/v1/auth/status` 返回 `PASSWORD_BOOTSTRAP` 或 `KEY_ACTIVE` 状态及（若存在）公钥指纹，不返回密码或公钥正文。
2. 首次引导页面调用安全随机源生成 P-256 密钥对，生成 PKCS#8 PEM 并触发下载。前端不以“我已保存”复选框作为成功条件。
3. 释放最初生成的密钥对象后，要求用户重新选择刚下载的 PEM。前端从文件重新解析私钥，计算公钥和指纹，并确认签名能通过本地解析；不声称浏览器能可靠擦除所有字符串/垃圾回收副本。
4. 前端用新公钥申请 `BOOTSTRAP` challenge，提交初始化密码、公钥、challenge ID 和新私钥持有证明。
5. 服务端校验 `auth_state`、密码、challenge 版本/用途/候选指纹及 PoP；在单一数据库事务中用 `auth_state='PASSWORD_BOOTSTRAP' AND public_key_pem IS NULL AND auth_version=?` 条件写入公钥与指纹、把状态改为 `KEY_ACTIVE`、把密码哈希设为禁用标记，并通过同一 CAS/事务返回递增后的 `auth_version`。只有一个并发首次登记可以成功。
6. 成功后仅用事务返回的 `auth_version` 签发 Cookie Session 并写审计记录；禁止在提交后重新读取“当前最新版本”来生成 Session。若期间版本再变化，该 Session 必须保持旧版本并在后续请求中失败。

## 日常登录流程

1. 用户选择私钥 PEM；浏览器限大小读取并解析，不保存到 `localStorage`、`IndexedDB`、URL 或 DOM。
2. `POST /api/v1/auth/challenges/login` 创建 `LOGIN` challenge，响应包含 ID、nonce、签发时版本、当前密钥指纹和过期时间。
3. 浏览器按上述登录消息计算一次 SHA-256，并使用当前私钥产生 raw `r || s` 签名；提交给 `POST /api/v1/auth/login`。
4. 服务端原子消费 challenge，校验状态、版本、指纹、公钥曲线和签名；仅当管理员当前版本仍等于 challenge 的 `auth_version` 时签发 Session，Session 必须使用 `challenge.auth_version`。禁止验证成功后重新读取最新版本再签发；若并发轮换先完成，旧 challenge 登录失败或得到旧版本且立即无效的 Session。

认证失败使用通用响应。Challenge 过期、已消费、用途/版本/指纹不匹配、曲线错误、签名错误都拒绝。challenge、签名、私钥和密码内容不得进入应用日志或错误消息。

## 密钥轮换

密钥轮换属于重新认证，不能仅凭被 HTTP 窃听的 Session + CSRF 完成：

1. 操作者重新选择当前私钥文件。
2. 浏览器生成新密钥并下载新的 PEM，随后释放生成状态并要求操作者重新选择该新文件；从重新导入的文件派生公钥、计算指纹，避免下载内容与提交公钥不一致。
3. 浏览器以当前 Session + CSRF 调用 `POST /api/v1/auth/challenges/rotate`，提交候选新公钥。服务端验证并绑定当前 `auth_version`、当前指纹和候选新指纹。
4. 操作者当前私钥签署轮换授权消息，新私钥签署 PoP 消息。`PUT /api/v1/auth/key` 必须同时验证 Session + CSRF、challenge、版本、两把公钥指纹及两份签名。
5. 数据库使用 CAS 更新并在同一事务返回新 `auth_version`：仅当 `auth_state='KEY_ACTIVE'`、`auth_version` 和当前指纹仍与 challenge 完全相同时替换公钥/指纹并递增版本；检查 `RowsAffected == 1`。失败返回冲突并要求重新开始，不允许最后写入覆盖。
6. 成功后只能用该 CAS/事务返回的新版本签发当前浏览器的 Cookie Session，禁止提交后重新读取“最新版本”。
7. 版本递增撤销所有其他旧会话和旧密钥；当前浏览器得到新版本 Cookie。所有共用密钥的人必须通过受控渠道获取新文件。

如果 Session 被动泄漏，持有人可在会话有效期内执行其他完整权限操作，但没有当前私钥便不能把认证根密钥替换为自己的密钥。主动 MITM 仍可窃取私钥，HTTP 无法提供对此的保护。

## HTTP 接口

- `GET /api/v1/auth/status`：返回认证状态和可选的公钥指纹。
- `POST /api/v1/auth/challenges/login`：创建 `LOGIN` challenge，公开接口但有独立请求限流。
- `POST /api/v1/auth/login`：仅接受 `{challenge_id, signature}`，不接受密码。
- `POST /api/v1/auth/challenges/bootstrap`：仅在 `PASSWORD_BOOTSTRAP` 接受 `{public_key_pem}`，绑定候选指纹并创建 `BOOTSTRAP` challenge。
- `POST /api/v1/auth/bootstrap`：接受 `{password, public_key_pem, challenge_id, proof_signature}`；仅首次引导有效。
- `POST /api/v1/auth/challenges/rotate`：认证并通过 CSRF 校验，接受新公钥并创建 `KEY_ROTATE` challenge。
- `PUT /api/v1/auth/key`：认证并通过 CSRF 校验，接受 `{challenge_id, new_public_key_pem, current_signature, proof_signature}`。
- `POST /api/v1/auth/logout`：仅清除当前浏览器的 session/CSRF Cookie 并记录 `auth.logout_current`，不递增全局 `auth_version`；已复制的 Cookie 和其他浏览器会话继续有效直至过期/撤销。
- `POST /api/v1/auth/logout-all`：要求认证与 CSRF 校验，递增全局 `auth_version` 使所有会话失效，并清除发起请求的浏览器 Cookie，记录 `auth.logout_all`。
- `PUT /api/v1/auth/password` 和密码修改 UI 移除。
- Browser auth 成功响应不在 JSON 中回显 JWT 或 CSRF token；前端只用当前同源 Cookie。现有鉴权中间件在每个受保护 HTTP 请求上读取数据库对比 `auth_version`，此行为必须保留并测试。任务 SSE 使用同源 Cookie。

## 会话、限流与代理来源

- HTTP 下会话 Cookie 保持 `HttpOnly=true`、`Secure=false`（仅因部署限制）、`SameSite=Strict`、`Path=/`、不设 `Domain`。登录、引导、轮换都重新设置会话和 CSRF Cookie；普通退出仅清除当前浏览器 Cookie，全局退出才递增 `auth_version` 并撤销所有会话。
- JWT TTL 默认及上限均为 30 分钟；`JWT_TTL` 超过 30 分钟时配置加载拒绝启动，不增加 refresh token。启动时强制校验上限，而不只依赖文档约定。缩短时长只能限制被动窃取 Session 的可用窗口，不能防止当前窗口内的管理员操作。
- 认证中间件对每个受保护 HTTP 请求从数据库校验 `auth_version`；SSE 使用同源 Cookie，在连接建立后持续检查过期时间和当前版本，最多每 30 秒重新验证一次（有事件时可提前检查）；版本撤销或过期后关闭流，撤销延迟上限为 30 秒。
- Challenge 创建本身单独限流，不依赖“失败次数”限流：默认每 IP 每分钟 10 次、每 IP 最多 5 个未完成 challenge、全局最多 1000 个未完成 challenge；具体值可配置。达到上限返回 429/503，不插入新记录。
- 签名失败只触发按解析后来源 IP 计数的进程内限流/有界退避；不得持久化 `admin` 锁定状态、不得让一个来源锁住其他来源，也不得在签名失败时递增 `auth_version`。失败审计受限流约束，避免数据库被日志写入耗尽。
- 限流 IP 只可来自安全解析的 `RemoteAddr` 或显式配置的可信代理。路由器必须总是显式配置 Gin trusted proxies：没有 `TRUSTED_PROXIES` 时禁用所有转发头信任并使用 `RemoteAddr`；有配置时仅信任配置的 CIDR，代理必须清洗客户端传入的 XFF。无效代理配置应导致启动失败，禁止直接相信任意 `X-Forwarded-For`。
- `client_ip` 只参与上述来源限流、pending 计数和审计，不参与签名、密钥选择、Session 认证或 IP 绑定。
- 审计记录初始化、成功/失败登录、限流、密钥轮换和两种退出操作；不记录密码、私钥、nonce 或签名。认证相关响应、登录 HTML 和静态签名逻辑资源设置 `Cache-Control: no-store`。

## 前端密码学与 XSS 防护

- 登录页根据 `/auth/status` 显示首次密钥登记或私钥文件登录；首次登记和轮换均要求下载后重新选择 PEM 验证。设置区提供独立的密钥轮换、“退出当前浏览器”和“退出所有会话”操作。
- 随项目发布固定版本、固定来源并附许可证的成熟 P-256 JavaScript 库；不从 CDN 加载，不自行实现椭圆曲线或伪随机数。
- 私钥生成必须只使用 `crypto.getRandomValues()`；该 API 不可用时立即失败，不回退到 `Math.random()`、时间戳或自行实现的 PRNG。ECDSA 签名优先使用 RFC 6979 deterministic ECDSA；若库依赖随机签名 nonce，必须使用上述 CSPRNG 且通过固定互操作向量验证。
- 选择库时记录版本、源码/发布物 hash 和许可证；升级必须重跑 Go ↔ JS 双向固定向量测试。测试比较“JS 签名、Go 验证”和“Go 签名、JS 验证”，不要求不同随机签名每次字节相同。
- CSP 禁止第三方脚本、inline/eval script：`default-src 'self'`、`script-src 'self'`、`object-src 'none'`、`base-uri 'none'`、`frame-ancestors 'none'`、`form-action 'self'`、`connect-src 'self'`、`img-src 'self' data:`。当前界面使用大量 inline style，暂保留 `style-src 'self' 'unsafe-inline'`，但不得允许 inline script 或 `unsafe-eval`；删除登录表单上的 inline event handler 和 `javascript:` action。
- 保留 `X-Content-Type-Options: nosniff`、`X-Frame-Options: DENY`，将 `Referrer-Policy` 设为 `no-referrer`。这些控制改善应用自身 XSS/嵌入防护，但不能抵御会改写 HTTP 响应的主动 MITM。
- 私钥文件在前端限于 16 KiB；解析失败时不将文件内容写入 console、DOM、URL 或错误消息。签名后清除文件 input 并尽力清理二进制缓冲区，但不宣称 JavaScript 可可靠擦除字符串或 GC 副本。

## 运维恢复

若所有私钥副本丢失，运维停止服务，使用 SQLite backup 能力创建一致备份，再执行受控恢复：清空公钥与指纹、将 `auth_state` 置为 `RECOVERY_PENDING`、将密码哈希设为 `__PENDING_INIT__`、递增 `auth_version` 并清除所有 `auth_challenges`。服务启动后仅在该状态下用 `ADMIN_INIT_PASSWORD` 重建引导哈希，转成 `PASSWORD_BOOTSTRAP` 并写入 `auth.recovery_bootstrap` 审计事件。普通手工清空公钥不会恢复密码登录。

部署文档须说明共享密钥不可逐人追责、文件保存/分发、轮换、恢复、HTTP 被动窃听和主动 MITM 的不同风险，并建议只从受控内网访问。

## 验证标准

- 单元与数据库测试：正确/错误签名、错误长度、非 P-256、错误 PEM、r/s 越界、非 canonical base64url、超大请求、过期挑战、重复消费、purpose 不匹配、版本变化、指纹变化。
- 并发测试：100 个 goroutine 同时提交一个登录 challenge 只能一个成功；两个相同 `auth_version` 的轮换只能一个 CAS 成功；并发首次登记只能一个成功；并发 challenge 创建不能突破 per-IP/global pending 上限。
- 轮换/引导测试：登录签名有效但缺当前轮换签名则拒绝；新公钥无 PoP 或 PoP 不匹配则拒绝；重新导入下载 PEM 后导出的指纹必须与待登记公钥一致；旧 key/challenge 在版本变化后失败。
- 状态与会话测试：公钥存在时密码永远不能登录；bootstrap 成功禁用 password hash；恢复只通过 `RECOVERY_PENDING` 重建；所有状态字段组合、缺失 Secret、无效公钥和 SQLite 版本不足均在 HTTP listener 建立前失败；认证 middleware 每个请求校验版本。
- Session 版本测试：登录只能签发 challenge 记录中的 `auth_version`；bootstrap/rotation 只能使用 CAS/事务返回的新版本；测试并发版本变化时不会重新读取最新版本为旧 challenge 签发新权限 Session。验证当前浏览器退出不撤销其他 Session，全局退出撤销全部 Session。
- SSE 在会话过期/版本撤销后 30 秒内关闭；JWT TTL 超过 30 分钟时应用启动失败；Cookie、no-store 与只在 Cookie 中返回凭证的响应正确。
- 限流/来源测试：challenge flood 触发 per-IP/global/pending 上限；pending 统计和创建原子执行；伪造 `X-Forwarded-For` 在未配置可信代理时不能绕过限流；单一来源失败不会锁住其他来源或写入全局锁定状态；只接受配置 CIDR 的代理转发地址。
- 审计和前端测试：审计不泄漏凭据；固定 Go↔JS 双向签名向量；浏览器文件重选流程、HTTP 内网首次登记/登录/轮换/恢复；私钥不进入持久化存储、URL、DOM、console 或 API 请求。
- 在 `control_panel/backend` 目录运行 `go test ./...`，并验证静态 JS、CSP、部署模板和 Helm README。
- 更新 `control_panel/deploy/README.md`、`control_panel/charts/control-panel/README.md` 与 Helm 默认配置，记录新的 cookie/session/challenge 限值、代理设置和 HTTP 风险。

## 不在范围内

- 多用户、角色、用户管理或个人级审计归因。
- WebAuthn/FIDO2、硬件安全密钥、密码保护的私钥文件、私钥云同步。
- 为 HTTP 增加自定义加密传输协议，或声称 ECDSA challenge 消除了 HTTP 中间人风险。
