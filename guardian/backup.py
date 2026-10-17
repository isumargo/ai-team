#!/usr/bin/env python3
"""Guardian: Backup AI team + Hermes config.

Rotates old backups when total exceeds limit.
Runs via cron (no_agent, zero tokens).
"""

import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

# --- Config ---
BACKUP_DIR = Path("/root/backups")
MAX_BACKUP_SIZE_MB = 200
FILES_TO_BACKUP = [
    "/root/ai-team/",
    "/root/.hermes/config.yaml",
    "/root/.hermes/USER.md",
    "/root/.hermes/skills/",
    "/root/.hermes/memories/",
    "/root/AGENTS.md",
]


def ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    print(f"[{ts()}] {msg}", file=sys.stderr)


def get_backup_name():
    now = datetime.now()
    return f"backup-{now.strftime('%Y-%m-%d-%H%M')}.tar.gz"


def get_total_size():
    total = 0
    if BACKUP_DIR.exists():
        for f in BACKUP_DIR.iterdir():
            if f.is_file() and f.suffix == ".gz":
                total += f.stat().st_size
    return total / (1024 * 1024)


def rotate_backups():
    while True:
        total = get_total_size()
        if total <= MAX_BACKUP_SIZE_MB:
            break
        backups = sorted(
            [f for f in BACKUP_DIR.iterdir() if f.suffix == ".gz"],
            key=lambda x: x.stat().st_mtime,
        )
        if not backups:
            break
        oldest = backups[0]
        log(f"Rotating: {oldest.name} ({total:.1f}MB > {MAX_BACKUP_SIZE_MB}MB)")
        oldest.unlink()


def create_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    name = get_backup_name()
    path = BACKUP_DIR / name

    if path.exists():
        log(f"Backup already exists: {name}")
        return

    sources = [s for s in FILES_TO_BACKUP if Path(s).exists()]
    if not sources:
        log("No source files found — aborting")
        sys.exit(1)

    log(f"Creating: {name} ({len(sources)} sources)")

    try:
        with tarfile.open(path, "w:gz") as tar:
            for src in sources:
                tar.add(src, arcname=src.lstrip("/"))
    except Exception as e:
        log(f"FAILED: {e}")
        if path.exists():
            path.unlink()
        sys.exit(1)

    size_mb = path.stat().st_size / (1024 * 1024)
    log(f"OK: {name} ({size_mb:.1f}MB)")
    rotate_backups()


def main():
    log("Starting backup...")
    create_backup()
    total = get_total_size()
    log(f"Done. Total: {total:.1f}MB / {MAX_BACKUP_SIZE_MB}MB")
    print(f"BACKUP=OK TOTAL_MB={total:.1f}")


if __name__ == "__main__":
    main()