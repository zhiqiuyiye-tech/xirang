# Worker 与 Notebook GPU / NPU 显示

## 显示内容

- Worker 列表展示型号、物理卡数量、工具采集的设备数量，以及已使用 / 总可分配设备数。
- Worker 页面支持刷新节点与卡信息，进入页面时自动查询。
- 端口映射 Notebook 列表和弹窗显示分配设备数，悬浮提示具体 Kubernetes 资源类型。
- 尚未调度的 Notebook 标记“未分配（申请数量）”；已结束的 Notebook 标记“已释放（配置数量）”。

## 数据来源与统计口径

- 沿用 Worker SSH 凭证执行只读的 `npu-smi info` 和 `nvidia-smi --query-gpu=uuid,name --format=csv,noheader,nounits`。
- 昇腾物理卡按 NPU ID 去重，设备按 Phy-ID 去重；例如 npu-smi 25.5.5 显示 NPU 0–7、Phy-ID 0–15，即 8 张 Ascend910 物理卡、16 个设备。
- NVIDIA 物理卡和设备按 GPU UUID 去重。
- Worker 已使用数为绑定到该节点的全部命名空间非终态 Pod 的有效设备申请，总数为节点 Kubernetes allocatable 中计数型加速设备资源总和。分子与分母使用相同单位，不与物理卡数混用。
- Notebook 按有效设备申请计算：逐资源 requests 优先，缺少时使用 limits；普通容器累加，init 使用调度峰值，支持可重启 init 和 Pod overhead。
- 识别 NVIDIA、AMD、海光、寒武纪及昇腾计数资源；排除显存、核心、百分比、共享份额等非设备计数单位。
- Worker 优先以主机地址匹配 Kubernetes InternalIP，再尝试节点名称，拒绝地址冲突与歧义。

## 厂商查询隔离与错误处理

- 各设备工具分别记录输出和退出码，单个工具失败不会丢弃其他工具成功的型号、物理卡及设备信息。
- `status=partial` 表示部分厂商采集失败；成功结果仍返回，失败工具、退出码和输出摘要作为诊断展示。完整物理卡总数 `total` 保持 null，避免将部分结果误当成整机总数。
- 已登录的管理界面显示 SSH 具体失败阶段、超时预算及命令错误摘要。单个错误输出流最多 512 个字符，保留 UTF-8；不持久化命令输出和凭证。
- SSH、设备工具、Kubernetes 权限或节点匹配失败时，对应未知数据不会伪装成 0。
- 驱动权限由管理员处理，面板不会 chmod、绕过权限或执行驱动安装。

## 超时与部署

- 独立的登录保护接口 `GET /api/v1/workers/accelerators` 避免设备探测阻塞节点配置操作。
- 每次请求最多并发探测 4 个 Worker；设备采集默认总预算 45 秒，可通过 `WORKER_ACCELERATOR_TIMEOUT` / Helm `config.workerAcceleratorTimeout` 配置。Kubernetes 统计超时 5 秒，两者并行。
- 心跳默认 30 秒，通过 `WORKER_HEARTBEAT_TIMEOUT` 配置；手动连接测试默认也为 30 秒。握手仍有独立 10 秒限制，心跳超时不会伪装成功。
- 用户提供的真实会话认证后耗时 16.6 秒且 exit=0，旧 15 秒心跳和 8 秒设备预算不足。加大预算容纳该延迟，不能据此判定远端 shell 启动慢的具体原因。
- 现有安装若显式配置旧心跳 15s，必须调整环境变量或 Helm values；原始 1.0.9 的设备预算硬编码 8 秒，新变量需要部署 1.0.10 或更新的二进制才有效。
- 不增加数据库迁移，不修改开发数据库。

## 验证

- `go test ./...`、`go vet ./...`。
- `node --check ../internal/api/web/app.js`、`npm test`（在 backend/web-build 执行）。
- 厂商退出码 126/127、双方成功或失败、实际双芯片布局、超时参数和真实 SSH 测试服务 17 秒响应的回归测试。
- 使用 Bash 执行真实探测脚本配合模拟厂商工具，验证一个工具失败仍保留另一工具成功数据。
- 自动化测试使用样例及 Kubernetes fake client；部署后的真实 Worker 查询和节点网络路径仍需确认。
