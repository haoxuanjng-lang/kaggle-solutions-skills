# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("daily_maintenance", ROOT / "scripts" / "daily_maintenance.py")
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)


class DailyMaintenance(unittest.TestCase):
    def test_failure_does_not_hide_other_checks_or_generate_missing_plan_validation(self):
        calls = []

        def run(name, command):
            calls.append((name, command))
            return {"name": name, "ok": name not in ("python-behavior", "scenario-plan:rogii"), "returncode": 1}

        report = daily.maintenance(run=run)
        self.assertFalse(report["ok"])
        self.assertIn("npm-installer", [name for name, _ in calls])
        self.assertIn("scenario-validate:m5", [name for name, _ in calls])
        self.assertNotIn("scenario-validate:rogii", [name for name, _ in calls])
        blocked = next(check for check in report["checks"] if check["name"] == "scenario-validate:rogii")
        self.assertFalse(blocked["ok"])
        self.assertTrue(blocked["skipped"])
        output_index = next(command for name, command in calls if name == "scenario-plan:otto").index("--output") + 1
        directory = Path(next(command for name, command in calls if name == "scenario-plan:otto")[output_index]).parent
        self.assertFalse(directory.exists(), "Generated smoke artifacts must be removed")

    def test_nonzero_and_timeout_are_failures(self):
        completed = subprocess.CompletedProcess(["tool"], 2, "", "")
        self.assertFalse(daily.run_check("bad", ["tool"], runner=lambda *args, **kwargs: completed)["ok"])

        def timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired("tool", 1, output="secret-not-for-report")

        report = daily.run_check("timeout", ["tool"], runner=timeout)
        self.assertFalse(report["ok"])
        self.assertEqual(report["error"], "timeout")
        self.assertNotIn("secret-not-for-report", json.dumps(report))

    def test_summary_is_retained_after_failed_check_and_appends_to_job_summary(self):
        report = {"ok": False, "scope": "No scored competition run", "upstream_review": "Review only",
                  "checks": [{"name": "example", "ok": False, "returncode": 1}]}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            summary = directory / "job.md"
            summary.write_text("Existing summary\n", encoding="utf-8")
            daily.write_report(report, directory / "report", github_summary=summary)
            self.assertEqual(json.loads((directory / "report/report.json").read_text()), report)
            self.assertIn("Result: **failed**", (directory / "report/summary.md").read_text())
            self.assertTrue(summary.read_text().startswith("Existing summary\n"))


if __name__ == "__main__":
    unittest.main()
