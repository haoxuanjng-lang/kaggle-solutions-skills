/** Native Cordis tools. Host owns model calls; this bundle owns offline research only. */
import { execFile } from 'node:child_process';
import { realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const name = 'kaggle-solutions-research';
export const inject = ['tools'];
const packageRoot = fileURLToPath(new URL('../../', import.meta.url));
const scriptRoot = path.join(packageRoot, 'skills/kaggle-solutions-skills/scripts');
const modalities = ['tabular', 'time-series', 'vision', 'text', 'audio', 'recommender', 'simulation', 'optimization', 'unknown'];
const boundary = 'Archive links are linked_unread; author reports and transfer hypotheses are not reproduced results. No training, cloud execution or submission is performed.';

function text(value, key, { optional = false, max = 2000 } = {}) {
  if (optional && value === undefined) return undefined;
  if (typeof value !== 'string' || !value.trim() || value.length > max || value.includes('\0')) {
    throw new TypeError(`${key} must be a non-empty string of at most ${max} characters`);
  }
  return value;
}
function integer(value, key, fallback, max = 100) {
  if (value === undefined) return fallback;
  if (!Number.isInteger(value) || value < 1 || value > max) throw new TypeError(`${key} must be an integer from 1 to ${max}`);
  return value;
}
function argumentsObject(value, allowed) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new TypeError('Arguments must be an object');
  for (const key of Object.keys(value)) if (!allowed.includes(key)) throw new TypeError(`Unknown argument: ${key}`);
  return value;
}
function within(parent, child) {
  const relative = path.relative(parent, child);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}
function config(value = {}) {
  argumentsObject(value, ['python', 'timeoutMs', 'maxBufferBytes', 'workspaceRoot']);
  const python = text(value.python ?? 'python', 'python', { max: 4096 });
  const timeoutMs = integer(value.timeoutMs, 'timeoutMs', 30000, 300000);
  const maxBufferBytes = integer(value.maxBufferBytes, 'maxBufferBytes', 8 * 1024 * 1024, 64 * 1024 * 1024);
  const workspaceRoot = value.workspaceRoot === undefined ? process.cwd() : text(value.workspaceRoot, 'workspaceRoot', { max: 4096 });
  if (!path.isAbsolute(workspaceRoot)) throw new TypeError('workspaceRoot must be absolute');
  return { python, timeoutMs, maxBufferBytes, workspaceRoot };
}

async function run(settings, script, args, signal) {
  signal?.throwIfAborted();
  return new Promise((resolve, reject) => {
    let childClosed;
    const child = execFile(settings.python, [path.join(scriptRoot, script), ...args], {
      shell: false, windowsHide: true, encoding: 'utf8', signal,
      timeout: settings.timeoutMs, maxBuffer: settings.maxBufferBytes,
      env: { ...process.env, PYTHONUTF8: '1', PYTHONIOENCODING: 'utf-8' },
    }, async (error, stdout, stderr) => {
      // Abort may invoke execFile's callback before process close. Wait for owned
      // subprocess/pipes to settle before returning control to the host.
      await childClosed;
      if (error) {
        reject(new Error(`Offline research command failed: ${error.message}${stdout ? `\n${stdout.trim()}` : ''}${stderr ? `\n${stderr.trim()}` : ''}`, { cause: error }));
        return;
      }
      try { resolve(JSON.parse(stdout)); }
      catch (parseError) { reject(new Error('Research command did not return JSON', { cause: parseError })); }
    });
    childClosed = new Promise(done => child.once('close', done));
  });
}

const string = description => ({ type: 'string', description });
const number = description => ({ type: 'integer', minimum: 1, maximum: 100, description });
function tool(settings, { name: toolName, description, properties, required = [], build, writable = false }) {
  return {
    name: toolName, description,
    parameters: { type: 'object', properties, required, additionalProperties: false },
    output: {
      schema: { type: 'object', properties: { command: { type: 'string' }, evidenceBoundary: { type: 'string' }, data: {} }, required: ['command', 'evidenceBoundary', 'data'], additionalProperties: false },
      render: (_args, value) => [{ type: 'text', text: JSON.stringify(value, null, 2) }],
    },
    isConcurrencySafe: () => !writable,
    timeoutMs: settings.timeoutMs,
    async execute(raw, exec) {
      const args = argumentsObject(raw, Object.keys(properties));
      const invocation = await build(args);
      return { command: toolName, evidenceBoundary: boundary, data: await run(settings, invocation.script ?? 'solutions.py', invocation.args, exec.signal) };
    },
  };
}

/** Exposed for deterministic tests; registration itself runs inside the owning Cordis effect. */
export function createTools(options = {}) {
  const settings = config(options);
  return [
    tool(settings, { name: 'kaggle_solutions_stats', description: 'Read pinned archive counts and provenance. Counts do not imply sources were read or results reproduced.', properties: {}, build: () => ({ args: ['stats'] }) }),
    tool(settings, {
      name: 'kaggle_solutions_search', description: 'Search Kaggle archive metadata and curated method associations offline. Results include linked_unread references.',
      properties: { query: string('Search terms in English or Chinese'), modality: { ...string('Heuristic modality filter'), enum: modalities }, limit: number('Maximum competitions, default 5'), topRank: number('Archive numeric rank filter'), solutionsLimit: number('Maximum links per competition, default 5') }, required: ['query'],
      build(args) {
        const query = text(args.query, 'query');
        const cli = ['search', query, '--json', '--limit', String(integer(args.limit, 'limit', 5)), '--solutions-limit', String(integer(args.solutionsLimit, 'solutionsLimit', 5))];
        if (args.modality !== undefined) {
          if (!modalities.includes(args.modality)) throw new TypeError('Unknown modality');
          cli.push('--modality', args.modality);
        }
        if (args.topRank !== undefined) cli.push('--top-rank', String(integer(args.topRank, 'topRank')));
        return { args: cli };
      },
    }),
    tool(settings, {
      name: 'kaggle_solutions_show', description: 'Retrieve archived writeup links for a competition slug or URL; archive claims require primary-source verification.',
      properties: { competition: string('Exact archive competition slug or Kaggle competition URL'), topRank: number('Archive numeric rank filter'), solutionsLimit: number('Maximum links, default 5') }, required: ['competition'],
      build(args) {
        const cli = ['show', text(args.competition, 'competition'), '--json', '--solutions-limit', String(integer(args.solutionsLimit, 'solutionsLimit', 5))];
        if (args.topRank !== undefined) cli.push('--top-rank', String(integer(args.topRank, 'topRank')));
        return { args: cli };
      },
    }),
    tool(settings, { name: 'kaggle_solutions_patterns', description: 'Retrieve reviewed decision cards with sources, transfer conditions and minimal experimental hypotheses.', properties: { query: string('Optional method terms; omit for all curated cards') }, build: args => ({ args: ['patterns', args.query === undefined ? '' : text(args.query, 'query'), '--json'] }) }),
    tool(settings, { name: 'kaggle_research_scenarios', description: 'List real historical competition scenarios for the research team workflow. Scenarios do not claim current leaderboard activity.', properties: {}, build: () => ({ script: 'research_team.py', args: ['scenarios', '--json'] }) }),
    tool(settings, {
      name: 'kaggle_research_plan', description: 'Create research role packets and a dependency graph for a real historical competition scenario in a new workspace directory. Does not launch agents or execute competitions.',
      properties: { scenario: string('Scenario ID from kaggle_research_scenarios'), outputDir: string('Absolute new output directory inside configured workspaceRoot') }, required: ['scenario', 'outputDir'], writable: true,
      async build(args) {
        const scenario = text(args.scenario, 'scenario', { max: 80 });
        const output = text(args.outputDir, 'outputDir', { max: 4096 });
        if (!path.isAbsolute(output)) throw new TypeError('outputDir must be absolute');
        const workspace = await realpath(settings.workspaceRoot);
        // Resolve existing parent to catch junctions/symlinks without creating directories.
        const parent = await realpath(path.dirname(output));
        const target = path.join(parent, path.basename(output));
        const source = await realpath(packageRoot);
        if (!within(workspace, target) || target === workspace) throw new TypeError('outputDir must be a new child directory inside workspaceRoot');
        if (within(source, target) || within(target, source)) throw new TypeError('Research output cannot overlap the installed skill package');
        return { script: 'research_team.py', args: ['plan', '--scenario', scenario, '--output', target] };
      },
    }),
  ];
}

export function apply(ctx, options = {}) {
  const definitions = createTools(options);
  ctx.effect(() => {
    const disposers = [];
    try { for (const definition of definitions) disposers.push(ctx.tools.register(definition)); }
    catch (error) { for (const dispose of disposers.reverse()) dispose(); throw error; }
    return () => { for (const dispose of disposers.reverse()) dispose(); };
  });
}
