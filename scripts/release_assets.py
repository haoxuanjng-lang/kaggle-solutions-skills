# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Attach release downloads without ever replacing an existing asset."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def run(command):
    return subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout


def publish_assets(repository, tag, directory, *, check_only=False, runner=run):
    directory = Path(directory)
    files = sorted([*directory.glob("*.zip"), *directory.glob("*.tgz")])
    checksums = directory / "SHA256SUMS.txt"
    if not files or not checksums.is_file():
        raise ValueError("Release packages and SHA256SUMS.txt are required")
    files.append(checksums)
    release = json.loads(runner([
        "gh", "release", "view", tag, "--repo", repository, "--json", "assets",
    ]))
    remote = {}
    for asset in release["assets"]:
        if asset["name"] in remote:
            raise ValueError("Duplicate release asset: " + asset["name"])
        remote[asset["name"]] = asset
    missing = []
    # Validate every existing file before the first mutation, including checksums.
    for path in files:
        asset = remote.get(path.name)
        if asset is None:
            missing.append(path)
            continue
        if asset.get("state") != "uploaded":
            raise ValueError("Release asset is not fully uploaded: " + path.name)
        prefix = f"https://api.github.com/repos/{repository}/releases/assets/"
        asset_id = asset.get("apiUrl", "").removeprefix(prefix)
        if not asset_id.isdigit():
            raise ValueError("Unexpected release asset API URL: " + path.name)
        content = runner([
            "gh", "api", f"repos/{repository}/releases/assets/{asset_id}",
            "-H", "Accept: application/octet-stream",
        ])
        if hashlib.sha256(content).digest() != hashlib.sha256(path.read_bytes()).digest():
            raise ValueError("Immutable release asset differs: " + path.name
                             + ". Recover original artifacts or publish a new version.")
    if not check_only and missing:
        # No --clobber: a concurrent upload must fail rather than overwrite.
        runner(["gh", "release", "upload", tag, "--repo", repository,
                *[str(path.resolve()) for path in missing]])
    return {"verified": len(files) - len(missing), "missing": len(missing),
            "uploaded": 0 if check_only else len(missing)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(publish_assets(args.repo, args.tag, args.directory,
                                      check_only=args.check_only)))
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Release asset verification failed: {error}\n")


if __name__ == "__main__":
    main()
