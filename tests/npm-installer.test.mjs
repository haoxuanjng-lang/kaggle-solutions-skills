import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(root, 'bin', 'cli.mjs');
function run(args, env = {}) {
  return spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8', env: { ...process.env, ...env } });
}
function withTemp(fn) {
  const folder = mkdtempSync(join(tmpdir(), 'kaggle-skill-test-'));
  try { fn(folder); } finally { rmSync(folder, { recursive: true, force: true }); }
}

test('installation includes the complete knowledge and original source bytes', () => withTemp(folder => {
  const destination = join(folder, 'skill');
  const result = run(['install', '--destination', destination]);
  assert.equal(result.status, 0, result.stderr);
  function compare(relative = '') {
    const source = join(root, 'skills', 'kaggle-solutions-skills', relative);
    for (const entry of readdirSync(source, { withFileTypes: true })) {
      if (entry.name === '__pycache__' || entry.name.endsWith('.pyc')) continue;
      const path = join(relative, entry.name);
      if (entry.isDirectory()) compare(path);
      else assert.deepEqual(readFileSync(join(destination, path)), readFileSync(join(source, entry.name)));
    }
  }
  compare();
  assert.match(result.stdout, /"files": 18/);
}));

test('existing user files are preserved unless update is explicitly selected', () => withTemp(folder => {
  const destination = join(folder, 'skill');
  assert.equal(run(['install', '--destination', destination]).status, 0);
  const entry = join(destination, 'SKILL.md');
  writeFileSync(entry, 'user edit');
  assert.equal(run(['install', '--destination', destination]).status, 1);
  assert.equal(readFileSync(entry, 'utf8'), 'user edit');
  assert.equal(run(['install', '--destination', destination, '--force']).status, 0);
  assert.match(readFileSync(entry, 'utf8'), /name: kaggle-solutions-skills/);
}));

test('CODEX_HOME default and paths with spaces work', () => withTemp(folder => {
  const result = run(['install'], { CODEX_HOME: join(folder, 'Codex Home') });
  assert.equal(result.status, 0, result.stderr);
  assert.match(readFileSync(join(folder, 'Codex Home', 'skills', 'kaggle-solutions-skills', 'SKILL.md'), 'utf8'), /name:/);
}));

test('help/version work and invalid options fail', () => {
  assert.equal(run(['--version']).stdout.trim(), JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version);
  assert.match(run(['--help']).stdout, /Python 3.10/);
  assert.equal(run(['install', '--destination']).status, 1);
  assert.equal(run(['install', '--unknown']).status, 1);
});
