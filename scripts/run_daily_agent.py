# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Run authorized daily Codex maintenance in an isolated, logged git worktree."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SHANGHAI = timezone(timedelta(hours=8))


def command(codex: str, workspace: Path, report: Path) -> list[str]:
    # stdin carries the project prompt, avoiding shell interpolation of its text.
    return [codex, 'exec', '--ignore-user-config', '--cd', str(workspace), '--sandbox', 'danger-full-access',
            '-c', 'approval_policy="never"', '--color', 'never',
            '--output-last-message', str(report), '-']


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--execute', action='store_true', help='Perform daily maintenance')
    mode.add_argument('--smoke', action='store_true', help='Read-only live Codex check; no git writes')
    args = parser.parse_args(argv)
    codex = shutil.which('codex')
    git = shutil.which('git')
    if not codex or not git:
        print(json.dumps({'ok': False, 'error': 'codex and git must be installed and on PATH'}))
        return 1
    stamp = datetime.now(SHANGHAI).strftime('%Y%m%d-%H%M%S-%f')
    run_dir = ROOT / 'cache' / 'maintenance' / 'runs' / stamp
    worktree = ROOT / 'cache' / 'maintenance' / 'worktrees' / stamp
    branch = 'maintenance/' + stamp
    report = run_dir / 'report.md'
    summary = {'mode': 'execute' if args.execute else 'smoke' if args.smoke else 'dry-run',
               'project': str(ROOT), 'worktree': str(worktree), 'branch': branch,
               'log_directory': str(run_dir), 'codex_command': command(codex, worktree, report),
               'prompt_file': str(ROOT / 'config' / 'daily-agent-prompt.md'),
               'timezone': 'Asia/Shanghai'}
    if not args.execute and not args.smoke:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    run_dir.mkdir(parents=True)
    if args.smoke:
        workspace = ROOT
        prompt = ('This is a READ-ONLY smoke test of daily project maintenance. '
                  'Do not edit files, run network operations, create branches, or push. '
                  'Read AGENTS.md and docs/roadmap.md. Report in Chinese the project purpose, '
                  'one concrete maintenance priority and the boundary between research plans '
                  'and actual scored competition results. No more than three short paragraphs.')
    else:
        workspace = worktree
        prompt = (ROOT / 'config' / 'daily-agent-prompt.md').read_text(encoding='utf-8')
    summary['started_at'] = datetime.now(SHANGHAI).isoformat()
    summary['workspace'] = str(workspace)
    status_path = run_dir / 'status.json'
    try:
        background = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
        with (run_dir / 'runner.log').open('w', encoding='utf-8') as log:
            if args.execute:
                subprocess.run([git, '-c', 'http.sslBackend=openssl', 'fetch', 'origin', 'main'],
                               cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True, **background)
                subprocess.run([git, 'worktree', 'add', '-b', branch, str(worktree), 'origin/main'],
                               cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True, **background)
            result = subprocess.run(command(codex, workspace, report), input=prompt,
                                    text=True, encoding='utf-8', cwd=workspace,
                                    stdout=log, stderr=subprocess.STDOUT, **background)
            summary['exit_code'] = result.returncode
            summary['ok'] = result.returncode == 0
            summary['report_written'] = report.is_file()
    except (OSError, subprocess.CalledProcessError) as error:
        summary['ok'] = False
        summary['error'] = str(error)
    summary['finished_at'] = datetime.now(SHANGHAI).isoformat()
    status_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ok': summary['ok'], 'status_file': str(status_path),
                      'report_file': str(report)}, ensure_ascii=False, indent=2))
    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
