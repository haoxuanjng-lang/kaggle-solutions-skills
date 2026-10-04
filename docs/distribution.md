# Distribution and releases

The source repository and npm package are public. The npm package is hosted on
GitHub Packages, not npmjs.org:

- Package: `@haoxuanjng-lang/kaggle-solutions-skills`
- Registry: `https://npm.pkg.github.com`
- [Package page](https://github.com/users/haoxuanjng-lang/packages/npm/package/kaggle-solutions-skills)
- [Public downloads](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases)

## Install without registry credentials

Node.js 20+ installs the package; Python 3.10+ runs the research scripts.

```sh
npx --yes --package=https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.1.1/haoxuanjng-lang-kaggle-solutions-skills-0.1.1.tgz kaggle-solutions-skills install
```

Use `--destination <skill-folder>` for another location. An existing destination
is preserved unless `--force` is selected; updates replace the packaged files
and retain other files already present in the directory. Start a new Codex chat
to use the installed skill.

The default location is `$CODEX_HOME/skills/kaggle-solutions-skills`, or
`~/.codex/skills/kaggle-solutions-skills` when `CODEX_HOME` is unset.

The Release ZIP contains the same 18 portable skill files. Extract it into the
skills directory so `kaggle-solutions-skills/SKILL.md` is directly inside it.
Check downloads against the release's `SHA256SUMS.txt` when needed.

## GitHub npm registry

Even public npm packages in GitHub Packages require registry authentication.
Follow the [official authentication instructions](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry).
After login:

```sh
npx --yes --registry=https://npm.pkg.github.com @haoxuanjng-lang/kaggle-solutions-skills@0.1.1 install
```

The public Release command above avoids this registry requirement.

## Publish a new version

1. Update `VERSION`, `package.json`, `pyproject.toml`, Skill frontmatter version,
   `CHANGELOG.md` and versioned README/download examples together.
2. Run `python scripts/project.py check`, the Python tests and `npm test`.
3. Push the reviewed commit, then publish a GitHub Release whose tag is
   `v<package-version>` and whose target is that commit.
4. The [publish workflow](../.github/workflows/publish-package.yml) validates the
   release version, builds both packages, installs and queries the actual npm
   tarball, publishes to GitHub Packages using `GITHUB_TOKEN`, then attaches
   `.tgz`, ZIP and checksums to the Release.
5. Confirm the workflow succeeded, the package visibility is public and the
   anonymous Release installation works. Record the observed results.

The workflow also supports manual dispatch to recover a release attempt. It
skips an already-published npm version and replaces Release assets with the
rebuilt files. Dispatch from the matching release revision when rebuilding
package content; use a new version for changes to the distributed files.

The npm package uses an explicit file allowlist, includes licenses and offline
knowledge, and has no runtime dependencies or install lifecycle scripts. It
excludes tests, source caches, credentials and private competition artifacts.

GitHub Packages and the Release are different distribution paths. A successful
Git commit or Release creation alone does not establish successful npm
publication; check the package and uploaded assets directly.
