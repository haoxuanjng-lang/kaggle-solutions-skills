#!/usr/bin/env node
// Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
import { cpSync, existsSync, lstatSync, mkdirSync, readdirSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const name = 'kaggle-solutions-skills';
const version = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version;
const source = join(root, 'skills', name);
const args = process.argv.slice(2);
const help = `kaggle-solutions-skills ${version}

Usage: kaggle-solutions-skills install [--destination <skill-folder>] [--force]

Install the complete offline skill into $CODEX_HOME/skills/${name},
or ~/.codex/skills/${name} when CODEX_HOME is unset.
Node.js installs the files; Python 3.10+ runs the skill's research tools.
--force replaces files from this package in an existing skill folder.
--version prints the package version. --help shows this message.`;

function collect(folder, relative = '') {
  return readdirSync(folder, { withFileTypes: true }).flatMap(entry => {
    if (entry.name === '__pycache__' || entry.name.endsWith('.pyc')) return [];
    if (entry.isSymbolicLink()) throw new Error('Skill source contains a symbolic link');
    const path = join(relative, entry.name);
    return entry.isDirectory() ? collect(join(folder, entry.name), path) : [path];
  });
}

try {
  if (!args.length || (args.length === 1 && ['--help', '-h'].includes(args[0]))) {
    console.log(help);
  } else if (args.length === 1 && args[0] === '--version') {
    console.log(version);
  } else {
    if (args.shift() !== 'install') throw new Error('Unknown command. Use --help.');
    let destination = join(process.env.CODEX_HOME || join(homedir(), '.codex'), 'skills', name);
    let force = false;
    while (args.length) {
      const option = args.shift();
      if (option === '--force') force = true;
      else if (option === '--destination' && args[0] && !args[0].startsWith('--')) destination = args.shift();
      else throw new Error(`Invalid option: ${option}. Use --help.`);
    }
    destination = resolve(destination);
    // Reject links in the destination chain before writing any package files.
    for (let path = destination; ; path = dirname(path)) {
      if (existsSync(path) && lstatSync(path).isSymbolicLink()) throw new Error('Destination must not contain symbolic links');
      if (dirname(path) === path) break;
    }
    if (existsSync(destination) && !force) throw new Error('Destination exists. Use --force to update it, or choose --destination.');
    const files = collect(source);
    // Preflight nested targets, including broken links, before overwriting.
    for (const relative of files) {
      for (let path = join(destination, relative); path !== destination; path = dirname(path)) {
        try {
          if (lstatSync(path).isSymbolicLink()) throw new Error('Destination contains a symbolic link');
        } catch (error) { if (error.code !== 'ENOENT') throw error; }
      }
    }
    mkdirSync(destination, { recursive: true });
    for (const relative of files) {
      const target = join(destination, relative);
      mkdirSync(dirname(target), { recursive: true });
      cpSync(join(source, relative), target);
    }
    console.log(JSON.stringify({ ok: true, version, destination, files: files.length }, null, 2));
    console.log('Open a new Codex chat and invoke $kaggle-solutions-skills.');
  }
} catch (error) {
  console.error(`Install failed: ${error.message}`);
  process.exitCode = 1;
}
