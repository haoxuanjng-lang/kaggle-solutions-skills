# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_assets", ROOT / "scripts/release_assets.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseAssets(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.content = {"skill.zip": b"zip", "skill.tgz": b"tar", "SHA256SUMS.txt": b"sums"}
        for name, content in self.content.items():
            (self.directory / name).write_bytes(content)
        self.assets = []
        self.downloads = {}
        self.calls = []

    def existing(self, name, content=None, state="uploaded"):
        number = str(len(self.assets) + 1)
        self.assets.append({"name": name, "state": state,
                            "apiUrl": "https://api.github.com/repos/owner/repo/releases/assets/" + number})
        self.downloads[number] = self.content[name] if content is None else content

    def runner(self, command):
        self.calls.append(command)
        if command[1:3] == ["release", "view"]:
            return json.dumps({"assets": self.assets}).encode()
        if command[1] == "api":
            return self.downloads[command[2].rsplit("/", 1)[1]]
        self.assertEqual(command[1:3], ["release", "upload"])
        self.assertNotIn("--clobber", command)
        return b""

    def publish(self, **kwargs):
        return release.publish_assets("owner/repo", "v1", self.directory, runner=self.runner, **kwargs)

    def test_new_release_uploads_all_files_without_replacement(self):
        self.assertEqual(self.publish()["uploaded"], 3)
        for name in self.content:
            self.assertIn(str((self.directory / name).resolve()), self.calls[-1])

    def test_identical_release_is_read_only(self):
        for name in self.content:
            self.existing(name)
        self.assertEqual(self.publish(), {"verified": 3, "missing": 0, "uploaded": 0})
        self.assertFalse(any(call[1:3] == ["release", "upload"] for call in self.calls))

    def test_partial_release_uploads_only_missing_assets(self):
        self.existing("skill.zip")
        self.assertEqual(self.publish()["uploaded"], 2)
        self.assertNotIn(str((self.directory / "skill.zip").resolve()), self.calls[-1])

    def test_preflight_does_not_upload_missing_assets(self):
        self.assertEqual(self.publish(check_only=True)["uploaded"], 0)
        self.assertEqual(len(self.calls), 1)

    def test_mismatch_even_in_last_checksum_prevents_all_uploads(self):
        self.existing("SHA256SUMS.txt", b"changed")
        with self.assertRaisesRegex(ValueError, "Immutable release asset differs"):
            self.publish()
        self.assertFalse(any(call[1:3] == ["release", "upload"] for call in self.calls))

    def test_incomplete_remote_asset_fails_closed(self):
        self.existing("skill.zip", state="starter")
        with self.assertRaisesRegex(ValueError, "not fully uploaded"):
            self.publish()

    def test_remote_read_failure_cannot_be_treated_as_missing(self):
        def fail(command):
            raise subprocess.CalledProcessError(1, command)
        with self.assertRaises(subprocess.CalledProcessError):
            release.publish_assets("owner/repo", "v1", self.directory, runner=fail)

    def test_missing_local_checksum_fails_before_network(self):
        (self.directory / "SHA256SUMS.txt").unlink()
        with self.assertRaises(ValueError):
            self.publish()
        self.assertEqual(self.calls, [])

    def test_unexpected_asset_url_is_rejected(self):
        self.existing("skill.zip")
        self.assets[0]["apiUrl"] = "https://example.com/123"
        with self.assertRaisesRegex(ValueError, "Unexpected release asset API URL"):
            self.publish()

    def test_concurrent_upload_failure_is_not_retried_with_clobber(self):
        def race(command):
            result = self.runner(command)
            if command[1:3] == ["release", "upload"]:
                raise subprocess.CalledProcessError(1, command)
            return result
        with self.assertRaises(subprocess.CalledProcessError):
            release.publish_assets("owner/repo", "v1", self.directory, runner=race)
        self.assertEqual(sum(call[1:3] == ["release", "upload"] for call in self.calls), 1)


if __name__ == "__main__":
    unittest.main()
