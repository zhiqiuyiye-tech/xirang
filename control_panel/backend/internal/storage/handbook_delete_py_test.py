"""Handbook deletion operations: exact device evidence, no Kubernetes/ioctls."""

import importlib.util
import io
import json
import pathlib
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "recovery", pathlib.Path(__file__).with_name("namespace_recovery.py")
)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

IDENTITY = {"uuid": "u", "major_minor": "253:0"}
TABLE = (
    "1 0 8:3 / / rw shared:1 - ext4 /dev/sda3 rw\n"
    "10 1 253:0 / /host-data/retired rw shared:578 - ext4 /dev/dm-0 rw\n"
    "11 1 253:10 / /other rw - ext4 /dev/dm-10 rw\n"
)


class HandbookTests(unittest.TestCase):
    def test_identity_check_does_not_require_kernel_namespace_inventory(self):
        request = {
            "operation": "inspect_lv",
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
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "kernel_mount_inventory") as kernel,
        ):
            result = r.main()
        self.assertEqual(result, 0, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["result"], IDENTITY)
        kernel.assert_not_called()

    def test_handbook_scan_matches_device_exactly_even_under_shared_parent(self):
        member = {"pid": 123, "start_time": "100", "cgroup": "0::/unknown-owner\n"}
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "pids", return_value=[123]),
            patch.object(r, "task_view", return_value=("mnt:[42]", 8, 1)),
            patch.object(r, "process_info", return_value=(member, "mnt:[42]", (8, 1))),
            patch.object(r, "read_text", return_value=TABLE),
            patch.object(r, "kernel_mount_inventory") as kernel,
        ):
            snapshot = r.scan("/dev/vg/lv", [], require_local=False)
        self.assertEqual([m["id"] for m in snapshot["holders"][0]["mounts"]], [10])
        kernel.assert_not_called()
        with self.assertRaises(r.RecoveryError):
            r.safe_mounts(r.parse_mountinfo(TABLE), "253:0", [])

    def test_deletion_scan_does_not_inspect_unrelated_process_roots(self):
        member = {"pid": 123, "start_time": "100", "cgroup": "0::/owner\n"}

        def evidence(path):
            if path == "/proc/123/mountinfo":
                return TABLE
            return "1 0 8:3 / / rw - ext4 /dev/sda3 rw\n"

        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "pids", return_value=[2, 123]),
            patch.object(
                r, "task_view", side_effect=lambda pid: ("mnt:[%d]" % pid, 8, 1)
            ),
            patch.object(
                r, "process_info", return_value=(member, "mnt:[42]", (8, 1))
            ) as info,
            patch.object(r, "read_text", side_effect=evidence),
        ):
            snapshot = r.scan("/dev/vg/lv", [], require_local=False)
        self.assertEqual(len(snapshot["holders"]), 1)
        self.assertTrue(all(call.args == (123,) for call in info.call_args_list))

    def test_deletion_scan_reads_one_mountinfo_per_task_view(self):
        reads = []

        def evidence(path):
            reads.append(path)
            return "1 0 8:3 / / rw - ext4 /dev/sda3 rw\n"

        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "pids", return_value=[11, 12, 13]),
            patch.object(r, "task_view", return_value=("mnt:[9]", 8, 1)),
            patch.object(r, "read_text", side_effect=evidence),
        ):
            snapshot = r.scan("/dev/vg/lv", [], require_local=False)
        self.assertEqual(snapshot["holders"], [])
        self.assertEqual(reads, ["/proc/11/mountinfo"])

    def test_deletion_scan_still_reports_holders_of_other_views(self):
        member = {"pid": 123, "start_time": "100", "cgroup": "0::/owner\n"}
        reads = []

        def evidence(path):
            reads.append(path)
            if path == "/proc/123/mountinfo":
                return TABLE
            return "1 0 8:3 / / rw - ext4 /dev/sda3 rw\n"

        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "pids", return_value=[11, 12, 123]),
            patch.object(
                r,
                "task_view",
                side_effect=lambda pid: ("mnt:[9]", 8, 1)
                if pid < 100
                else ("mnt:[42]", 8, 1),
            ),
            patch.object(r, "process_info", return_value=(member, "mnt:[42]", (8, 1))),
            patch.object(r, "read_text", side_effect=evidence),
        ):
            snapshot = r.scan("/dev/vg/lv", [], require_local=False)
        self.assertEqual([m["id"] for m in snapshot["holders"][0]["mounts"]], [10])
        self.assertEqual(reads.count("/proc/11/mountinfo"), 1)
        self.assertNotIn("/proc/12/mountinfo", reads)

    def test_deletion_scan_refuses_a_task_that_moves_during_the_view_read(self):
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "pids", return_value=[11]),
            patch.object(
                r, "task_view", side_effect=[("mnt:[9]", 8, 1), ("mnt:[10]", 8, 1)]
            ),
            patch.object(
                r, "read_text", return_value="1 0 8:3 / / rw - ext4 /dev/sda3 rw\n"
            ),
            self.assertRaises(r.RecoveryError),
        ):
            r.scan("/dev/vg/lv", [], require_local=False)

    def test_task_scale_bound_follows_the_kernel_pid_space(self):
        entries = {
            "/proc": ["self", "1", "2"],
            "/proc/1/task": ["1", "11"],
            "/proc/2/task": ["2"],
        }
        with (
            patch.object(r, "read_text", return_value="4194304\n"),
            patch.object(r.os, "listdir", side_effect=entries.__getitem__),
        ):
            self.assertEqual(r.pids(), [1, 2, 11])

    def test_task_scale_bound_still_refuses_exhausted_pid_space(self):
        entries = {"/proc": ["1"], "/proc/1/task": ["1", "2", "3"]}
        with (
            patch.object(r, "read_text", return_value="2\n"),
            patch.object(r.os, "listdir", side_effect=entries.__getitem__),
            self.assertRaises(r.RecoveryError),
        ):
            r.pids()

    def test_handbook_still_rejects_protected_stacked_and_child_mounts(self):
        for text in (
            TABLE.replace("/host-data/retired", "/proc/retired"),
            TABLE + "12 10 0:9 / /host-data/retired/child rw - tmpfs tmpfs rw\n",
            TABLE + "12 1 0:9 / /host-data/retired rw - tmpfs tmpfs rw\n",
        ):
            with self.subTest(text=text), self.assertRaises(r.RecoveryError):
                r.safe_mounts(r.parse_mountinfo(text), "253:0", [], require_local=False)


if __name__ == "__main__":
    unittest.main()
