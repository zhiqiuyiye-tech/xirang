## 1、安装NFS

```sql
sudo yum update -y
sudo yum install -y nfs-utils
```

## 2、配置强制使用NFSv4

```sql
sudo vi /etc/nfs.conf
```

找到 `[nfsd]` 这一节（如果没有就自己加在文件末尾），配置如下：

```conf
[nfsd]
vers2=n
vers3=n
vers4=y
vers4.0=y
vers4.1=y
vers4.2=y
```

## 3、把物理盘做成 LVM 存储池 (Volume Group)

```bash
# 0. 安装依赖
dnf install -y lvm2

# 1. 创建物理卷 (PV)
pvcreate /dev/nvme1n1p1

# 2. 创建一个名为 "vg_data" 的存储池 (VG)，把刚才的 PV 加进去
vgcreate vg_data /dev/nvme1n1p1

# 可以运行 vgs 看看，你现在拥有了一个容量为 3.5T 的资源池！
vgs
```

## 4、按需“切出”你想要的空间 (Logical Volume)

现在，你要给某个 Notebook 切一个 200G 的盘，给另一个切 500G 的盘：

```bash
# 1. 从资源池里切出一个 200G 的卷，取名叫 lv_notebook_200g
lvcreate -L 200G -n lv_notebook_200g vg_data

# 2. 从资源池里切出一个 500G 的卷，取名叫 lv_notebook_500g
lvcreate -L 500G -n lv_notebook_500g vg_data

# 可以运行 lvs 查看你切出来的卷
lvs
```

## 5、格式化并挂载为独立的文件夹

```bash
# 1. 格式化这些逻辑卷 (推荐使用 ext4 或 xfs)
mkfs.ext4 /dev/vg_data/lv_notebook_200g
mkfs.ext4 /dev/vg_data/lv_notebook_500g

# 2. 在宿主机上创建专门用来跑 NFS 的挂载点
mkdir -p /data02/notebook_a_200g
mkdir -p /data02/notebook_b_500g

# 3. 将逻辑卷挂载到对应的文件夹
mount /dev/vg_data/lv_notebook_200g /data02/notebook_a_200g
mount /dev/vg_data/lv_notebook_500g /data02/notebook_b_500g
```

(注意：为了机器重启后不掉线，你需要把它们写入 `/etc/fstab`。)

```bash
/dev/vg_data/lv_notebook_200g   /data02/notebook_a_200g   ext4    defaults    0 2
/dev/vg_data/lv_notebook_500g   /data02/notebook_b_500g   ext4    defaults    0 2
```

请注意将 `ext4` 替换为真实格式

## 6、通过 NFS 暴露出去

现在，你再去修改 NFS 的配置文件 `/etc/exports`

```bash
vi /etc/exports
```

添加上下面的内容

```bash
/data02/notebook_a_200g *(rw,sync,no_root_squash,no_subtree_check)
/data02/notebook_b_500g *(rw,sync,no_root_squash,no_subtree_check)
```

## 7、启动服务并设置开机自启

```bash
# 使挂载配置生效
sudo exportfs -arv

# 启动并设置开机自启（注意名字是 nfs-server）
sudo systemctl enable --now nfs-server

# 查看服务状态确认有没有报错
sudo systemctl status nfs-server
```


## 8、回收LVM空间

### 8.1 停止 NFS 共享并清理配置

```bash
sudo vi /etc/exports
```

把里面关于 `/data02/notebook_a_200g` 和 `/data02/notebook_b_500g` 的那两行配置**删除**。

刷新NFS配置

```bash
sudo exportfs -arv
```

### 8.2 在宿主机上卸载（Unmount）目录

```bash
sudo umount /data02/notebook_a_200g
sudo umount /data02/notebook_b_500g
```

(💡 小贴士：如果系统提示 `target is busy`，说明有进程正在使用这个目录。你可以通过 `sudo lsof +D /data02/notebook_a_200g` 查出是哪个进程，把它杀掉后再尝试卸载。)

### 8.3 彻底删除 LVM 逻辑卷（回收空间）

现在这 700G 的空间处于游离状态，我们需要把它们彻底销毁，把容量还给底层的 3.5T `vg_data` 存储池。

执行删除命令（系统会询问你是否确认删除，输入 `y` 并回车）：

```bash
sudo lvremove /dev/vg_data/lv_notebook_200g
sudo lvremove /dev/vg_data/lv_notebook_500g
```

删除后，你可以运行 `sudo vgs` 看一眼，你会发现 `vg_data` 的 `VFree`（可用空间）又变回满血的 3.5T 了！

### 8.4 清理开机自启配置（极其重要！）

如果你之前为了防止重启失效，把挂载信息写进了 `/etc/fstab` 文件里，**这一步千万不能忘！**

找到带有 `lv_notebook_200g` 和 `lv_notebook_500g` 的那两行，**把它们删掉**。


添加nfs到集群

mysql -u root -p -h 172.16.88.7 -P 6301                    Aba98b87@vq

```bash
INSERT INTO esx_tai.file_storage (uuid, name, path, service_address, workspace_uuid, type)
Values('cof540cd-eb8b-4619-Bad2-82b0eBe4532g', 'jxsr-nfs-200g', '/data02/notebook_a_200g', '10.37.1.45', 'ws-d8t5nq1uma3bg0ocu5cg', 'EnterprtseAllocate');
```