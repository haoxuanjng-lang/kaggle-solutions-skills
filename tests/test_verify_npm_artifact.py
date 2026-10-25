# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_npm_artifact", ROOT / "scripts/verify_npm_artifact.py")
artifact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifact)


class NpmArtifact(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.tarball = Path(temporary.name) / "skill.tgz"
        self.tarball.write_bytes(b"original package")
        self.integrity = "sha512-" + base64.b64encode(hashlib.sha512(self.tarball.read_bytes()).digest()).decode()

    def runner(self, command, **kwargs):
        self.assertEqual(command[1:5], ["view", "@owner/skill@1.0.0", "dist.integrity", "--json"])
        self.assertTrue(kwargs["check"])
        return subprocess.CompletedProcess(command, 0, json.dumps(self.integrity).encode())

    def verify(self):
        return artifact.verify("@owner/skill@1.0.0", self.tarball, runner=self.runner)

    def test_original_registry_artifact_is_accepted(self):
        self.assertTrue(self.verify()["verified"])

    def test_changed_tarball_is_rejected_even_without_release_assets(self):
        self.tarball.write_bytes(b"rebuilt different package")
        with self.assertRaisesRegex(ValueError, "differs"):
            self.verify()

    def test_missing_or_unsupported_integrity_is_rejected(self):
        for value in (None, "", {}, "sha1-abc"):
            with self.subTest(value=value):
                self.integrity = value
                with self.assertRaises(ValueError):
                    self.verify()

    def test_registry_failure_does_not_pass(self):
        def fail(command, **kwargs):
            raise subprocess.CalledProcessError(1, command)
        with self.assertRaises(subprocess.CalledProcessError):
            artifact.verify("@owner/skill@1.0.0", self.tarball, runner=fail)

    def test_missing_tarball_fails_before_registry_call(self):
        self.tarball.unlink()
        with self.assertRaises(FileNotFoundError):
            self.verify()
