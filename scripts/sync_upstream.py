# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Refresh only changed upstream commits; create a review PR without merging."""
import json
import os
import subprocess
from pathlib import Path
from project import ROOT, SKILL, load_module, check


def run(*command, capture=False):
    result = subprocess.run(command,cwd=ROOT,check=True,text=True,capture_output=capture,encoding='utf-8')
    return result.stdout.strip() if capture else None


def main():
    solutions = load_module('solutions',SKILL/'scripts'/'solutions.py')
    _,_,commit,_ = solutions.upstream_snapshot()
    old = solutions.load_json(solutions.DATA/'manifest.json')['upstream_commit']
    if old == commit:
        print(json.dumps({'changed':False,'upstream_commit':commit}))
        return
    branch = 'automation/archive-' + commit[:12]
    repo = os.environ.get('GH_REPO')
    if not repo:
        raise ValueError('GH_REPO must select the maintained project repository')
    existing = json.loads(run('gh','pr','list','--repo',repo,'--head',branch,'--state','all','--json','url,state',capture=True))
    if existing:
        print(json.dumps({'changed':True,'existing_review':existing,'upstream_commit':commit}))
        return
    run('git','switch','-c',branch)
    result = solutions.refresh(solutions.DATA,ref=commit)
    checked = check()
    if not checked['ok']:
        raise ValueError(json.dumps(checked['errors']))
    run(os.sys.executable,'-m','unittest','discover','-s','tests','-v')
    run('git','config','user.name','github-actions[bot]')
    run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    run('git','add',str(solutions.DATA.relative_to(ROOT)))
    run('git','commit','-m','Refresh Kaggle archive to '+commit[:12])
    run('git','push','origin',branch)
    delta = result['changes']
    body = (f'Update the metadata archive from `{old}` to `{commit}`.\n\n'
            f'Competitions: {result["manifest"]["competition_count"]}; solution link records: {result["manifest"]["solution_link_count"]}.\n'
            f'Added: {len(delta["added"])}; removed: {len(delta["removed"])}; changed: {len(delta["changed"])}.\n\n'
            'Curated method cards and source records are preserved. Review `last-refresh.json` for affected competitions.\n\n'
            'Validation: knowledge/packaging checks and behavior tests passed. No competition runs or scoring were performed.\n')
    body_file = ROOT/'cache'/'upstream-pr-body.md'
    body_file.parent.mkdir(parents=True,exist_ok=True)
    body_file.write_text(body,encoding='utf-8')
    run('gh','pr','create','--repo',repo,'--base','main','--head',branch,
        '--title','Refresh solution archive '+commit[:12],'--body-file',str(body_file))


if __name__ == '__main__':
    main()
