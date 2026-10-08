# Worker 与 Notebook GPU / NPU 显示

## 显示内容

- Worker 列表新增 GPU / NPU 列：各型号的物理卡数量、已使用 / 总共、采集来源及时间。
- Worker 页面新增“刷新节点与卡信息”，进入页面时也自动查询。
- 端口映射的 Notebook 列表和配置弹窗显示用卡数量，悬浮提示具体 Kubernetes 资源类型。
- 尚未调度的 Notebook 标记“未分配（申请数量）”；已结束的 Notebook 标记“已释放（配置数量）”。

## 数据来源与统计口径

- 通过已有 Worker SSH 凭证执行只读的 `npu-smi info`、`nvidia-smi --query-gpu=uuid,name --format=csv,noheader,nounits`。
- 昇腾卡按照 NPU ID 去重，避免将同一卡的芯片、进程或重复表格当成多张卡；NVIDIA 卡按照 GPU UUID 去重。
- Worker 总数为工具采集的物理卡数；已使用数为全部命名空间中绑定到节点的非终态 Pod 的有效卡资源申请，并非算力利用率或进程数量。
- Notebook 用卡数量按有效资源申请计算：逐资源优先 requests，缺少时使用 limits；普通容器累加，init 容器使用调度峰值，支持可重启 init 容器和 Pod overhead。
- 识别 NVIDIA、AMD、海光、寒武纪及昇腾的卡计数资源；排除显存、核心、百分比和共享份额等非卡计数单位。
- Worker 优先以主机地址匹配 Kubernetes InternalIP；匹配失败时允许节点名称匹配，但拒绝地址冲突和歧义。
- Kubernetes 可分配数量与物理卡数量不一致时额外展示可分配数量，提示可能存在共享或虚拟化。

## 边界与约束

- 卡信息使用独立、需登录的 `GET /api/v1/workers/accelerators` 接口，避免远程设备探测阻塞节点列表及配置操作。
- 每次请求最多并发探测 4 个 Worker，单节点 SSH 超时 8 秒；Kubernetes 统计超时 5 秒，两种查询并行执行。
- 不增加数据库迁移，不保存凭证或命令输出，不修改开发数据库。
- SSH、驱动、设备工具、Kubernetes 权限或节点匹配异常时对应数据展示“未知”，而非 0。
- 驱动输出无法识别时不会猜测型号和数量。不同版本的 `npu-smi` 若引入新表格格式，需要增加样例和解析测试。

## 方案选择

沿用已有 SSH 通道采集硬件，通过 Kubernetes 计算分配；前端异步补充卡信息。相比直接在 Worker 列表接口同步探测，此方式保持节点管理操作可用；相比新增常驻采集和存储体系，此次改动更小、无需迁移。

## 验证

- `go test ./...`
- `go vet ./...`
- `node --check ../internal/api/web/app.js`（在 backend/web-build 执行）
- `npm test`（在 backend/web-build 执行）

自动化测试使用设备输出样例和 Kubernetes fake client；真实 Worker 驱动输出及真实集群权限需在部署环境验证。
