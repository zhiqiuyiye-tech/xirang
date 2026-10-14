# NFS 虚拟盘回收：按手册执行

## 回收顺序

`storage_delete_lv` 与 `storage_reclaim_nfs` 共用《NFS创建流程》第 8 节的底层回收顺序：

1. 校验 worker、VG/LV 名称和真实设备身份，检测宿主机挂载点，拒绝系统根目录及配置的保护目录。
2. 仅移除目标挂载路径的 `/etc/exports` 条目，执行 `exportfs -arv`。
3. 对目标宿主机挂载执行普通 `umount`，多挂载点按深层优先处理。busy 或其他卸载错误立即停止，不强制或延迟卸载。
4. 按目标设备主次号精确匹配 `/proc/*/mountinfo`，找到仍保留该文件系统的进程及挂载命名空间，按命名空间去重。只读取与目标设备有关的持有者身份，不把无关系统组件的 hostPath 或其他卷当成占用。
5. 固定持有者的 PID/starttime、namespace/root 和挂载证据，由可信宿主机执行器进入对应 namespace/root，核对设备与 mount ID 后执行 flags=0 的普通 `umount2`。不重启 Promtail，不删除 Pod，不终止业务进程。
6. 再次确认目标设备身份不变、进程可见的目标挂载消失、`dmsetup` Open Count=0，才允许 `lvremove`。打开计数非零时保留卷并报告原因，不以“没有找到 PID”作为删除依据。
7. LV 删除成功后清理该设备的 `/etc/fstab` 条目。任务日志保留每一步的真实结果；后续配置清理失败会报告部分已完成操作。

前置释放验证之后若竞态导致首次 `lvremove` 再次明确报 filesystem-in-use，最多额外进行一轮精确设备检查/释放和一次删除重试。传输错误或其他 LVM 错误不触发盲目重试。

## 操作者必须确认的前提

**该回收流程是不可逆的底层删除操作，不再自动检查 Kubernetes Pod/PVC/PV 是否仍引用该卷。** `umount` 成功、Open Count=0 并不证明一个闲置 Notebook 的 PVC 不再需要其数据，也不保证未来重新挂载的数据安全。

管理员在点击删除/回收或提交 API 请求前，必须确认：

- 目标卷及数据可以永久丢弃，业务已停用；没有其他客户端、调度器、特权程序或外部管理员并发修改相关挂载/LVM。
- 操作的是正确的节点、VG/LV 和设备；不能把历史 PID 或 Pod 名当作本次占用证据。
- 维护范围涵盖程序无法完全枚举的引用；进程扫描不是完整的内核命名空间证明，最终设备打开计数与实际命令结果仍须核实。

前端保留不可撤销确认，明确提示上述前提。不再出现维护模式勾选框，不再因为全局 Pod 列表、维护开关或工作负载许可名单阻止该手册回收流程；接口亦不会自动删除 Pod/PVC。

## Linux 5.10 兼容性与工具

回收不依赖 Linux 6.12 的 `NS_MNT_GET_INFO/NEXT/PREV`，Linux 5.10 节点无需升级内核来执行该流程。节点需具备：

- 可信宿主机 Python 3、GNU coreutils `timeout`、LVM/device-mapper 工具，以及 `findmnt`、普通 `umount`、`exportfs`、`sed`。
- Linux 宿主机 root 及读取目标进程证据、进入其 mount namespace/root、普通卸载所需权限。
- 单个后端实例、同一物理节点不重复注册为多个 worker。应用内 worker 串行锁不约束外部操作者。

实际持有者挂载可以是 shared；程序按手册普通卸载，不为了删除修改任何传播设置。仍校验目标设备、保护路径、PID/root/mount 身份，拒绝层叠或子挂载等不能明确定位的复杂结构；普通卸载被内核拒绝时停止。

`SHARED_HOST_MAINTENANCE_ENABLED`、`NAMESPACE_CLEANUP_ALLOWLIST` 与旧 `maintenance_confirmed` 请求字段仅保留旧配置/客户端兼容性，**不再作为删除或 NFS 回收的启用/许可条件**。未传维护字段也采用同一手册流程。

`NAMESPACE_CLEANUP_TIMEOUT` 和 `NAMESPACE_UNMOUNT_TIMEOUT` 继续限制释放阶段及单个 helper 的时间预算。resize 的业务使用及保守检查不因删除流程改变而放宽。

## 执行状态不明

远端命名空间清理在改变挂载前创建 `/run/control-panel-storage-recovery.uncertain`。超时、连接丢失或无法确认远端执行器退出时，保留标记并隔离该 worker，停止后续存储命令。

只有维护人员确认 helper 已退出、挂载/设备状态核实后才可解除标记。不可为继续删除直接清除标记；无法终止的内核等待需要节点维护。已完成的宿主机卸载、导出修改或部分容器卸载不会因任务失败自动恢复，需依据任务日志处理。

## 验收与发布边界

本地 Go/Python/前端测试仅验证协议、流程和纯解析/保护条件。真实 PID/root 上下文、普通卸载、共享传播、busy 及 helper 异常终止，仍须在隔离 Linux 测试环境验收；不能在生产卷上做破坏性测试，也不能宣称 Windows mocked 测试证明现场删除成功。

Git 提交或推送不等于更新运行中的镜像/Deployment。Python 执行器和前端资源嵌入 Go 后端，需要重新构建并部署后端后修改才生效。手工步骤见 `NFS创建流程.md` 第 8.2.1 节。
