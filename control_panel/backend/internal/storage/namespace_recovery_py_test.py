"""Pure parser and safety tests. Never enter a namespace or touch a volume."""

import importlib.util
import json
import types
import pathlib
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "recovery", pathlib.Path(__file__).with_name("namespace_recovery.py")
)
r = importlib.util.module_from_spec(spec) if spec else None
if spec:
    spec.loader.exec_module(r)

ROOT = "1 0 0:1 / / rw - rootfs rootfs rw\n"
TARGET = "10 1 253:0 / /data02/test rw - xfs /dev/mapper/vg-lv rw\n"
# Real worker-3-10 evidence: nsfs roots are namespace handles, not paths.
NSFS = """1411 30 0:4 net:[4026568827] /run/netns/cni-6b70c1b1-4cd2-3b08-7304-b1b67ed158a3 rw shared:473 - nsfs nsfs rw
771 30 0:4 net:[4026568809] /run/netns/cni-da91d1e3-3535-4d1b-16c8-eb9ae9f9d3b9 rw shared:419 - nsfs nsfs rw
1109 30 0:4 net:[4026568650] /run/netns/cni-27f043a1-0249-8a2c-a771-ea172b66d2ae rw shared:395 - nsfs nsfs rw
1207 30 0:4 net:[4026569044] /run/netns/cni-1a28a774-be2e-7f28-9b10-027953487bd7 rw shared:425 - nsfs nsfs rw
1357 30 0:4 net:[4026569126] /run/netns/cni-97cbe95e-aa71-54cf-ab6e-77baea725c32 rw shared:449 - nsfs nsfs rw
1155 30 0:4 net:[4026568584] /run/netns/cni-0b07a6f1-276f-96d2-554a-070402e5aaf0 rw shared:552 - nsfs nsfs rw
1011 30 0:4 net:[4026547883] /run/netns/cni-d3bda1ef-98f7-6c02-8440-f8641a5777f7 rw shared:365 - nsfs nsfs rw
"""
HOST_NSFS = ROOT + "30 1 0:2 / /run rw - tmpfs tmpfs rw\n" + NSFS


class ParserTests(unittest.TestCase):
    def test_inspect_reads_lvm_segment_json_table(self):
        row = dict(
            lv_uuid="a" * 32,
            lv_attr="-wi-a-----",
            segtype="linear",
            origin="",
            pool_lv="",
            lv_kernel_major="253",
            lv_kernel_minor="0",
        )
        report = json.dumps({"report": [{"seg": [row]}]})
        block = types.SimpleNamespace(st_mode=r.stat.S_IFBLK, st_rdev=7)
        with (
            patch.object(r, "run_probe", return_value=report) as probe,
            patch.object(r.os, "stat", return_value=block),
            patch.object(r.os, "major", return_value=253, create=True),
            patch.object(r.os, "minor", return_value=0, create=True),
            patch.object(r.os, "listdir", return_value=[]),
            patch.object(r, "read_text", return_value="LVM-" + "v" * 32 + "a" * 32),
        ):
            self.assertEqual(
                r.inspect_device("/dev/vg/lv"),
                {"uuid": "a" * 32, "major_minor": "253:0"},
            )
            self.assertIn("--segments", probe.call_args.args[0])

    def test_exact_field_and_escape(self):
        mounts = r.parse_mountinfo(
            ROOT
            + TARGET.replace("/data02/test", "/data02/test\\040space")
            + "11 1 253:10 / /other rw - xfs 253:0 rw\n"
        )
        chosen = r.safe_mounts(mounts, "253:0", ["/data01"])
        self.assertEqual([m["id"] for m in chosen], [10])
        self.assertEqual(chosen[0]["path"], "/data02/test space")

    def test_worker_nsfs_handles_preserved_without_blocking_lv(self):
        mounts = r.parse_mountinfo(HOST_NSFS + TARGET)
        handles = [m for m in mounts if m["device"] == "0:4"]
        self.assertEqual(len(handles), 7)
        self.assertEqual(handles[0]["root"], "net:[4026568827]")
        self.assertEqual(handles[0]["optional"], ["shared:473"])
        self.assertEqual(
            r.safe_mounts(mounts, "253:0", ["/data01"]), r.parse_mountinfo(TARGET)
        )

    def test_nsfs_namespace_types(self):
        for kind in ("net", "mnt", "uts", "ipc", "pid", "user", "cgroup", "time"):
            with self.subTest(kind=kind):
                text = "2 1 0:4 %s:[42] /ns rw - nsfs nsfs rw\n" % kind
                self.assertEqual(r.parse_mountinfo(text)[0]["root"], kind + ":[42]")

    def test_namespace_handles_only_allowed_in_nsfs_root(self):
        cases = [
            "2 1 0:4 net:[42] /ns rw - tmpfs tmpfs rw\n",
            "2 1 0:4 / net:[42] rw - nsfs nsfs rw\n",
        ]
        for root in (
            "net:[0]",
            "net:[-1]",
            "net:[abc]",
            "net:[42]/child",
            "net:[42]suffix",
            "unknown:[42]",
            "relative",
            "net:[42]\x00",
            "net:[42]\\999",
        ):
            cases.append("2 1 0:4 %s /ns rw - nsfs nsfs rw\n" % root)
        for text in cases:
            with self.subTest(text=text), self.assertRaises(r.RecoveryError):
                r.parse_mountinfo(text)

    def test_ordinary_paths_remain_canonical(self):
        for value in ("relative", "/x/../y", "/x//y", "/x/", "/x\x00"):
            for field in (3, 4):
                fields = TARGET.rstrip("\n").split(" ")
                fields[field] = value
                with (
                    self.subTest(value=value, field=field),
                    self.assertRaises(r.RecoveryError),
                ):
                    r.parse_mountinfo(" ".join(fields) + "\n")

    def test_namespace_handle_never_authorizes_target_mount(self):
        mounts = r.parse_mountinfo(ROOT + TARGET)
        mounts[1]["root"] = "net:[42]"
        with self.assertRaises(r.RecoveryError):
            r.safe_mounts(mounts, "253:0", [])

    def test_nsfs_records_still_enforce_target_topology(self):
        for parent, path in ((10, "/elsewhere"), (1, "/data02/test/ns")):
            text = "2 %d 0:4 net:[42] %s rw - nsfs nsfs rw\n" % (parent, path)
            with self.subTest(parent=parent), self.assertRaises(r.RecoveryError):
                r.safe_mounts(r.parse_mountinfo(ROOT + TARGET + text), "253:0", [])

    def test_inspect_with_worker_nsfs_evidence(self):
        import io

        identity = {"uuid": "u", "major_minor": "253:0"}
        request = {
            "operation": "inspect",
            "lv_dev": "/dev/vg/lv",
            "reserved": [],
            "unmount_timeout": 1,
            "payload": None,
        }
        output = io.StringIO()
        with (
            patch.object(r.sys, "platform", "linux"),
            patch.object(r.os, "geteuid", return_value=0, create=True),
            patch.object(r.sys, "stdin", io.StringIO(json.dumps(request))),
            patch.object(r.sys, "stdout", output),
            patch.object(r, "inspect_device", return_value=identity),
            patch.object(r, "read_text", return_value=HOST_NSFS + TARGET),
        ):
            status = r.main()
        self.assertEqual(status, 0, output.getvalue())
        self.assertEqual(
            json.loads(output.getvalue()), {"ok": True, "result": identity}
        )

    def test_scan_and_verify_with_worker_nsfs_evidence(self):
        identity = {"uuid": "u", "major_minor": "253:0"}
        member = {"pid": 123, "start_time": "100", "cgroup": "0::/test\n"}
        with (
            patch.object(r, "inspect_device", return_value=identity),
            patch.object(r, "pids", return_value=[123]),
            patch.object(r, "process_info", return_value=(member, "mnt:[42]", (1, 2))),
            patch.object(r, "read_text", return_value=HOST_NSFS + TARGET) as evidence,
            patch.object(r, "open_count", return_value=0),
        ):
            snapshot = r.scan("/dev/vg/lv", [])
            self.assertEqual(len(snapshot["holders"]), 1)
            self.assertEqual(
                snapshot["holders"][0]["mounts"], r.parse_mountinfo(TARGET)
            )
            evidence.return_value = HOST_NSFS
            self.assertTrue(r.verify("/dev/vg/lv", [], identity)["released"])

    def test_shared_leaf_under_private_parent_can_be_ordinary_unmounted(self):
        text = ROOT + TARGET.replace("rw -", "rw shared:578 -")
        self.assertEqual(
            r.safe_mounts(r.parse_mountinfo(text), "253:0", []),
            r.parse_mountinfo(text)[1:],
        )
        # The same leaf under a shared direct parent still cannot be cleaned
        # inside a container without cross-namespace propagation authorization.
        shared_root = ROOT.replace("rw -", "rw shared:1 -")
        shared_leaf = TARGET.replace("rw -", "rw shared:578 -")
        with self.assertRaises(r.RecoveryError):
            r.safe_mounts(r.parse_mountinfo(shared_root + shared_leaf), "253:0", [])

    def test_shared_leaf_classification_preserves_resize_inspection_policy(self):
        import io

        text = ROOT + TARGET.replace("rw -", "rw shared:578 -")
        identity = {"uuid": "u", "major_minor": "253:0"}
        for operation in ("inspect", "delete_inspect"):
            request = {
                "operation": operation,
                "lv_dev": "/dev/vg/lv",
                "reserved": [],
                "unmount_timeout": 1,
                "payload": None,
            }
            output = io.StringIO()
            with (
                self.subTest(operation=operation),
                patch.object(r.sys, "platform", "linux"),
                patch.object(r.os, "geteuid", return_value=0, create=True),
                patch.object(r.sys, "stdin", io.StringIO(json.dumps(request))),
                patch.object(r.sys, "stdout", output),
                patch.object(r, "inspect_device", return_value=identity),
                patch.object(r, "read_text", return_value=text),
            ):
                status = r.main()
            result = json.loads(output.getvalue())
            if operation == "inspect":
                self.assertEqual(status, 1)
            else:
                self.assertEqual(status, 0)
                self.assertFalse(result["result"]["requires_host_authorization"])

    def test_receive_only_slave_parent_does_not_propagate_leaf_unmount_outward(self):
        # HostToContainer log mounts may be slaves: receive host events, never
        # send this local leaf removal to the master or another peer group.
        text = (
            ROOT
            + "2 1 8:3 /data02 /host-data rw master:1 - ext4 /dev/sda3 rw\n"
            + "10 2 253:0 / /host-data/test rw shared:578 - ext4 /dev/dm-0 rw\n"
        )
        self.assertEqual(len(r.safe_mounts(r.parse_mountinfo(text), "253:0", [])), 1)
        with self.assertRaises(r.RecoveryError):
            r.safe_mounts(
                r.parse_mountinfo(
                    text.replace("rw master:1 -", "rw shared:7 master:1 -")
                ),
                "253:0",
                [],
            )

    def test_shared_ancestor_above_private_parent_is_safe(self):
        root = ROOT.replace("rw -", "rw shared:1 -")
        parent = "2 1 8:1 / /data02 rw - xfs /dev/sdb1 rw\n"
        leaf = TARGET.replace("10 1", "10 2")
        self.assertEqual(
            r.safe_mounts(r.parse_mountinfo(root + parent + leaf), "253:0", []),
            r.parse_mountinfo(leaf),
        )

    def test_missing_evidence_skips_only_confirmed_exited_tasks(self):
        def procstat(state, start="987"):
            return (
                "123 (worker) "
                + state
                + " "
                + " ".join(["0"] * 18 + [start] + ["0"] * 10)
            )

        for state, expected in [("Z", True), ("X", True), ("S", False), ("D", False)]:
            with (
                self.subTest(state=state),
                patch.object(r.os.path, "exists", return_value=True),
                patch.object(
                    r, "read_text", side_effect=[procstat(state), procstat(state)]
                ),
            ):
                self.assertEqual(r.can_skip_missing_process(123), expected)
        with (
            patch.object(r.os.path, "exists", return_value=True),
            patch.object(
                r, "read_text", side_effect=[procstat("Z"), procstat("Z", "988")]
            ),
        ):
            self.assertFalse(r.can_skip_missing_process(123))
        with (
            patch.object(r.os.path, "exists", return_value=True),
            patch.object(r, "read_text", side_effect=PermissionError("denied")),
            self.assertRaises(PermissionError),
        ):
            r.can_skip_missing_process(123)
        with patch.object(r.os.path, "exists", return_value=False):
            self.assertTrue(r.can_skip_missing_process(123))

    def test_scan_and_verify_skip_confirmed_exited_nonholders(self):
        identity = {"uuid": "u", "major_minor": "253:0"}
        member = {"pid": 123, "start_time": "100", "cgroup": "0::/test\n"}

        def info(pid):
            if pid == 456:
                raise FileNotFoundError("exited task has no namespace")
            return member, "mnt:[42]", (1, 2)

        with (
            patch.object(r, "inspect_device", return_value=identity),
            patch.object(r, "pids", return_value=[123, 456]),
            patch.object(r, "process_info", side_effect=info),
            patch.object(r, "read_text", return_value=ROOT),
            patch.object(r, "can_skip_missing_process", return_value=True) as skip,
            patch.object(r, "open_count", return_value=0),
        ):
            self.assertEqual(r.scan("/dev/vg/lv", [])["holders"], [])
            self.assertTrue(r.verify("/dev/vg/lv", [], identity)["released"])
            self.assertEqual(skip.call_count, 2)
        with (
            patch.object(r, "inspect_device", return_value=identity),
            patch.object(r, "pids", return_value=[456]),
            patch.object(
                r,
                "process_info",
                side_effect=FileNotFoundError("missing live evidence"),
            ),
            patch.object(r, "can_skip_missing_process", return_value=False),
            self.assertRaises(r.RecoveryError),
        ):
            r.scan("/dev/vg/lv", [])

    def test_dangerous_topologies_fail_closed(self):
        cases = [
            ROOT.replace("rw -", "rw shared:1 -") + TARGET,
            ROOT + TARGET.replace("rw -", "rw master:2 -"),
            ROOT + TARGET.replace("10 1", "10 99"),
            ROOT + TARGET + "11 10 0:2 / /data02/test/child rw - tmpfs tmpfs rw\n",
            ROOT + TARGET + TARGET.replace("10 1", "11 1"),
            ROOT + TARGET.replace("/data02/test", "/"),
            ROOT + TARGET.replace("/data02/test", "/data01/x"),
            ROOT + TARGET.replace("/data02/test", "/proc/x"),
        ]
        for text in cases:
            with self.subTest(text=text), self.assertRaises(r.RecoveryError):
                r.safe_mounts(r.parse_mountinfo(text), "253:0", ["/data01"])

    def test_bad_mountinfo_rejected(self):
        for text in [
            "",
            "10 1 253:0 / /x rw",
            TARGET.replace("/data02/test", "/x\\999"),
            TARGET + TARGET,
        ]:
            with self.subTest(text=text), self.assertRaises(r.RecoveryError):
                r.parse_mountinfo(text)

    def test_stat_comm_parentheses(self):
        text = "123 (name ) with spaces) S " + " ".join(
            ["0"] * 18 + ["987"] + ["0"] * 10
        )
        self.assertEqual(r.parse_starttime(text), "987")

    def test_membership_requires_exact_approved_set(self):
        member = {"pid": 123, "start_time": "42", "cgroup": "0::/x\n"}
        r.check_members([member], [member])
        with self.assertRaises(r.RecoveryError):
            r.check_members([member], [member, dict(member, pid=124)])
        with self.assertRaises(r.RecoveryError):
            r.check_members([member], [dict(member, start_time="43")])

    def test_lvm_plain_only(self):
        row = dict(
            lv_uuid="uuid",
            lv_attr="-wi-a-----",
            segtype="linear",
            origin="",
            pool_lv="",
            lv_kernel_major="253",
            lv_kernel_minor="0",
        )
        self.assertEqual(
            r.identity_from_rows([row]), {"uuid": "uuid", "major_minor": "253:0"}
        )
        for update in [
            dict(segtype="thin"),
            dict(origin="origin"),
            dict(pool_lv="pool"),
            dict(lv_attr="swi-a-----"),
            dict(lv_kernel_minor="-1"),
        ]:
            with self.subTest(update=update), self.assertRaises(r.RecoveryError):
                r.identity_from_rows([dict(row, **update)])

    def test_verify_bounded_and_identity_stable(self):
        ident = {"uuid": "u", "major_minor": "253:0"}
        with (
            patch.object(r, "inspect_device", return_value=ident),
            patch.object(r, "scan", return_value={"device": ident, "holders": []}),
            patch.object(r, "open_count", side_effect=[2, 1, 0]) as count,
            patch.object(r.time, "sleep") as sleep,
        ):
            self.assertEqual(r.verify("/dev/vg/lv", [], ident)["released"], True)
            self.assertEqual(count.call_count, 3)
            self.assertEqual(sleep.call_count, 2)
        with patch.object(
            r, "inspect_device", return_value=dict(ident, uuid="changed")
        ):
            with self.assertRaises(r.RecoveryError):
                r.verify("/dev/vg/lv", [], ident)

    def test_threads_are_included_in_namespace_members(self):
        def listdir(path):
            return {"/proc": ["123", "self"], "/proc/123/task": ["123", "124"]}[path]

        with (
            patch.object(r, "read_text", return_value="4194304\n"),
            patch.object(r.os, "listdir", side_effect=listdir),
        ):
            self.assertEqual(r.pids(), [123, 124])

    def test_lvm_unknown_target_attributes_rejected(self):
        row = dict(
            lv_uuid="uuid",
            lv_attr="-wi-a-t---",
            segtype="linear",
            origin="",
            pool_lv="",
            lv_kernel_major="253",
            lv_kernel_minor="0",
        )
        with self.assertRaises(r.RecoveryError):
            r.identity_from_rows([row])

    def test_cleanup_timeout_retains_marker_and_releases_pins(self):
        import types

        member = {"pid": 123, "start_time": "42", "cgroup": "0::/x\n"}
        holder = dict(
            member,
            namespace="mnt:[42]",
            root_dev=1,
            root_ino=2,
            mounts=[{"id": 10, "device": "253:0"}],
            members=[member],
        )
        snap = {"device": {"uuid": "u", "major_minor": "253:0"}, "holders": [holder]}
        with (
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r.os, "close") as close,
            patch.object(r.os, "O_CLOEXEC", 0, create=True),
            patch.object(r.os, "O_DIRECTORY", 0, create=True),
            patch.object(r.os, "O_PATH", 0, create=True),
            patch.object(r.os, "readlink", create=True, return_value="mnt:[1]"),
            patch.object(r.os, "open", side_effect=[11, 12, 13]),
            patch.object(
                r.os,
                "fstat",
                side_effect=lambda fd: types.SimpleNamespace(
                    st_dev=1, st_ino=42 if fd == 11 else 2
                ),
            ),
            patch.object(r, "load_host_libc"),
            patch.object(r, "inspect_device", return_value=snap["device"]),
            patch.object(r, "scan", return_value=snap),
            patch.object(r, "check_holder_process"),
            patch.object(r, "pids", return_value=[123]),
            patch.object(r, "process_info", return_value=(member, "mnt:[42]", (1, 2))),
            patch.object(
                r, "spawn_unmount", side_effect=[None, r.RecoveryError("timeout", True)]
            ),
        ):
            with self.assertRaises(r.RecoveryError) as raised:
                r.cleanup("/dev/vg/lv", [], snap, 1)
            self.assertTrue(raised.exception.state_unknown)
            remove.assert_not_called()
            self.assertEqual(
                {call.args[0] for call in close.call_args_list}, {7, 11, 12, 13}
            )

    def test_generic_cleanup_exit_is_unknown(self):
        import io
        import json

        request = {
            "operation": "cleanup",
            "lv_dev": "/dev/vg/lv",
            "reserved": [],
            "unmount_timeout": 1,
            "payload": {},
        }
        output = io.StringIO()
        with (
            patch.object(r.sys, "platform", "linux"),
            patch.object(r.os, "geteuid", return_value=0, create=True),
            patch.object(r.sys, "stdin", io.StringIO(json.dumps(request))),
            patch.object(r.sys, "stdout", output),
            patch.object(r, "cleanup", side_effect=OSError("close failed")),
        ):
            self.assertEqual(r.main(), 1)
        self.assertTrue(json.loads(output.getvalue())["state_unknown"])

    def test_watchdog_kills_only_own_child_and_reports_unknown(self):
        with (
            patch.object(r.os, "fork", return_value=999, create=True),
            patch.object(r.os, "WNOHANG", 1, create=True),
            patch.object(r.os, "waitpid", return_value=(0, 0), create=True),
            patch.object(r.os, "kill") as kill,
            patch.object(r.signal, "SIGKILL", 9, create=True),
            patch.object(r.time, "monotonic", side_effect=[0, 2, 2, 4]),
        ):
            with self.assertRaises(r.RecoveryError) as raised:
                r.spawn_unmount(None, (1, 2, 3), {}, [], 1)
            self.assertTrue(raised.exception.state_unknown)
            kill.assert_called_once_with(999, 9)

    def test_scan_deduplicates_namespace_without_dropping_members(self):
        identity = {"uuid": "u", "major_minor": "253:0"}

        def info(pid):
            return (
                {"pid": pid, "start_time": "42", "cgroup": "0::/x\\n"},
                "mnt:[42]",
                (1, 2),
            )

        with (
            patch.object(r, "inspect_device", return_value=identity),
            patch.object(r, "pids", return_value=[123, 124]),
            patch.object(r, "process_info", side_effect=info),
            patch.object(r, "read_text", return_value=ROOT + TARGET),
        ):
            snapshot = r.scan("/dev/vg/lv", [])
        self.assertEqual(len(snapshot["holders"]), 1)
        self.assertEqual(
            [p["pid"] for p in snapshot["holders"][0]["members"]], [123, 124]
        )

    def test_cleanup_checks_all_before_child(self):
        # A snapshot mismatch must never spawn an unmount worker.
        snap = {"device": {"uuid": "u", "major_minor": "253:0"}, "holders": []}
        with (
            patch.object(r, "create_marker", return_value=7),
            patch.object(r.os, "close"),
            patch.object(r, "remove_marker"),
            patch.object(r, "inspect_device", return_value=snap["device"]),
            patch.object(r, "scan", return_value=dict(snap, holders=[{}])),
            patch.object(r, "spawn_unmount") as spawn,
        ):
            with self.assertRaises(r.RecoveryError):
                r.cleanup("/dev/vg/lv", [], snap, 1)
            spawn.assert_not_called()


if __name__ == "__main__":
    unittest.main()
