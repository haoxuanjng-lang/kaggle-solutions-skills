import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import * as plugin from '../integrations/deepseek-harness/index.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const signal = () => new AbortController().signal;
const call = (tools, name, args = {}) => tools.find(tool => tool.name === name).execute(args, { signal: signal() });

test('offline tools query shipped archive and retain evidence boundaries', async () => {
  const tools = plugin.createTools();
  assert.equal(tools.length, 6);
  const stats = await call(tools, 'kaggle_solutions_stats');
  assert.ok(stats.data.competition_count > 0);
  assert.match(stats.evidenceBoundary, /not reproduced/);
  const search = await call(tools, 'kaggle_solutions_search', { query: 'recommender', modality: 'recommender', limit: 2 });
  assert.ok(search.data.results.length <= 2);
  const competition = await call(tools, 'kaggle_solutions_show', { competition: 'otto-recommender-system', topRank: 5 });
  assert.equal(competition.data.results[0].slug, 'otto-recommender-system');
  assert.match(competition.data.retrieval, /linked_unread/);
  const patterns = await call(tools, 'kaggle_solutions_patterns', { query: 'retrieval' });
  assert.ok(patterns.data.some(card => card.id === 'retrieval-then-ranking'));
});

test('model arguments reject malformed values and arbitrary command fields', async () => {
  const tools = plugin.createTools();
  await assert.rejects(call(tools, 'kaggle_solutions_stats', { command: 'refresh' }), /Unknown argument/);
  await assert.rejects(call(tools, 'kaggle_solutions_search', { query: 'otto', limit: 0 }), /integer/);
  await assert.rejects(call(tools, 'kaggle_solutions_search', { query: 'otto', modality: 'invented' }), /modality/);
  await assert.rejects(call(tools, 'kaggle_solutions_search', { query: '' }), /non-empty/);
  assert.throws(() => plugin.createTools({ python: '' }), /python/);
  assert.throws(() => plugin.createTools({ workspaceRoot: 'relative' }), /absolute/);
});

test('research plan writes five packets only in explicit workspace and does not dispatch agents', async () => {
  const workspace = await mkdtemp(path.join(tmpdir(), 'kaggle-harness-'));
  try {
    const tools = plugin.createTools({ workspaceRoot: workspace });
    const scenarios = await call(tools, 'kaggle_research_scenarios');
    assert.ok(scenarios.data.some(item => item.id === 'otto'));
    const outputDir = path.join(workspace, 'otto-research');
    const result = await call(tools, 'kaggle_research_plan', { scenario: 'otto', outputDir });
    assert.equal(result.data.task_count, 5);
    assert.equal(result.data.dispatch_status, 'not_dispatched');
    const plan = JSON.parse(await readFile(path.join(outputDir, 'plan.json'), 'utf8'));
    assert.equal(plan.tasks.length, 5);
    await assert.rejects(call(tools, 'kaggle_research_plan', { scenario: 'otto', outputDir }), /failed/i);
    await assert.rejects(call(tools, 'kaggle_research_plan', { scenario: 'otto', outputDir: workspace }), /new child/);
    await assert.rejects(call(tools, 'kaggle_research_plan', { scenario: 'otto', outputDir: path.join(path.dirname(workspace), 'escape') }), /inside workspaceRoot/);
    const sourceTools = plugin.createTools({ workspaceRoot: root });
    await assert.rejects(call(sourceTools, 'kaggle_research_plan', { scenario: 'otto', outputDir: path.join(root, 'overwrite-source') }), /overlap/);
  } finally { await rm(workspace, { recursive: true, force: true }); }
});

test('pre-cancelled calls never start Python; unavailable Python fails honestly', async () => {
  const controller = new AbortController();
  controller.abort(new Error('cancelled by caller'));
  const tools = plugin.createTools();
  await assert.rejects(tools[0].execute({}, { signal: controller.signal }), /cancelled by caller/);
  await assert.rejects(call(plugin.createTools({ python: 'nonexistent-kaggle-python-executable' }), 'kaggle_solutions_stats'), /Offline research command failed/);
});

test('in-flight cancellation terminates the owned Python process and later queries still work', async () => {
  const controller = new AbortController();
  const tools = plugin.createTools();
  const running = tools[0].execute({}, { signal: controller.signal });
  controller.abort();
  await assert.rejects(running, /aborted/i);
  const later = await call(tools, 'kaggle_solutions_stats');
  assert.ok(later.data.competition_count > 0);
});

const runtimeBase = process.env.DEEPSEEK_RUNTIME_NODE_MODULES;
test('official Cordis and ToolRuntime register, dispatch, and dispose the real plugin', { skip: !runtimeBase && 'Set DEEPSEEK_RUNTIME_NODE_MODULES to test exact official npm runtime' }, async () => {
  const require = createRequire(path.join(path.resolve(runtimeBase), '../package.json'));
  const load = name => import(pathToFileURL(require.resolve(name)));
  const { Context } = await load('@deepseek-ai/cordis');
  const { ToolRuntime } = await load('@deepseek-ai/dsh-tools');
  const { SystemPrompt } = await load('@deepseek-ai/dsh-system-prompt');
  const manifest = JSON.parse(await readFile(require.resolve('@deepseek-ai/dsh-tools/package.json'), 'utf8'));
  assert.equal(manifest.version, '0.2.0-rc.2');
  const ctx = new Context();
  const promptFiber = ctx.plugin(SystemPrompt);
  const toolFiber = ctx.plugin(ToolRuntime);
  const pluginFiber = ctx.plugin(plugin);
  try {
    const deadline = Date.now() + 2000;
    while ((ctx.tools?.schemas().length ?? 0) !== 6 && Date.now() < deadline) {
      await new Promise(resolve => setTimeout(resolve, 10));
    }
    assert.equal(ctx.tools.schemas().length, 6);
    const result = await ctx.tools.execute({ callId: 'official-runtime-smoke', name: 'kaggle_solutions_show', arguments: { competition: 'otto-recommender-system' }, signal: signal() });
    assert.equal(result.isError, false);
    assert.equal(result.value.data.results[0].slug, 'otto-recommender-system');
    assert.match(result.content[0].text, /evidenceBoundary/);
    const invalid = await ctx.tools.execute({ callId: 'invalid', name: 'kaggle_solutions_search', arguments: { query: 'otto', limit: 0 }, signal: signal() });
    assert.equal(invalid.isError, true);
    await pluginFiber.dispose();
    assert.deepEqual(ctx.tools.schemas(), []);
  } finally {
    await pluginFiber.dispose();
    await toolFiber.dispose();
    await promptFiber.dispose();
  }
});
