# 控制面板 - 子项目 #1 基础层 设计文档

- **日期：** 2026-07-23
- **范围：** control_panel/backend 基础后端（Worker 管理 + 凭证 + SSH + 任务引擎 + 面板认证）
- **状态：** 待评审

## 1. 背景与目标

### 1.1 总体项目

"无代理（Agentless）"架构的 K8s + 存储控制面板，类似 Ansible 工作模式：Master 节点部署一个服务 Pod，通过免密/密码 SSH 到 Worker 节点执行底层存储操作（LVM/NFS），并直接调 K8s API 下发 SVC 与 NetworkPolicy。优点是架构极简、部署负担小；代价是该服务掌握所有 Worker 的 root 权限，需特别保护密钥。

### 1.2 子项目分解

总体项目按以下顺序分多个子项目交付，每个子项目独立 spec -> plan -> 实现：

| # | 子项目 | 交付 | 依赖 |
|---|--------|------|------|
| **1** | **基础层（本文档）** | Worker CRUD + 加密凭证 + SSH 客户端/连接池 + 两个设密码接口 + 任务引擎 + 面板认证 + Go 骨架 + 基础 Dockerfile | - |
| 2 | K8s 操作 | SVC + NetworkPolicy 创建/删除（client-go，集群内）| #1 |
| 3 | LVM/NFS 生命周期 | provision + reclaim + 失败回滚 | #1 |
| 4 | 丰富前端 | 内嵌 SPA：节点拓扑、实时进度、凭证表单、操作历史 | #1–3 API |
| 5 | 部署加固 | RBAC、SSH-key Secret 挂载、Service/Ingress、install.sh、镜像打磨 | #1–4 |

理由：#1 是承重层（所有 SSH 长操作都要靠它），必须先做扎实。K8s 与 LVM/NFS 都复用 #1 的任务引擎做进度流。前端消费所有 API，故在其后。部署加固最后，因 RBAC/Secret 反映最终形态。

### 1.3 本期目标

交付基础后端，使后续子项目能在其上增量开发：能注册 Worker、安全存储并使用其凭证、经 SSH 执行命令并流式记录进度、提供面板自身认证。

### 1.4 已确认约束（跨子项目，本文档记录以指导 #2/#3）

- **SVC/NetworkPolicy 跟随 Pod 生命周期：** 子项目 #2 创建资源时设 `metadata.ownerReferences` 指向目标 Pod，K8s 原生 GC 在 Pod 销毁时自动清除被拥有的资源。参考 `control_panel/docs/k8spod端口映射手册.md` 已展示该模式。
- **LVM 空间可回收：** 子项目 #3 实现 provision 与 reclaim 互为逆操作（reclaim 按反序：删 exports 行 -> exportfs -> umount -> lvremove -> 清 fstab）。参考 `control_panel/docs/NFS创建流程.md` 第 8 节。失败回滚由任务引擎的"已执行步骤"跟踪驱动。

这两条约束对 #1 无额外实现要求（#1 任务引擎已内置步骤跟踪以支持回滚），仅作为后续设计依据记录。

## 2. 运行形态与技术选型

- **形态：** 单体 Go 服务，单 Pod Deployment。进程内含 HTTP API + 任务引擎 + SSH 客户端。
- **存储：** SQLite 文件放 PVC；敏感字段 AES-256-GCM 加密；主密钥从 K8s Secret 注入环境变量。
- **语言/库：**
  - Go + Gin（HTTP）。
  - `golang.org/x/crypto/ssh`（SSH）。
  - `modernc.org/sqlite`（纯 Go，无 CGO，静态二进制，镜像小）。
  - `golang-jwt/jwt/v5`（JWT）。
  - `golang.org/x/crypto/bcrypt`（管理员密码哈希）。
- **配置：** 全走环境变量，无配置文件。

选 modernc.org/sqlite（纯 Go）而非 CGO 版：避免构建环境依赖 gcc、镜像更小、交叉编译友好，契合"单 Pod 全功能、部署极简"。性能对低并发管理负载无感知。

## 3. 目录结构

```
control_panel/backend/
  cmd/server/main.go          # 入口：加载配置、初始化 db/crypto/ssh/taskengine/auth、起 HTTP
  internal/
    config/                   # 从环境变量读配置（主密钥、JWT secret、DB路径、监听端口等）
    db/                       # SQLite 连接、迁移、模型、查询
    crypto/                   # AES-256-GCM 加解密封装
    auth/                     # 管理员登录、JWT 签发与校验中间件
    ssh/                      # SSH 客户端抽象 + 连接池
    tasks/                    # 任务引擎：Task/Step 记录、goroutine 调度、进度流
    workers/                  # Worker 节点 CRUD、凭证管理、设密码逻辑
    api/                      # HTTP handlers 与路由（Gin）
  migrations/                 # SQL 迁移脚本
  Dockerfile
  go.mod
```

分层依赖（单向）：`api` -> `workers`/`tasks` -> `ssh`/`db`/`crypto`/`auth` -> `config`。

## 4. 数据模型（SQLite 表）

```sql
admin
  id              INTEGER PRIMARY KEY
  username        TEXT UNIQUE NOT NULL
  password_hash   TEXT NOT NULL          -- bcrypt
  created_at      TIMESTAMP NOT NULL

worker_nodes
  id              INTEGER PRIMARY KEY
  name            TEXT NOT NULL
  host            TEXT NOT NULL
  port            INTEGER NOT NULL DEFAULT 22
  username        TEXT NOT NULL DEFAULT 'root'
  auth_mode       TEXT NOT NULL           -- 'key' | 'password' | 'both'
  enc_password    TEXT                    -- AES-256-GCM, 可空
  enc_private_key TEXT                    -- AES-256-GCM, 可空
  status         TEXT NOT NULL DEFAULT 'unknown'  -- 'online' | 'offline' | 'unknown'
  last_seen_at    TIMESTAMP
  created_at      TIMESTAMP NOT NULL
  updated_at      TIMESTAMP NOT NULL

tasks
  id              INTEGER PRIMARY KEY
  type            TEXT NOT NULL           -- 'set_root_password' 等；后续子项目注册更多
  target_kind     TEXT NOT NULL           -- 'worker' | 'k8s' | ...
  target_id       INTEGER NOT NULL
  status          TEXT NOT NULL           -- 'pending' | 'running' | 'succeeded' | 'failed' | 'rolled_back'
  params_json     TEXT NOT NULL
  error           TEXT
  created_at      TIMESTAMP NOT NULL
  started_at      TIMESTAMP
  finished_at     TIMESTAMP

task_steps
  id              INTEGER PRIMARY KEY
  task_id         INTEGER NOT NULL REFERENCES tasks(id)
  seq             INTEGER NOT NULL
  name            TEXT NOT NULL
  status          TEXT NOT NULL           -- 'pending' | 'running' | 'succeeded' | 'failed'
  stdout          TEXT
  stderr          TEXT
  started_at      TIMESTAMP
  finished_at     TIMESTAMP
  error           TEXT

audit_log
  id              INTEGER PRIMARY KEY
  actor           TEXT NOT NULL           -- 'admin'
  action          TEXT NOT NULL
  target          TEXT
  params_json     TEXT
  result          TEXT NOT NULL           -- 'success' | 'fail'
  at              TIMESTAMP NOT NULL
```

凭证字段（`enc_password`、`enc_private_key`）只在内存按需解密，绝不落日志或审计明文。

## 5. SSH 客户端与连接池

- `ssh.Manager`：per-worker 维护一个 `[]*ssh.Client` 池（默认 3 连接）。
- 取连接前做 `Ping`，坏连接剔除重建。
- 空闲超时 5 分钟关闭。
- 认证顺序：私钥（DB 解密）-> 密码（DB 解密）-> 报错。两种都配则先试密钥、失败回退密码。
- 接口：
  - `Run(ctx, workerID, cmd) (stdout, stderr string, exitCode int)`
  - `RunSteps(ctx, workerID, steps []Step, reporter Reporter)` 供任务引擎流式记录每步。
- 私钥/密码解密仅在建立连接瞬间，连接对象不持久化明文。

## 6. 任务引擎（进程内，方案 A）

- `tasks.Engine.Submit(type, params) -> taskID`：写 task 记录（pending），起 goroutine 执行已注册 handler。
- handler 实现 `interface { Run(ctx, task, reporter) error }`，按 type 注册。本期仅注册 `set_root_password`；K8s、LVM/NFS 子项目后续注册各自的。
- `reporter` 提供 `Step(name)`、`Write(stdout/stderr)`、`SetStatus`，每步落 `task_steps` 表。
- 进度暴露：
  - `GET /api/v1/tasks/:id`（全量）
  - `GET /api/v1/tasks/:id/stream`（SSE 推步骤完成事件）
- 失败标记 failed + 错误信息。
- 回滚能力由各 handler 自行实现；引擎提供"已执行步骤"列表供 handler 反向 undo（LVM/NFS 子项目用）。
- **重启恢复：** 启动时扫描 `tasks` 表，将所有 `status='running'` 的任务（含其 `task_steps` 中 `status='running'` 的步骤）标记为 `failed`，`error='interrupted by restart'`，并写 `finished_at`。本期不尝试重跑或回滚被中断的任务（多步操作的中间状态可能已部分生效，自动回滚风险高），仅如实记录中断状态，由管理员人工复核后决定是否重试或手动清理。
- **`target_id` 语义：** 指向被操作资源的表内主键。本期 `target_kind='worker'` 时指向 `worker_nodes.id`。后续子项目的 `target_kind` 取值与对应指向由该子项目的 spec 定义。

## 7. 面板认证（JWT 单管理员）

- 管理员账号密码存 SQLite，密码 bcrypt 哈希。
- 首次启动用 `ADMIN_INIT_PASSWORD` 种默认管理员（用户名固定 `admin`）。
- 登录换发 JWT token，后续 API 带 Bearer token。
- JWT 默认 12h 过期。
- 所有写操作落 `audit_log`。

## 8. API 表面（本期）

```
POST   /api/v1/auth/login                              {username,password} -> {token}
GET    /api/v1/workers                                 列表
POST   /api/v1/workers                                 创建(name,host,port,username)
GET    /api/v1/workers/:id
PUT    /api/v1/workers/:id                             更新基本信息
DELETE /api/v1/workers/:id
POST   /api/v1/workers/:id/test                        测试连接(密钥优先/密码回退)
POST   /api/v1/workers/:id/credentials/private-key     上传私钥(加密存DB)
POST   /api/v1/workers/:id/credentials/password        【接口一】设面板侧登录密码(加密存DB)
POST   /api/v1/workers/:id/root-password              【接口二】推送改Worker实际root密码(chpasswd+同步存DB)
GET    /api/v1/tasks                                   任务列表
GET    /api/v1/tasks/:id                               任务详情+步骤
GET    /api/v1/tasks/:id/stream                        SSE 进度流
GET    /api/v1/audit-log                               审计日志
```

### 8.1 接口一：面板侧登录密码

- `POST /api/v1/workers/:id/credentials/password`
- body: `{ "password": "..." }`
- 仅加密存入 `enc_password`，不改 Worker 机器。
- 立即影响后续 SSH 回退认证。
- 同步设 `auth_mode` 为 `password` 或 `both`（若已有私钥）。

### 8.2 接口二：Worker root 密码

- `POST /api/v1/workers/:id/root-password`
- body: `{ "password": "..." }`
- 起任务，SSH 执行 `echo "root:NEWPASS" | chpasswd`。
- 成功后把新密码加密写入 `enc_password`（即同步执行接口一的效果）。
- 前置条件：当前已能 SSH 连上该 Worker（否则无法推送）。

## 9. 安全

- 从 K8s Secret 注入的环境变量：
  - `AES_KEY`（32 字节，base64 编码）--主密钥
  - `JWT_SECRET`
  - `ADMIN_INIT_PASSWORD`--首次启动种管理员
- 启动校验三者存在，缺失拒绝启动。
- 管理员密码 bcrypt。
- 私钥/密码解密仅在 SSH 连接建立瞬间，连接对象不持久化明文。
- 凭证明文不落日志、不落审计。
- 所有写操作落 `audit_log`。
- **SSE 端点认证：** 浏览器 EventSource 无法设置自定义请求头，故 `GET /api/v1/tasks/:id/stream` 除支持 Bearer 头外，额外接受 `?token=<jwt>` 查询参数。查询参数 token 仅限该 SSE 端点使用，其他端点一律只认 Bearer 头。查询参数走 HTTPS（子项目 #5 Ingress 启用 TLS）以避免 token 出现在明文链路。

## 10. 本期交付边界

**做：**
- Go 项目骨架 + 配置加载
- crypto 包（AES-256-GCM）
- auth（JWT 单管理员 + 中间件）
- Worker CRUD
- 凭证管理（私钥上传、面板密码、root 密码推送）
- SSH 客户端 + 连接池
- 任务引擎（Task/Step、goroutine、SSE 进度流）
- 审计日志
- 基础 Dockerfile
- 单元测试（crypto、ssh 认证顺序、任务引擎、auth 中间件等）

**不做（后续子项目）：**
- K8s SVC/NetworkPolicy 操作（子2）
- LVM/NFS 生命周期与回滚（子3）
- 前端（子4）
- RBAC/install.sh/Service/Ingress/Secret 挂载细节（子5）

## 11. 风险与对策

| 风险 | 对策 |
|------|------|
| 掌握所有 Worker root 权限，面板被突破=集群被突破 | JWT 单管理员 + bcrypt + 凭证 AES 加密 + 主密钥在 Secret 不落盘 + 审计日志；后续子5 加 RBAC 限制 ServiceAccount 权限 |
| 单 Pod 重启中断进行中的任务 | 本期接受（单 Pod 部署）；任务重启后状态为 running 的标记为 failed；后续如需可演进为持久化队列 |
| SQLite 多副本不可用 | 单 Pod Deployment，本期可接受 |
| SSH 高频握手延迟 | per-worker 持久连接池 |
| 密钥泄露 | 主密钥走 K8s Secret 环境变量；DB 只存密文；日志无明文 |
