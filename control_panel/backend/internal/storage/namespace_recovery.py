"""Host-only Linux namespace recovery. Imported tests never execute main.

All container entry happens in forked helpers, using host-loaded libc only.
Unknown/unsafe evidence is fatal; no force/lazy unmount or business process kill.
"""

import ctypes
import json
import os
import posixpath
import re
import signal
import stat
import subprocess
import sys
import time

MARKER = "/run/control-panel-storage-recovery.uncertain"
MAX_BYTES = 8 * 1024 * 1024
MAX_PROCESSES = 32768
MAX_MOUNTS = 65536
PROTECTED = (
    "/",
    "/boot",
    "/dev",
    "/proc",
    "/sys",
    "/run",
    "/etc",
    "/usr",
    "/bin",
    "/sbin",
    "/lib",
    "/lib64",
    "/var",
)
LV_PATTERN = re.compile(
    r"/dev/[A-Za-z0-9_+][A-Za-z0-9_+.-]*/[A-Za-z0-9_+][A-Za-z0-9_+.-]*\Z"
)
DEVICE_PATTERN = re.compile(r"(?:0|[1-9][0-9]*):(?:0|[1-9][0-9]*)\Z")


class RecoveryError(Exception):
    def __init__(self, message, state_unknown=False):
        super().__init__(message)
        self.state_unknown = state_unknown


def require(condition, message):
    if not condition:
        raise RecoveryError(message)


def read_text(path, dir_fd=None):
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC, dir_fd=dir_fd)
    try:
        with os.fdopen(
            fd, "r", encoding="utf-8", errors="strict", closefd=False
        ) as stream:
            text = stream.read(MAX_BYTES + 1)
        require(len(text) <= MAX_BYTES, "proc evidence exceeds limit")
        return text
    finally:
        os.close(fd)


def decode_path(value):
    # mountinfo defines exactly these four octal escapes. Unknown escapes must
    # not silently turn into a path the kernel did not report.
    escapes = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}
    output = []
    i = 0
    while i < len(value):
        if value[i] == "\\":
            code = value[i + 1 : i + 4]
            require(code in escapes, "invalid mountinfo path escape")
            output.append(escapes[code])
            i += 4
        else:
            output.append(value[i])
            i += 1
    path = "".join(output)
    require(
        path.startswith("/")
        and "\x00" not in path
        and posixpath.normpath(path) == path,
        "noncanonical mountinfo path",
    )
    return path


def parse_mountinfo(text):
    records = []
    seen = set()
    require(bool(text.strip()), "empty mountinfo")
    for line in text.splitlines():
        fields = line.split(" ")
        require(all(fields) and fields.count("-") == 1, "malformed mountinfo")
        sep = fields.index("-")
        require(sep >= 6 and len(fields) == sep + 4, "malformed mountinfo fields")
        require(fields[0].isdigit() and fields[1].isdigit(), "invalid mount IDs")
        ident, parent = int(fields[0]), int(fields[1])
        require(
            ident > 0 and ident not in seen and DEVICE_PATTERN.fullmatch(fields[2]),
            "invalid mount identity",
        )
        seen.add(ident)
        records.append(
            {
                "id": ident,
                "parent_id": parent,
                "device": fields[2],
                "root": decode_path(fields[3]),
                "path": decode_path(fields[4]),
                "optional": fields[6:sep],
            }
        )
        require(len(records) <= MAX_MOUNTS, "mount scale exceeds limit")
    return records


def within(path, root):
    return path == root or path.startswith(root.rstrip("/") + "/")


def safe_mounts(records, device, reserved):
    require(DEVICE_PATTERN.fullmatch(device), "invalid target device")
    by_id = {m["id"]: m for m in records}
    paths = {}
    for record in records:
        paths.setdefault(record["path"], []).append(record)
    targets = [m for m in records if m["device"] == device]
    for mount in targets:
        path = mount["path"]
        require(path != "/", "target is namespace root")
        for root in list(PROTECTED[1:]) + list(reserved):
            require(
                not within(path, root) and not within(root, path),
                "target intersects protected path",
            )
        require(len(paths[path]) == 1, "stacked target mounts")
        # Reject all descendants, including same-device descendants. This
        # conservative first version never recursively unmounts another mount.
        for other in records:
            if other["id"] != mount["id"]:
                require(
                    not within(other["path"], path), "target has child/stacked mount"
                )
                cursor = other
                visited = set()
                while cursor["parent_id"] in by_id and cursor["id"] not in visited:
                    visited.add(cursor["id"])
                    require(
                        cursor["parent_id"] != mount["id"],
                        "target has mount-tree child",
                    )
                    cursor = by_id[cursor["parent_id"]]
        # An unmount event propagates through the DIRECT parent mount. A
        # private parent isolates the event even if more distant ancestors are
        # shared. Keep structural checks for the whole ancestry below.
        require(mount["parent_id"] in by_id, "unknown mount parent")
        require(
            not mount["optional"] and not by_id[mount["parent_id"]]["optional"],
            "target/direct-parent propagation not proven private",
        )
        current = mount
        visited = set()
        while True:
            require(current["id"] not in visited, "cyclic mount parent")
            visited.add(current["id"])
            if current["path"] == "/":
                break
            require(current["parent_id"] in by_id, "unknown mount parent")
            parent = by_id[current["parent_id"]]
            require(
                len(paths[parent["path"]]) == 1
                and within(current["path"], parent["path"]),
                "ambiguous or inconsistent parent mount",
            )
            current = parent
    return sorted(targets, key=lambda m: m["id"])


def parse_starttime(text):
    end = text.rfind(")")
    require(end > 0 and " (" in text[:end], "invalid proc stat")
    fields = text[end + 1 :].split()
    # fields starts at field 3 (state); starttime is field 22.
    require(len(fields) > 19 and fields[19].isdigit(), "invalid process starttime")
    return fields[19]


def can_skip_missing_process(pid):
    """ENOENT is ignorable only for vanished or stably exited tasks.

    Zombie leaders can remain in /proc after their namespace/root references
    are released while other threads survive; pids() still enumerates those
    threads. Never ignore permission errors or missing evidence for live tasks.
    """
    base = "/proc/%d" % pid
    if not os.path.exists(base):
        return True
    try:
        first = read_text(base + "/stat")
        second = read_text(base + "/stat")
    except FileNotFoundError:
        return not os.path.exists(base)
    if parse_starttime(first) != parse_starttime(second):
        return False
    first_state = first[first.rfind(")") + 1 :].split()[0]
    second_state = second[second.rfind(")") + 1 :].split()[0]
    return first_state in ("Z", "X", "x") and second_state in ("Z", "X", "x")


def process_info(pid):
    base = "/proc/%d/" % pid
    start = parse_starttime(read_text(base + "stat"))
    cgroup = read_text(base + "cgroup")
    require(bool(cgroup.strip()), "empty process cgroup")
    for line in cgroup.splitlines():
        parts = line.split(":", 2)
        require(
            len(parts) == 3 and parts[0].isdigit() and parts[2].startswith("/"),
            "invalid cgroup evidence",
        )
    namespace = os.readlink(base + "ns/mnt")
    require(re.fullmatch(r"mnt:\[[1-9][0-9]*\]", namespace), "invalid mount namespace")
    root = os.stat(base + "root")
    require(
        start == parse_starttime(read_text(base + "stat")),
        "process identity changed during read",
    )
    return (
        {"pid": pid, "start_time": start, "cgroup": cgroup},
        namespace,
        (root.st_dev, root.st_ino),
    )


def run_probe(arguments):
    try:
        proc = subprocess.run(
            arguments,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=5,
            env={"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C"},
            text=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RecoveryError(
            "host LVM/device-mapper probe unavailable or timed out"
        ) from exc
    require(
        proc.returncode == 0 and len(proc.stdout) <= MAX_BYTES,
        "host device probe failed",
    )
    return proc.stdout


def identity_from_rows(rows):
    require(isinstance(rows, list) and len(rows) > 0, "missing LV metadata")
    identity = None
    for row in rows:
        keys = (
            "lv_uuid",
            "lv_attr",
            "segtype",
            "origin",
            "pool_lv",
            "lv_kernel_major",
            "lv_kernel_minor",
        )
        require(
            isinstance(row, dict)
            and all(k in row and isinstance(row[k], str) for k in keys),
            "incomplete LV metadata",
        )
        row = {k: row[k].strip() for k in keys}
        # Only ordinary active, writable, linear independent volumes. Origin,
        # snapshot, thin, raid, cached and unknown volume types are rejected.
        require(
            re.fullmatch(r"-w[aciln]-a[o-]----", row["lv_attr"]) is not None
            and row["segtype"] == "linear"
            and not row["origin"]
            and not row["pool_lv"],
            "LV is not an ordinary independent linear volume",
        )
        major, minor = row["lv_kernel_major"], row["lv_kernel_minor"]
        require(
            major.isdigit() and minor.isdigit() and bool(row["lv_uuid"]),
            "invalid active LV identity",
        )
        candidate = {
            "uuid": row["lv_uuid"],
            "major_minor": "%d:%d" % (int(major), int(minor)),
        }
        require(identity is None or identity == candidate, "inconsistent LV segments")
        identity = candidate
    return identity


def inspect_device(lv_dev):
    require(
        LV_PATTERN.fullmatch(lv_dev) and "/mapper/" not in lv_dev, "expected /dev/VG/LV"
    )
    fields = "lv_uuid,lv_attr,segtype,origin,pool_lv,lv_kernel_major,lv_kernel_minor"
    try:
        report = json.loads(
            run_probe(
                [
                    "lvs",
                    "--reportformat",
                    "json",
                    "--segments",
                    "-o",
                    fields,
                    "--",
                    lv_dev,
                ]
            )
        )
        require(len(report["report"]) == 1, "ambiguous LV report")
        # --segments selects the "seg" report, not the ordinary "lv" table.
        identity = identity_from_rows(report["report"][0]["seg"])
    except (ValueError, KeyError, TypeError) as exc:
        raise RecoveryError("invalid LVM JSON report") from exc
    info = os.stat(lv_dev)
    require(stat.S_ISBLK(info.st_mode), "target is not a block device")
    require(
        "%d:%d" % (os.major(info.st_rdev), os.minor(info.st_rdev))
        == identity["major_minor"],
        "LV path device mismatch",
    )
    holder_path = "/sys/dev/block/" + identity["major_minor"] + "/holders"
    require(not os.listdir(holder_path), "LV has dependent block devices")
    # Correlate device mapper UUID (LVM- + VG UUID + LV UUID) to the lvs UUID.
    dm_uuid = read_text(
        "/sys/dev/block/" + identity["major_minor"] + "/dm/uuid"
    ).strip()
    uuid = identity["uuid"].replace("-", "")
    require(
        dm_uuid.startswith("LVM-") and len(dm_uuid) == 68 and dm_uuid[36:] == uuid,
        "device mapper/LVM UUID mismatch",
    )
    return identity


def pids():
    found = set()
    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue
        base = "/proc/" + name
        try:
            # Non-leader threads can hold distinct mount namespaces and are
            # invisible in the top-level /proc listing. Include their TIDs.
            tasks = os.listdir(base + "/task")
        except FileNotFoundError:
            require(not os.path.exists(base), "live process task evidence missing")
            continue
        found.update(int(tid) for tid in tasks if tid.isdigit())
        require(len(found) <= MAX_PROCESSES, "process/thread scale exceeds limit")
    return sorted(found)


def scan(lv_dev, reserved):
    device = inspect_device(lv_dev)
    groups = {}
    # Every process is read. Namespace de-duplication never drops other cgroup
    # members: the parent authorizes the complete namespace membership set.
    for pid in pids():
        try:
            member, ns, root = process_info(pid)
            mounts = parse_mountinfo(read_text("/proc/%d/mountinfo" % pid))
            member2, ns2, root2 = process_info(pid)
            require(
                (member, ns, root) == (member2, ns2, root2),
                "process changed during namespace scan",
            )
        except FileNotFoundError:
            require(can_skip_missing_process(pid), "incomplete live process evidence")
            continue
        except PermissionError as exc:
            raise RecoveryError("permission denied reading namespace evidence") from exc
        group = groups.setdefault(ns, {"members": [], "views": []})
        group["members"].append(member)
        # Validate each root view immediately; retain only matching mounts,
        # rather than one complete mount table per namespace member.
        targets = safe_mounts(mounts, device["major_minor"], reserved)
        group["views"].append((member, root, targets if targets else None))
    holders = []
    for ns in sorted(groups):
        group = groups[ns]
        target_views = [v for v in group["views"] if v[2] is not None]
        if not target_views:
            continue
        member, root, records = target_views[0]
        require(
            len(target_views) == len(group["views"]),
            "namespace has inaccessible target root views",
        )
        targets = records
        for _, other_root, other_records in target_views:
            require(
                other_root == root and other_records == targets,
                "namespace members have different root/mount views",
            )
        holders.append(
            dict(
                member,
                namespace=ns,
                root_dev=root[0],
                root_ino=root[1],
                mounts=targets,
                members=group["members"],
            )
        )
        require(len(holders) <= 4096, "namespace scale exceeds limit")
    require(inspect_device(lv_dev) == device, "LV identity changed during scan")
    return {"device": device, "holders": holders}


def check_members(expected, actual):
    require(expected == actual, "namespace membership or process identity changed")


def check_holder_process(holder):
    member, namespace, root = process_info(holder["pid"])
    require(
        member == {k: holder[k] for k in ("pid", "start_time", "cgroup")}
        and namespace == holder["namespace"]
        and root == (holder["root_dev"], holder["root_ino"]),
        "representative PID/root/namespace identity changed",
    )


def create_marker():
    try:
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o600)
    except FileExistsError as exc:
        raise RecoveryError(
            "prior namespace recovery state is uncertain", True
        ) from exc
    try:
        os.write(
            fd,
            b"namespace recovery in progress; reconcile helper exit before removing\n",
        )
        os.fsync(fd)
    except BaseException:
        os.close(fd)
        raise
    return fd


def remove_marker():
    os.unlink(MARKER)


def load_host_libc():
    # dlopen(NULL) resolves already-loaded host libc symbols; no container
    # executable, interpreter, dynamic loader or libc path is ever consulted.
    libc = ctypes.CDLL(None, use_errno=True)
    libc.setns.argtypes = (ctypes.c_int, ctypes.c_int)
    libc.setns.restype = ctypes.c_int
    libc.umount2.argtypes = (ctypes.c_char_p, ctypes.c_int)
    libc.umount2.restype = ctypes.c_int
    libc.prctl.argtypes = (
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
    )
    libc.prctl.restype = ctypes.c_int
    return libc


def libc_check(result, operation):
    if result != 0:
        raise RecoveryError(operation + " failed (errno %d)" % ctypes.get_errno())


def open_mount_path(root_fd, path):
    # Do not traverse symlinked ancestors or permit '..'. O_PATH itself does
    # not open a business file for I/O, and fdinfo exposes the exact mount ID.
    current = os.dup(root_fd)
    try:
        parts = path.split("/")[1:]
        require(
            all(part and part not in (".", "..") for part in parts),
            "invalid mount path components",
        )
        for part in parts:
            child = os.open(
                part, os.O_PATH | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=current
            )
            os.close(current)
            current = child
            require(
                stat.S_ISDIR(os.fstat(current).st_mode),
                "target path contains non-directory/symlink",
            )
        result = current
        current = -1
        return result
    finally:
        if current >= 0:
            os.close(current)


def validate_mount_path(root_fd, proc_fd, mount):
    fd = open_mount_path(root_fd, mount["path"])
    try:
        info = os.fstat(fd)
        require(
            "%d:%d" % (os.major(info.st_dev), os.minor(info.st_dev)) == mount["device"],
            "mount path device changed",
        )
        text = read_text("self/fdinfo/%d" % fd, dir_fd=proc_fd)
        matches = re.findall(r"^mnt_id:\s*([0-9]+)$", text, re.MULTILINE)
        require(
            matches == [str(mount["id"])],
            "mount path does not resolve to approved mount ID",
        )
    finally:
        os.close(fd)


def child_unmount(
    libc, ns_fd, root_fd, proc_fd, holder, reserved, preflight, parent_pid
):
    try:
        # Only our helper child receives a parent-death signal. This never
        # targets the representative or any container/business process.
        libc_check(
            libc.prctl(1, signal.SIGKILL, 0, 0, 0), "helper parent-death watchdog"
        )
        require(os.getppid() == parent_pid, "helper supervisor already exited")
        libc_check(libc.setns(ns_fd, 0x00020000), "setns")
        os.fchdir(root_fd)
        os.chroot(".")
        os.chdir("/")
        current_root = os.stat("/")
        require(
            (current_root.st_dev, current_root.st_ino)
            == (holder["root_dev"], holder["root_ino"]),
            "pinned root changed",
        )
        records = parse_mountinfo(read_text("self/mountinfo", dir_fd=proc_fd))
        require(
            safe_mounts(records, holder["mounts"][0]["device"], reserved)
            == holder["mounts"],
            "namespace mount evidence changed",
        )
        for mount in holder["mounts"]:
            validate_mount_path(root_fd, proc_fd, mount)
        if not preflight:
            for mount in holder["mounts"]:
                # Re-read immediately before each ordinary unmount. The kernel
                # still cannot make a path-based umount atomic with remounts.
                records = parse_mountinfo(read_text("self/mountinfo", dir_fd=proc_fd))
                approved = safe_mounts(records, mount["device"], reserved)
                require(mount in approved, "approved mount changed before unmount")
                validate_mount_path(root_fd, proc_fd, mount)
                libc_check(
                    libc.umount2(os.fsencode(mount["path"]), 0), "ordinary umount2"
                )
        os._exit(0)
    except BaseException:
        # Child emits no cmdline/environment or uncontrolled exception content.
        os._exit(1)


def spawn_unmount(libc, pinned, holder, reserved, timeout, preflight=False):
    parent_pid = os.getpid()
    pid = os.fork()
    if pid == 0:
        child_unmount(libc, *pinned, holder, reserved, preflight, parent_pid)
    deadline = time.monotonic() + timeout
    while True:
        found, status = os.waitpid(pid, os.WNOHANG)
        if found:
            require(
                os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0,
                "namespace helper rejected changed evidence or ordinary unmount failed",
            )
            return
        if time.monotonic() >= deadline:
            # Kill only the forked helper. A blocked kernel unmount may remain
            # uninterruptible: never claim release, and always retain marker.
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            reap_deadline = time.monotonic() + 1
            while time.monotonic() < reap_deadline:
                found, _ = os.waitpid(pid, os.WNOHANG)
                if found:
                    break
                time.sleep(0.02)
            raise RecoveryError(
                "namespace helper timed out; reconcile remote state before further storage operations",
                True,
            )
        time.sleep(0.02)


def cleanup(lv_dev, reserved, snapshot, timeout):
    marker_fd = create_marker()
    pinned = []
    uncertain = False
    try:
        require(
            snapshot["device"] == inspect_device(lv_dev),
            "LV identity changed before cleanup",
        )
        fresh = scan(lv_dev, reserved)
        require(
            fresh == snapshot and bool(snapshot["holders"]),
            "authorized snapshot changed before cleanup",
        )
        libc = load_host_libc()
        host_ns = os.readlink("/proc/self/ns/mnt")
        # Pin every namespace and root before any preflight/unmount worker.
        for holder in snapshot["holders"]:
            require(
                holder["namespace"] != host_ns,
                "host namespace must be ordinarily unmounted by host workflow",
            )
            check_holder_process(holder)
            fds = []
            try:
                fds.append(
                    os.open(
                        "/proc/%d/ns/mnt" % holder["pid"], os.O_RDONLY | os.O_CLOEXEC
                    )
                )
                fds.append(
                    os.open(
                        "/proc/%d/root" % holder["pid"],
                        os.O_PATH | os.O_DIRECTORY | os.O_CLOEXEC,
                    )
                )
                fds.append(
                    os.open("/proc", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
                )
                ns_ino = int(
                    re.fullmatch(r"mnt:\[([0-9]+)\]", holder["namespace"]).group(1)
                )
                root = os.fstat(fds[1])
                require(
                    os.fstat(fds[0]).st_ino == ns_ino
                    and (root.st_dev, root.st_ino)
                    == (holder["root_dev"], holder["root_ino"]),
                    "pinned namespace/root mismatch",
                )
                check_holder_process(holder)
                pinned.append(tuple(fds))
            except BaseException:
                for fd in fds:
                    os.close(fd)
                raise
        # Check every target in its actual root context without any unmount.
        for holder, fds in zip(snapshot["holders"], pinned):
            spawn_unmount(libc, fds, holder, reserved, timeout, preflight=True)
        require(scan(lv_dev, reserved) == snapshot, "snapshot changed after preflight")
        for holder, fds in zip(snapshot["holders"], pinned):
            check_holder_process(holder)
            # Re-scan complete members, including newly created unknown members.
            actual = []
            for pid in pids():
                try:
                    member, namespace, root = process_info(pid)
                except FileNotFoundError:
                    require(
                        can_skip_missing_process(pid),
                        "incomplete live process evidence",
                    )
                    continue
                if namespace == holder["namespace"]:
                    require(
                        root == (holder["root_dev"], holder["root_ino"]),
                        "member root changed",
                    )
                    actual.append(member)
            check_members(holder["members"], actual)
            require(
                inspect_device(lv_dev) == snapshot["device"],
                "LV identity changed before unmount",
            )
            spawn_unmount(libc, fds, holder, reserved, timeout)
        return {"cleaned": True}
    except RecoveryError as exc:
        uncertain = exc.state_unknown
        raise
    except BaseException as exc:
        # Unknown exceptions are conservatively quarantined. Ordinary evidence
        # failures above are known exits with all workers already reaped.
        uncertain = True
        raise RecoveryError(
            "cleanup failed without confirmed remote state", True
        ) from exc
    finally:
        for fds in pinned:
            for fd in fds:
                os.close(fd)
        os.close(marker_fd)
        if not uncertain:
            remove_marker()


def open_count(identity):
    major, minor = identity["major_minor"].split(":")
    output = run_probe(
        [
            "dmsetup",
            "info",
            "-c",
            "--noheadings",
            "-o",
            "major,minor,open",
            "--separator",
            ":",
            "-j",
            major,
            "-m",
            minor,
        ]
    ).strip()
    require(
        re.fullmatch(r"[0-9]+:[0-9]+:[0-9]+", output),
        "invalid device-mapper Open Count",
    )
    fields = output.split(":")
    require(
        ":".join(fields[:2]) == identity["major_minor"], "Open Count device mismatch"
    )
    return int(fields[2])


def verify(lv_dev, reserved, identity):
    for attempt in range(3):
        require(
            inspect_device(lv_dev) == identity,
            "LV identity changed before verification",
        )
        snapshot = scan(lv_dev, reserved)
        require(
            snapshot["device"] == identity and not snapshot["holders"],
            "residual target namespace mounts remain",
        )
        count = open_count(identity)
        require(
            inspect_device(lv_dev) == identity,
            "LV identity changed during verification",
        )
        if count == 0:
            return {"released": True, "device": identity}
        if attempt < 2:
            time.sleep(1)
    raise RecoveryError("device Open Count remains nonzero after 3 checks")


def no_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def main():
    operation = None
    try:
        require(
            sys.platform == "linux" and os.geteuid() == 0,
            "namespace recovery requires Linux host root",
        )
        text = sys.stdin.read(MAX_BYTES + 1)
        require(len(text) <= MAX_BYTES, "request exceeds limit")
        req = json.loads(text, object_pairs_hook=no_duplicate_pairs)
        require(
            isinstance(req, dict)
            and set(req)
            == {"operation", "lv_dev", "reserved", "unmount_timeout", "payload"},
            "invalid request schema",
        )
        operation, lv_dev, reserved = req["operation"], req["lv_dev"], req["reserved"]
        require(
            isinstance(lv_dev, str)
            and LV_PATTERN.fullmatch(lv_dev)
            and "/mapper/" not in lv_dev,
            "invalid LV path",
        )
        require(
            isinstance(reserved, list)
            and len(reserved) <= 256
            and all(
                isinstance(p, str) and p.startswith("/") and posixpath.normpath(p) == p
                for p in reserved
            ),
            "invalid protected paths",
        )
        timeout = req["unmount_timeout"]
        require(
            type(timeout) in (int, float) and 0 < timeout <= 10,
            "invalid unmount timeout",
        )
        if operation == "inspect":
            result = inspect_device(lv_dev)
            safe_mounts(
                parse_mountinfo(read_text("/proc/self/mountinfo")),
                result["major_minor"],
                reserved,
            )
        elif operation == "scan":
            result = scan(lv_dev, reserved)
        elif operation == "cleanup":
            result = cleanup(lv_dev, reserved, req["payload"], timeout)
        elif operation == "verify":
            result = verify(lv_dev, reserved, req["payload"])
        else:
            raise RecoveryError("unsupported recovery operation")
        print(
            json.dumps({"ok": True, "result": result}, separators=(",", ":")),
            flush=True,
        )
        return 0
    except RecoveryError as exc:
        response = {"ok": False, "error": str(exc), "state_unknown": exc.state_unknown}
    except BaseException:
        response = {
            "ok": False,
            "error": "host recovery probe or evidence failed",
            "state_unknown": operation == "cleanup",
        }
    print(json.dumps(response, separators=(",", ":")), flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
