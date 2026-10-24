# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Require registry and Release npm tarballs to have identical bytes."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def verify(package, tarball, *, runner=subprocess.run):
    content = Path(tarball).read_bytes()
    result = runner([
        shutil.which("npm") or "npm", "view", package, "dist.integrity", "--json",
        "--registry=https://npm.pkg.github.com",
    ], check=True, capture_output=True)
    integrity = json.loads(result.stdout)
    expected = "sha512-" + base64.b64encode(hashlib.sha512(content).digest()).decode("ascii")
    if integrity != expected:
        raise ValueError("Published npm integrity is missing, unsupported or differs. "
                         "Recover the original tarball or publish a new version.")
    return {"verified": True, "integrity": expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True)
    parser.add_argument("--tarball", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.package, args.tarball)))
    except (OSError, ValueError, subprocess.CalledProcessError):
        # Do not echo registry subprocess output, which may contain auth details.
        parser.exit(1, "Registry artifact verification failed; no Release upload allowed. "
                    "Check registry access and recover the original tarball, or use a new version.\n")


if __name__ == "__main__":
    main()
