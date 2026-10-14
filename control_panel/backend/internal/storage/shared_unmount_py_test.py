"""Shared host unmount safety tests; never mount or unmount a real volume."""

import copy
import importlib.util
import io
import json
import pathlib
import types
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location(
    "recovery", pathlib.Path(__file__).with_name("namespace_recovery.py")
)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

IDENTITY = {"uuid": "u", "major_minor": "253:0"}
PATH = "/data02/nfs_9de044db"
HOST = "mnt:[1]"
HOST_TABLE = (
    "97 1 8:3 / / rw,relatime shared:1 - ext4 /dev/sda3 rw,seclabel\n"
    "1091 97 253:0 / /data02/nfs_9de044db rw,relatime shared:578 "
    "- ext4 /dev/mapper/vg_data_nvme1n1p1-9de044db rw,seclabel,stripe=32\n"
)
FOREIGN_TABLE = (
    "2 0 0:3 / / rw - overlay overlay rw\n"
    "10 2 8:3 /data02 /host-data rw master:1 - ext4 /dev/sda3 rw\n"
    "11 10 253:0 / /host-data/nfs_9de044db rw master:578 - ext4 /dev/dm-0 rw\n"
)


def view(pid, text, cgroup="0::/test\n"):
    return {
        "root": (8, pid),
        "members": [{"pid": pid, "start_time": "100", "cgroup": cgroup}],
        "mounts": r.parse_mountinfo(text),
    }


def views():
    return {
        HOST: view(1, HOST_TABLE, "0::/init.scope\n"),
        "mnt:[42]": view(123, FOREIGN_TABLE),
    }


def plan(evidence=None):
    return r.shared_unmount_plan_from_views(
        IDENTITY, HOST, evidence or views(), [PATH], ["/data01"]
    )


class SharedUnmountTests(unittest.TestCase):
    def test_deletion_inspection_accepts_real_shared_host_mount(self):
        request = {
            "operation": "delete_inspect",
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
            patch.object(r, "read_text", return_value=HOST_TABLE),
        ):
            status = r.main()
        self.assertEqual(status, 0, output.getvalue())
        self.assertEqual(
            json.loads(output.getvalue())["result"],
            {"device": IDENTITY, "requires_host_authorization": True},
        )
        # The original (also used by resize) private-only guard is preserved.
        with self.assertRaises(r.RecoveryError):
            r.safe_mounts(r.parse_mountinfo(HOST_TABLE), "253:0", [])

    def test_real_shared_host_and_slave_holder_are_in_authorized_plan(self):
        result = plan()
        self.assertEqual(result["device"], IDENTITY)
        self.assertEqual(result["host"]["pid"], 1)
        self.assertEqual(result["host"]["mounts"][0]["id"], 1091)
        self.assertEqual(len(result["holders"]), 1)
        self.assertEqual(
            result["holders"][0]["mounts"][0]["path"], "/host-data/nfs_9de044db"
        )
        self.assertRegex(result["proof"], r"^[0-9a-f]{64}$")

    def test_unknown_members_are_preserved_for_authorization(self):
        evidence = views()
        member = {"pid": 124, "start_time": "200", "cgroup": "0::/unknown\n"}
        evidence["mnt:[42]"]["members"].append(member)
        self.assertIn(member, plan(evidence)["holders"][0]["members"])

    def test_private_nonpropagating_lv_holders_still_require_authorization(self):
        evidence = views()
        evidence["mnt:[42]"] = view(
            123, FOREIGN_TABLE.replace(" master:1", "").replace(" master:578", "")
        )
        self.assertEqual(len(plan(evidence)["holders"]), 1)

    def test_peer_slave_chain_includes_all_target_holders(self):
        evidence = views()
        evidence["mnt:[42]"]["mounts"][1]["optional"] = ["shared:7", "master:1"]
        evidence["mnt:[43]"] = view(125, FOREIGN_TABLE.replace("master:1", "master:7"))
        self.assertEqual(len(plan(evidence)["holders"]), 2)

    def test_propagation_must_never_unmount_other_device_or_root(self):
        for change in ({"device": "8:9"}, {"root": "/another"}):
            evidence = views()
            evidence["mnt:[42]"]["mounts"][2].update(change)
            with self.subTest(change=change), self.assertRaises(r.RecoveryError):
                plan(evidence)

    def test_receiver_with_missing_mount_is_not_a_holder(self):
        evidence = views()
        evidence["mnt:[42]"]["mounts"].pop()
        self.assertEqual(plan(evidence)["holders"], [])

    def test_root_offset_outside_receiver_is_not_affected(self):
        evidence = views()
        receiver = evidence["mnt:[42]"]["mounts"]
        receiver[1]["root"] = "/elsewhere"
        receiver.pop()
        self.assertEqual(plan(evidence)["holders"], [])

    def test_stacked_or_child_mounts_are_rejected(self):
        for record in (
            {
                "id": 12,
                "parent_id": 11,
                "device": "0:9",
                "root": "/",
                "path": "/host-data/nfs_9de044db/child",
                "optional": [],
            },
            {
                "id": 12,
                "parent_id": 10,
                "device": "0:9",
                "root": "/",
                "path": "/host-data/nfs_9de044db",
                "optional": [],
            },
        ):
            evidence = views()
            evidence["mnt:[42]"]["mounts"].append(record)
            with self.subTest(record=record), self.assertRaises(r.RecoveryError):
                plan(evidence)

    def test_unknown_propagation_and_cycles_are_rejected(self):
        for optional in (
            ["shared:0"],
            ["shared:1", "shared:2"],
            ["future:1"],
            ["shared:1", "master:1"],
        ):
            evidence = views()
            evidence[HOST]["mounts"][0]["optional"] = optional
            with self.subTest(optional=optional), self.assertRaises(r.RecoveryError):
                plan(evidence)

    def test_multiple_host_mounts_or_changed_detected_paths_are_rejected(self):
        evidence = views()
        other = copy.deepcopy(evidence[HOST]["mounts"][1])
        other.update(id=1092, path="/other")
        evidence[HOST]["mounts"].append(other)
        with self.assertRaises(r.RecoveryError):
            plan(evidence)
        with self.assertRaises(r.RecoveryError):
            r.shared_unmount_plan_from_views(IDENTITY, HOST, views(), ["/wrong"], [])

    def test_proof_covers_mounts_roots_members_and_device(self):
        original = plan()["proof"]
        for field in ("root", "members", "mounts"):
            evidence = views()
            if field == "root":
                evidence["mnt:[42]"][field] = (8, 999)
            elif field == "members":
                evidence["mnt:[42]"][field][0]["start_time"] = "999"
            else:
                evidence["mnt:[42]"][field][0]["optional"] = ["shared:99"]
            self.assertNotEqual(plan(evidence)["proof"], original)
        changed = dict(IDENTITY, uuid="changed")
        self.assertNotEqual(
            r.shared_unmount_plan_from_views(changed, HOST, views(), [PATH], [])[
                "proof"
            ],
            original,
        )

    def test_stale_plan_never_spawns_unmount(self):
        snapshot = plan()
        changed = dict(snapshot, proof="0" * 64)
        with (
            patch.object(r, "shared_host_plan", return_value=changed),
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r.os, "close"),
            patch.object(r, "spawn_unmount") as spawn,
            self.assertRaises(r.RecoveryError),
        ):
            r.unmount_shared_host("/dev/vg/lv", [], snapshot, 1)
        spawn.assert_not_called()
        remove.assert_called_once()

    def test_supervised_host_unmount_retains_marker_on_unknown_timeout(self):
        snapshot = plan()
        with (
            patch.object(r, "shared_host_plan", return_value=snapshot),
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r, "pin_holder", return_value=(11, 12, 13)),
            patch.object(r.os, "close") as close,
            patch.object(r, "load_host_libc"),
            patch.object(
                r, "spawn_unmount", side_effect=[None, r.RecoveryError("timeout", True)]
            ) as spawn,
            self.assertRaises(r.RecoveryError) as raised,
        ):
            r.unmount_shared_host("/dev/vg/lv", [], snapshot, 1)
        self.assertTrue(raised.exception.state_unknown)
        remove.assert_not_called()
        self.assertEqual(
            {call.args[0] for call in close.call_args_list}, {7, 11, 12, 13}
        )
        self.assertEqual(spawn.call_count, 2)
        self.assertEqual(
            spawn.call_args.kwargs["host_request"], ("/dev/vg/lv", snapshot)
        )

    def test_host_unmount_generic_failure_is_quarantined(self):
        snapshot = plan()
        with (
            patch.object(r, "shared_host_plan", return_value=snapshot),
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r, "pin_holder", side_effect=OSError("pin failed")),
            patch.object(r.os, "close"),
            patch.object(r, "load_host_libc"),
            self.assertRaises(r.RecoveryError) as raised,
        ):
            r.unmount_shared_host("/dev/vg/lv", [], snapshot, 1)
        self.assertTrue(raised.exception.state_unknown)
        remove.assert_not_called()

    def test_mount_namespace_without_identifiable_tasks_is_rejected(self):
        def info(pid):
            return {"pid": pid, "start_time": "100", "cgroup": "0::/test"}, HOST, (8, 1)

        with (
            patch.object(r, "pids", return_value=[1]),
            patch.object(r, "process_info", side_effect=info),
            patch.object(r, "read_text", return_value=HOST_TABLE),
            patch.object(r.os, "listdir", return_value=["3"]),
            patch.object(r.os, "readlink", return_value="mnt:[999]", create=True),
            self.assertRaises(r.RecoveryError),
        ):
            r.collect_mount_views()

    def test_hidden_namespace_root_views_are_rejected(self):
        def info(pid):
            return (
                {"pid": pid, "start_time": "100", "cgroup": "0::/test"},
                HOST,
                (8, pid),
            )

        with (
            patch.object(r, "pids", return_value=[1, 123]),
            patch.object(r, "process_info", side_effect=info),
            patch.object(r, "read_text", return_value=HOST_TABLE),
            patch.object(r.os, "listdir", return_value=[]),
            self.assertRaises(r.RecoveryError),
        ):
            r.collect_mount_views()

    def test_transient_host_members_do_not_invalidate_proof(self):
        evidence = views()
        evidence[HOST]["members"].append(
            {"pid": 999, "start_time": "999", "cgroup": "0::/sshd\n"}
        )
        self.assertEqual(plan(evidence)["proof"], plan()["proof"])

    def test_successful_host_unmount_confirms_release_and_closes_pins(self):
        snapshot = plan()
        with (
            patch.object(r, "shared_host_plan", return_value=snapshot),
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r, "pin_holder", return_value=(11, 12, 13)),
            patch.object(r, "load_host_libc"),
            patch.object(r, "spawn_unmount") as spawn,
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(
                r, "read_text", return_value=HOST_TABLE.splitlines()[0] + "\n"
            ),
            patch.object(r.os, "close") as close,
        ):
            result = r.unmount_shared_host("/dev/vg/lv", [], snapshot, 1)
        self.assertEqual(result, {"unmounted": True, "device": IDENTITY})
        self.assertEqual(spawn.call_count, 2)
        remove.assert_called_once()
        self.assertEqual(
            {call.args[0] for call in close.call_args_list}, {7, 11, 12, 13}
        )

    def test_kernel_namespace_inventory_includes_processless_namespace(self):
        def ioctl(fd, command, argument):
            argument._obj.nr_mounts = 2 if fd == 10 else 3
            argument._obj.mnt_ns_id = fd
            if command == 0x8010B70A:
                return 0
            if command == 0x8010B70B and fd == 10:
                argument._obj.nr_mounts = 3
                argument._obj.mnt_ns_id = 11
                return 11
            r.ctypes.set_errno(r.errno.ENOENT)
            return -1

        libc = types.SimpleNamespace(ioctl=ioctl)
        with (
            patch.object(r.ctypes, "CDLL", return_value=libc),
            patch.object(
                r.os,
                "uname",
                return_value=types.SimpleNamespace(machine="x86_64"),
                create=True,
            ),
            patch.object(
                r.os, "readlink", return_value="user:[4026531837]", create=True
            ),
            patch.object(r, "read_text", return_value="CapEff:\t0000000000200000\n"),
            patch.object(r.os, "O_CLOEXEC", 0, create=True),
            patch.object(r.os, "open", return_value=10),
            patch.object(
                r.os,
                "fstat",
                side_effect=lambda fd: types.SimpleNamespace(
                    st_ino=1 if fd == 10 else 42
                ),
            ),
            patch.object(r.os, "close") as close,
        ):
            inventory = r.kernel_mount_inventory()
        self.assertEqual(set(inventory), {HOST, "mnt:[42]"})
        self.assertEqual(inventory["mnt:[42]"], {"id": 11, "mounts": 3})
        self.assertEqual({call.args[0] for call in close.call_args_list}, {10, 11})

    def test_kernel_inventory_capability_missing_fails_closed(self):
        def ioctl(fd, command, argument):
            r.ctypes.set_errno(r.errno.ENOTTY)
            return -1

        with (
            patch.object(
                r.ctypes, "CDLL", return_value=types.SimpleNamespace(ioctl=ioctl)
            ),
            patch.object(
                r.os,
                "uname",
                return_value=types.SimpleNamespace(machine="x86_64"),
                create=True,
            ),
            patch.object(
                r.os, "readlink", return_value="user:[4026531837]", create=True
            ),
            patch.object(r, "read_text", return_value="CapEff:\t0000000000200000\n"),
            patch.object(r.os, "O_CLOEXEC", 0, create=True),
            patch.object(r.os, "open", return_value=10),
            patch.object(r.os, "close"),
            self.assertRaises(r.RecoveryError),
        ):
            r.kernel_mount_inventory()

    def test_kernel_inventory_must_match_complete_process_mount_views(self):
        evidence = views()
        baseline = {
            HOST: {"id": 100, "mounts": 2},
            "mnt:[42]": {"id": 101, "mounts": 3},
        }
        for case in ("processless", "hidden_mount", "changed_inventory", "complete"):
            first = copy.deepcopy(baseline)
            second = copy.deepcopy(baseline)
            if case == "processless":
                first["mnt:[999]"] = {"id": 999, "mounts": 1}
                second = first
            elif case == "hidden_mount":
                first[HOST]["mounts"] = 3
                second = first
            elif case == "changed_inventory":
                second["mnt:[42]"]["id"] = 102
            host_member = evidence[HOST]["members"][0]
            with (
                self.subTest(case=case),
                patch.object(r, "inspect_device", return_value=IDENTITY),
                patch.object(
                    r, "process_info", return_value=(host_member, HOST, (8, 1))
                ),
                patch.object(r.os, "readlink", return_value=HOST, create=True),
                patch.object(
                    r.os, "stat", return_value=types.SimpleNamespace(st_dev=8, st_ino=1)
                ),
                patch.object(r, "collect_mount_views", return_value=evidence),
                patch.object(r, "kernel_mount_inventory", side_effect=[first, second]),
            ):
                if case == "complete":
                    result = r.shared_host_plan("/dev/vg/lv", [], IDENTITY, [PATH])
                    self.assertEqual(len(result["holders"]), 1)
                else:
                    with self.assertRaises(r.RecoveryError):
                        r.shared_host_plan("/dev/vg/lv", [], IDENTITY, [PATH])

    def test_shared_release_requires_complete_kernel_views_and_zero_open_count(self):
        evidence = {HOST: view(1, HOST_TABLE.splitlines()[0] + "\n")}
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(
                r, "complete_mount_views", return_value=(evidence, {}), create=True
            ),
            patch.object(r, "open_count", side_effect=[1, 0]) as count,
            patch.object(r.time, "sleep"),
        ):
            self.assertTrue(
                r.verify_shared_release("/dev/vg/lv", [], IDENTITY)["released"]
            )
        self.assertEqual(count.call_count, 2)
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(
                r,
                "complete_mount_views",
                side_effect=r.RecoveryError("processless namespace"),
                create=True,
            ),
            patch.object(r, "open_count") as count,
            self.assertRaises(r.RecoveryError),
        ):
            r.verify_shared_release("/dev/vg/lv", [], IDENTITY)
        count.assert_not_called()

    def test_maintenance_mode_does_not_call_unsupported_kernel_api(self):
        evidence = views()
        member = evidence[HOST]["members"][0]
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "process_info", return_value=(member, HOST, (8, 1))),
            patch.object(r.os, "readlink", return_value=HOST, create=True),
            patch.object(
                r.os, "stat", return_value=types.SimpleNamespace(st_dev=8, st_ino=1)
            ),
            patch.object(r, "collect_mount_views", return_value=evidence),
            patch.object(
                r, "kernel_mount_inventory", side_effect=r.RecoveryError("ENOTTY")
            ) as kernel,
        ):
            result = r.shared_host_plan(
                "/dev/vg/lv", [], IDENTITY, [PATH], mode="maintenance"
            )
        kernel.assert_not_called()
        self.assertEqual(result["mode"], "maintenance")
        self.assertEqual(len(result["holders"]), 1)
        self.assertNotEqual(result["proof"], plan(evidence)["proof"])

    def test_strict_mode_never_falls_back_when_kernel_api_is_missing(self):
        evidence = views()
        member = evidence[HOST]["members"][0]
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "process_info", return_value=(member, HOST, (8, 1))),
            patch.object(r.os, "readlink", return_value=HOST, create=True),
            patch.object(
                r.os, "stat", return_value=types.SimpleNamespace(st_dev=8, st_ino=1)
            ),
            patch.object(r, "collect_mount_views") as visible,
            patch.object(
                r, "kernel_mount_inventory", side_effect=r.RecoveryError("ENOTTY")
            ),
            self.assertRaises(r.RecoveryError),
        ):
            r.shared_host_plan("/dev/vg/lv", [], IDENTITY, [PATH])
        visible.assert_not_called()

    def test_maintenance_release_still_requires_absence_and_zero_open_count(self):
        evidence = {HOST: view(1, HOST_TABLE.splitlines()[0] + "\n")}
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "collect_mount_views", return_value=evidence),
            patch.object(r, "kernel_mount_inventory") as kernel,
            patch.object(r, "open_count", return_value=0),
        ):
            result = r.verify_shared_release(
                "/dev/vg/lv", [], IDENTITY, mode="maintenance"
            )
        self.assertTrue(result["released"])
        kernel.assert_not_called()
        with (
            patch.object(r, "inspect_device", return_value=IDENTITY),
            patch.object(r, "collect_mount_views", return_value=views()),
            patch.object(r, "open_count") as count,
            self.assertRaises(r.RecoveryError),
        ):
            r.verify_shared_release("/dev/vg/lv", [], IDENTITY, mode="maintenance")
        count.assert_not_called()

    def test_unknown_host_recovery_mode_is_rejected(self):
        with self.assertRaises(r.RecoveryError):
            r.shared_host_plan(
                "/dev/vg/lv", [], IDENTITY, [PATH], mode="automatic-fallback"
            )

    def test_actual_unmount_failure_always_retains_uncertain_marker(self):
        snapshot = plan()
        with (
            patch.object(r, "shared_host_plan", return_value=snapshot),
            patch.object(r, "create_marker", return_value=7),
            patch.object(r, "remove_marker") as remove,
            patch.object(r, "pin_holder", return_value=(11, 12, 13)),
            patch.object(r, "load_host_libc"),
            patch.object(r.os, "close"),
            patch.object(
                r,
                "spawn_unmount",
                side_effect=[None, r.RecoveryError("helper signaled")],
            ),
            self.assertRaises(r.RecoveryError) as raised,
        ):
            r.unmount_shared_host("/dev/vg/lv", [], snapshot, 1)
        self.assertTrue(raised.exception.state_unknown)
        remove.assert_not_called()

    def test_child_rejects_changed_proof_before_syscall(self):
        snapshot = plan()
        libc = types.SimpleNamespace(
            prctl=Mock(return_value=0),
            setns=Mock(return_value=0),
            umount2=Mock(return_value=0),
        )
        with (
            patch.object(
                r, "shared_host_plan", return_value=dict(snapshot, proof="0" * 64)
            ),
            patch.object(r.os, "fchdir", create=True),
            patch.object(r.os, "chroot", create=True),
            patch.object(r.os, "chdir"),
            patch.object(
                r.os, "stat", return_value=types.SimpleNamespace(st_dev=8, st_ino=1)
            ),
            patch.object(r.os, "_exit", side_effect=SystemExit(1)) as exit_child,
            self.assertRaises(SystemExit),
        ):
            r.child_unmount(
                libc,
                11,
                12,
                13,
                snapshot["host"],
                [],
                False,
                r.os.getppid(),
                ("/dev/vg/lv", snapshot),
            )
        libc.umount2.assert_not_called()
        exit_child.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
