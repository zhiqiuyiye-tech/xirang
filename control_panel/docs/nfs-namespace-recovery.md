# NFS 虚拟盘回收：按手册执行

## 回收顺序

`storage_delete_lv` 与 `storage_reclaim_nfs` 共用《NFS创建流程》第 8 节的底层回收顺序：

1. 校验 worker、VG/LV 名称和真实设备身份，检测宿主机挂载点，拒绝系统根目录及配置的保护目录。
2. 仅移除目标挂载路径的 `/etc/exports` 条目，执行 `exportfs -arv`。宿主机没有 `/etc/exports` 或没有 `exportfs` 时这两步直接跳过：无导出可撤销不是删除失败。文件存在时的 `sed` 失败仍然致命。
3. 对目标宿主机挂载执行普通 `umount`，多挂载点按深层优先处理。提示 `target is busy` 时不停止：说明仍有持有者保留该挂载，先执行第 4、5 步，再重试这条 `umount`。路径已被其他进程释放（`not mounted`、`mountpoint not found`）视为已达成目标，不再重试。其他卸载错误立即停止，不强制或延迟卸载。卸载与 `lvremove` 固定以 `LC_ALL=C` 运行，使 busy / not mounted / filesystem-in-use 的判定不依赖 worker 的语言环境。
4. 按目标设备主次号精确匹配 `/proc/<pid>/mountinfo`，得到仍保留该文件系统的任务及其挂载路径；每个挂载只记录一次，并取该挂载命名空间中任务 ID 最小的进程（容器主进程），也就是操作者在节点上认得的那个 PID。查找只产出第 5 步需要的 `<pid>` 与 `<path>`：读不到的任务证据、以及未通过保护检查的挂载，会被跳过而不是让整个查找失败。跳过不会卸载错误的路径，只会多出一次被拒绝的删除。查找整体失败时在任务日志中记录原因并继续执行第 6 步；查找读到的设备身份与目标不一致时仍停止并保留卷。
5. 对每个持有者执行一条 `nsenter -t <pid> -m umount <path>`：只进入该挂载命名空间，保留宿主机 root，使扫描到的挂载路径可在其中直接解析，执行普通 `umount`。不强制、不延迟卸载；不固定进程身份，不核对设备或 mount ID，也不进入持有者容器的根目录。持有者在这条命令之前自行释放该挂载（`not mounted`）不算失败。不重启 Promtail，不删除 Pod，不终止业务进程。
6. 重试第 3 步中因 busy 未完成的宿主机卸载；重试仍失败时停止并保留卷，并报告是宿主机的本地使用者而非持有者仍占用该挂载。随后校验目标挂载已消失、设备身份不变，执行 `lvremove`。删除前不检查 `dmsetup` Open Count：卷仍被某处占用时，由 `lvremove` 自身报 filesystem-in-use 并保留卷。
7. LV 删除成功后清理该设备的 `/etc/fstab` 条目。任务日志保留每一步的真实结果；后续配置清理失败会报告部分已完成操作。

首次 `lvremove` 明确报 filesystem-in-use 时，最多额外进行一轮设备查找、命名空间普通卸载和一次删除重试。传输错误或其他 LVM 错误不触发盲目重试。

## 操作者必须确认的前提

**该回收流程是不可逆的底层删除操作，不再自动检查 Kubernetes Pod/PVC/PV 是否仍引用该卷。** 宿主机与持有者视图中的 `umount` 成功并不证明一个闲置 Notebook 的 PVC 不再需要其数据，也不保证未来重新挂载的数据安全。

管理员在点击删除/回收或提交 API 请求前，必须确认：

- 目标卷及数据可以永久丢弃，业务已停用；没有其他客户端、调度器、特权程序或外部管理员并发修改相关挂载/LVM。
- 操作的是正确的节点、VG/LV 和设备；不能把历史 PID 或 Pod 名当作本次占用证据。
- 维护范围涵盖程序无法完全枚举的引用；进程扫描不是完整的内核命名空间证明，最终以 `lvremove` 的实际结果为准。

前端保留不可撤销确认，明确提示上述前提。不再出现维护模式勾选框，不再因为全局 Pod 列表、维护开关或工作负载许可名单阻止该手册回收流程；接口亦不会自动删除 Pod/PVC。

## Linux 5.10 兼容性与工具

回收不依赖 Linux 6.12 的 `NS_MNT_GET_INFO/NEXT/PREV`，Linux 5.10 节点无需升级内核来执行该流程。节点需具备：

- 可信宿主机 Python 3、GNU coreutils `timeout`、LVM/device-mapper 工具，以及 `findmnt`、普通 `umount`、`nsenter`。`exportfs` 与 `sed` 仅在宿主机上确有导出需要撤销（存在 `/etc/exports`）时才需要。
- Linux 宿主机 root 及读取目标进程证据、进入其 mount namespace、普通卸载所需权限。
- 单个后端实例、同一物理节点不重复注册为多个 worker。应用内 worker 串行锁不约束外部操作者。

实际持有者挂载可以是 shared；程序按手册普通卸载，不为了删除修改任何传播设置。查找仍按目标设备精确匹配并校验保护路径，层叠/子挂载、保护路径等不能明确定位的结构会被排除在卸载列表之外；被排除的挂载不卸载，交由 `lvremove` 判定。普通卸载本身被内核拒绝时任务停止并保留卷。

`SHARED_HOST_MAINTENANCE_ENABLED`、`NAMESPACE_CLEANUP_ALLOWLIST` 与旧 `maintenance_confirmed` 请求字段仅保留旧配置/客户端兼容性，**不再作为删除或 NFS 回收的启用/许可条件**。未传维护字段也采用同一手册流程。

`NAMESPACE_CLEANUP_TIMEOUT` 继续限定删除/回收阶段扫描与命名空间卸载的总预算。`NAMESPACE_UNMOUNT_TIMEOUT` 仍约束保留的 Python 卸载 helper（host unmount 等路径）。删除流程不放宽 resize 的检查；resize 本身按《NFS创建流程》第 9 节执行（扩容在线进行，缩容仍要求卷未被挂载占用），并且只读取 LV 身份（与删除流程使用同一个 `inspect_lv`），不再要求挂载传播证明——那项证据 resize 从不使用，却会以 `target/direct-parent propagation not proven local` 拒绝所有无法证明本地传播的节点的扩容（见 2026-10-21 设计修订）。

## 执行状态不明

删除/回收路径的命名空间卸载是逐条 SSH 命令，不创建标记，也不因单条卸载失败隔离 worker；失败作为任务错误上报，已完成的卸载不会自动回滚。

保留的 Python 卸载 helper（host unmount 等路径）仍在改变挂载前创建 `/run/control-panel-storage-recovery.uncertain`，超时或无法确认执行器退出时保留标记并隔离该 worker。宿主机上存在该标记时后续存储命令继续被拒绝：只有维护人员确认 helper 已退出、挂载/设备状态核实后才可解除标记，不可为继续删除直接清除；无法终止的内核等待需要节点维护。已完成的宿主机卸载、导出修改或部分容器卸载不会因任务失败自动恢复，需依据任务日志处理。

当前删除/回收流程不调用该 helper，也不创建该标记，`guardedStorageRunner` 的内存隔离同样只由已废弃的共享宿主机卸载路径设置。因此现场遇到的标记只可能是旧版本中断后留下的残留；它位于 `/run`（tmpfs），worker 重启也会清除。任务日志会直接给出该文件路径与解除步骤。

## 验收与发布边界

本地 Go/Python/前端测试仅验证协议、流程和纯解析/保护条件。真实 PID 与挂载命名空间上下文、普通卸载、共享传播、busy 及 helper 异常终止，仍须在隔离 Linux 测试环境验收；不能在生产卷上做破坏性测试，也不能宣称 Windows mocked 测试证明现场删除成功。

Git 提交或推送不等于更新运行中的镜像/Deployment。Python 执行器和前端资源嵌入 Go 后端，需要重新构建并部署后端后修改才生效。手工步骤见 `NFS创建流程.md` 第 8.2 节。
