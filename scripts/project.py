# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Check and install the complete portable skill without research caches."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kaggle-solutions-skills"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check():
    import yaml
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---", 2)
    metadata = yaml.safe_load(parts[1]) if len(parts) == 3 else {}
    if metadata.get("name") != SKILL.name or not metadata.get("description"):
        errors.append("Skill frontmatter missing correct name/description")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject_version = re.search(r'^version\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.MULTILINE)
    if metadata.get("metadata", {}).get("version") != version or not pyproject_version or pyproject_version.group(1) != version:
        errors.append("VERSION, pyproject.toml and skill metadata version must agree")
    ui = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    if not 25 <= len(ui["interface"]["short_description"]) <= 64:
        errors.append("UI short_description must be 25-64 characters")
    if "$" + SKILL.name not in ui["interface"]["default_prompt"]:
        errors.append("UI default_prompt must mention the skill")
    if not ui.get("policy", {}).get("allow_implicit_invocation", True):
        errors.append("Implicit discovery was unexpectedly disabled")
    for path in ROOT.rglob("*.md"):
        if any(part in ("sources", "cache", ".git", ".venv", "workspaces") for part in path.relative_to(ROOT).parts):
            continue
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith("#"):
                continue
            target = link.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(f"Broken local link: {path.relative_to(ROOT)} -> {link}")
    knowledge = load_module("solutions", SKILL / "scripts" / "solutions.py").validate()
    errors.extend(knowledge["errors"])
    # Distribution checks target actual filenames/content, not all possible secrets.
    for path in skill_files():
        if path.name in ("kaggle.json", "access_token", "credentials.json") or path.name.startswith(".env"):
            errors.append(f"Credential file included: {path.name}")
        text = path.read_text(encoding="utf-8")
        if re.search(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|KGAT_[A-Za-z0-9]{20,}", text):
            errors.append(f"Credential-shaped token in {path.relative_to(SKILL)}")
    return {"ok": not errors, "errors": errors, "knowledge": knowledge,
            "skill_files": len(skill_files()), "skill_bytes": sum(path.stat().st_size for path in skill_files())}


def skill_files():
    return sorted(path for path in SKILL.rglob("*") if path.is_file()
                  and "__pycache__" not in path.parts and path.suffix != ".pyc")


def default_destination():
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return codex_root / "skills" / SKILL.name


def install(destination):
    import yaml
    result = check()
    if not result["ok"]:
        raise ValueError(json.dumps(result["errors"]))
    destination = destination.resolve()
    if destination == SKILL.resolve() or SKILL.resolve() in destination.parents:
        raise ValueError("Install destination must be separate from source skill")
    if destination.exists():
        entry = destination / "SKILL.md"
        if not entry.is_file() or yaml.safe_load(entry.read_text(encoding="utf-8").split("---", 2)[1]).get("name") != SKILL.name:
            raise ValueError("Destination is not this skill; choose a separate skill directory")
    files = skill_files()
    destination.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for source in files:
        relative = source.relative_to(SKILL)
        target = destination / relative
        if not target.resolve().is_relative_to(destination):
            raise ValueError("Install target escapes destination")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
        if hashes[relative.as_posix()] != hashlib.sha256(source.read_bytes()).hexdigest():
            raise ValueError(f"Installed byte mismatch: {relative}")
    manifest = {"skill": SKILL.name, "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
                "files": hashes, "source": str(SKILL.resolve())}
    (destination / ".install-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "destination": str(destination), "files": len(files), "bytes": result["skill_bytes"], "byte_verified": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    install_parser = sub.add_parser("install")
    install_parser.add_argument("--destination", type=Path, default=default_destination())
    args = parser.parse_args()
    try:
        result = check() if args.command == "check" else install(args.destination)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result["ok"] else 1
    except (OSError, ValueError, KeyError, IndexError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
