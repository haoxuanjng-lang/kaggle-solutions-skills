# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Run daily deterministic checks and retain an honest, compact maintenance report."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kaggle-solutions-skills"
SCENARIOS = ("otto", "birdclef-2024", "rogii", "amex", "m5")


def run_check(name, command, *, runner=subprocess.run, timeout=600):
    """Continue collecting evidence after failures; never turn a failure into success."""
    started = time.monotonic()
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    try:
        result = runner(command, cwd=ROOT, env=env, timeout=timeout, check=False,
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
        for output in (result.stdout, result.stderr):
            if output:
                print(output, end="" if output.endswith("\n") else "\n", flush=True)
        record = {"name": name, "ok": result.returncode == 0, "returncode": result.returncode}
    except (OSError, subprocess.TimeoutExpired) as exc:
        # Reports retain error types, not environment values or arbitrary subprocess output.
        record = {"name": name, "ok": False, "returncode": None,
                  "error": "timeout" if isinstance(exc, subprocess.TimeoutExpired) else type(exc).__name__}
    record["duration_seconds"] = round(time.monotonic() - started, 3)
    print(json.dumps(record), flush=True)
    return record


def maintenance(*, run=run_check):
    npm = shutil.which("npm") or "npm"
    checks = [
        run("project-integrity", [sys.executable, "scripts/project.py", "check"]),
        run("python-behavior", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        run("npm-installer", [npm, "test"]),
        run("npm-pack-dry-run", [npm, "pack", "--dry-run"]),
    ]
    team = str(SKILL / "scripts" / "research_team.py")
    checks.append(run("scenario-discovery", [sys.executable, team, "scenarios", "--json"]))
    with tempfile.TemporaryDirectory(prefix="kaggle-maintenance-") as temporary:
        for scenario in SCENARIOS:
            destination = str(Path(temporary) / scenario)
            planned = run("scenario-plan:" + scenario,
                          [sys.executable, team, "plan", "--scenario", scenario, "--output", destination])
            checks.append(planned)
            if planned["ok"]:
                checks.append(run("scenario-validate:" + scenario,
                                  [sys.executable, team, "validate", destination]))
            else:
                checks.append({"name": "scenario-validate:" + scenario, "ok": False,
                               "returncode": None, "error": "plan_failed", "skipped": True})
    return {"schema_version": 1, "completed_at": datetime.now(timezone.utc).isoformat(),
            "ok": all(check["ok"] for check in checks), "checks": checks,
            "scope": "Deterministic integrity and research-plan smoke checks; no LLM, training or Kaggle submission.",
            "upstream_review": "Separate Review upstream archive workflow creates a PR only for new commits."}


def render_summary(report):
    lines = ["## Daily maintenance", "", "Result: **" + ("passed" if report["ok"] else "failed") + "**",
             "", report["scope"], "", "| Check | Result |", "|---|---|"]
    for check in report["checks"]:
        state = "passed" if check["ok"] else ("blocked (plan failed)" if check.get("skipped") else "failed")
        lines.append("| " + check["name"] + " | " + state + " |")
    lines.extend(["", report["upstream_review"], "", "Full command output is available in the Actions log.", ""])
    return "\n".join(lines)


def write_report(report, output, *, github_summary=None):
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = render_summary(report)
    (output / "summary.md").write_text(summary, encoding="utf-8")
    if github_summary:
        with Path(github_summary).open("a", encoding="utf-8") as target:
            target.write(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "cache" / "daily-maintenance")
    args = parser.parse_args()
    report = maintenance()
    write_report(report, args.output, github_summary=os.environ.get("GITHUB_STEP_SUMMARY"))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
