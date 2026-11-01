#!/usr/bin/env python3
"""Generate runtime AGENTS.md copies from the canonical policy sources.

Canonical sources (single source of truth, inside the PC-synced workspace):
  /root/ai-team/workspace/01-organisasi/policy/TEAM-POLICY.md
  /root/ai-team/workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md

Generated runtime copies:
  /root/AGENTS.md
  /root/.hermes/AGENTS.md
  /root/ai-team/workspace/01-organisasi/AGENTS.md
  /root/.hermes/profiles/developer/AGENTS.md   (team policy + developer instructions)

Usage:
  python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --check
  python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --sync

--check never writes. --sync backs up existing targets privately and writes copies atomically.
Do not edit generated runtime copies by hand.

Why the Developer copy is a merge:
Hermes loads exactly ONE project-context file per directory (first non-empty of
AGENTS.override.md / AGENTS.md / agents.md). The Developer profile directory only
contains its own AGENTS.md, so the team policy was NOT reaching that profile even
though the instructions claimed it was "loaded separately". The Developer copy is
therefore generated as team policy + developer instructions so both are present.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/root/ai-team/workspace/01-organisasi/policy")
TEAM_SOURCE = BASE / "TEAM-POLICY.md"
DEV_SOURCE = BASE / "DEVELOPER-INSTRUCTIONS.md"
BACKUP_DIR = Path("/root/.hermes/backups/policy-sync")

TEAM_TARGETS = [
    Path("/root/AGENTS.md"),
    Path("/root/.hermes/AGENTS.md"),
    Path("/root/ai-team/workspace/01-organisasi/AGENTS.md"),
]
DEV_TARGET = Path("/root/.hermes/profiles/developer/AGENTS.md")

DEV_MERGE_HEADER = """<!-- GENERATED FILE - do not edit by hand.
Source: workspace/01-organisasi/policy/TEAM-POLICY.md + DEVELOPER-INSTRUCTIONS.md
Regenerate: python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --sync
-->

"""


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(131072), b""):
            h.update(chunk)
    return h.hexdigest()


def backup_target(target: Path) -> Path | None:
    if not target.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{target.name}.{target.parent.name or 'root'}.{stamp}.bak"
    backup = BACKUP_DIR / name
    shutil.copy2(target, backup)
    os.chmod(backup, 0o600)
    print(f"Backup: {backup}")
    return backup


def atomic_write(target: Path, data: bytes, private: bool) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as dst:
            dst.write(data)
            dst.flush()
            os.fsync(dst.fileno())
        os.chmod(tmp_name, 0o600 if private else 0o644)
        os.replace(tmp_name, target)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def atomic_copy(source: Path, target: Path) -> None:
    atomic_write(target, source.read_bytes(), private=str(target).startswith("/root/.hermes"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="compare all generated copies; never write")
    group.add_argument("--sync", action="store_true", help="backup then atomically generate all copies")
    args = parser.parse_args()

    for source in (TEAM_SOURCE, DEV_SOURCE):
        if not source.is_file():
            print(f"ERROR: canonical file missing: {source}", file=sys.stderr)
            return 2

    team_bytes = TEAM_SOURCE.read_bytes()
    dev_merge = DEV_MERGE_HEADER.encode() + team_bytes + b"\n\n---\n\n" + DEV_SOURCE.read_bytes()
    dev_merge_hash = hashlib.sha256(dev_merge).hexdigest()

    def report(target: Path, expected: bytes) -> int:
        if args.check:
            if not target.is_file():
                print(f"DRIFT: generated target missing: {target}")
                return 1
            actual = target.read_bytes()
            if actual != expected:
                print(f"DRIFT: {target} differs from expected content "
                      f"({hashlib.sha256(actual).hexdigest()[:12]} != "
                      f"{hashlib.sha256(expected).hexdigest()[:12]})")
                return 1
            print(f"OK: {target} matches generated content "
                  f"({hashlib.sha256(actual).hexdigest()[:12]})")
            return 0
        backup_target(target)
        atomic_write(target, expected, private=str(target).startswith("/root/.hermes"))
        print(f"SYNCED: {target} ({hashlib.sha256(expected).hexdigest()[:12]})")
        return 0

    status = 0
    for target in TEAM_TARGETS:
        status |= report(target, team_bytes)
    status |= report(DEV_TARGET, dev_merge)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
