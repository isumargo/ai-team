#!/usr/bin/env python3
"""Guardian: OpenRouter cost sanitizer & auto-switch.

Checks OpenRouter credit usage periodically. If accumulated cost
crosses thresholds:
  - $4.00 → alert EVE (warning)
  - $5.00 → auto-switch model to backup (free/cheap)

Usage: python3 /root/ai-team/guardian/check_usage.py
Env:   OPENROUTER_API_KEY
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

# --- Config ---
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
CREDITS_URL = "https://openrouter.ai/api/v1/credits"

# Model thresholds
BACKUP_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
COST_LIMIT = 5.00        # $ — auto-switch
WARNING_LIMIT = 4.00     # $ — alert only

# Paths
TEAM_DIR = Path("/root/ai-team")
REPORT_DIR = TEAM_DIR / "guardian" / "reports"
USAGE_LOG = REPORT_DIR / "usage-log.json"
ALERT_FILE = REPORT_DIR / "usage-alert.md"

# --- Helpers ---

def ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(msg):
    print(f"[{ts()}] {msg}", file=sys.stderr)

def save_log(data):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    history = []
    if USAGE_LOG.exists():
        try:
            history = json.loads(USAGE_LOG.read_text())
        except json.JSONDecodeError:
            pass
    history.append(data)
    USAGE_LOG.write_text(json.dumps(history[-100:], indent=2))

def write_alert(status, details):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    alert = f"""# OpenRouter Usage Alert

**Waktu:** {ts()}
**Status:** {status}

{details}
"""
    ALERT_FILE.write_text(alert)

def switch_model(new_model):
    """Switch Hermes model via config command."""
    log(f"Switching model to: {new_model}")
    result = subprocess.run(
        ["hermes", "config", "set", "model.default", new_model],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        log(f"FAILED to switch model: {result.stderr}")
        return False
    log(f"Model switched OK: {result.stdout.strip()}")
    return True

def fetch_credits():
    """Call OpenRouter credits API."""
    if not API_KEY:
        log("OPENROUTER_API_KEY not set")
        return None
    req = Request(
        CREDITS_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        log(f"API call failed: {e}")
        return None

# --- Main ---

def main():
    log("Checking OpenRouter credits...")

    credits = fetch_credits()
    if credits is None:
        sys.exit(1)

    data = credits.get("data", credits)
    total_credits = data.get("total_credits", 0)
    total_usage = data.get("total_usage", 0)
    remaining = total_credits - total_usage
    spent = total_usage

    entry = {
        "time": ts(),
        "total_credits": total_credits,
        "total_usage": total_usage,
        "spent": spent,
        "remaining": remaining,
    }
    save_log(entry)

    log(f"Spent: ${spent:.4f} / ${total_credits:.2f} (${remaining:.4f} remaining)")

    if spent >= COST_LIMIT:
        write_alert("SWITCHED",
            f"Biaya melampaui ${COST_LIMIT}.\n"
            f"Akumulasi: ${spent:.2f}\n"
            f"Beralih ke: {BACKUP_MODEL}")
        if switch_model(BACKUP_MODEL):
            log("Model switched successfully")
        else:
            log("Model switch FAILED — manual intervention needed")
            sys.exit(1)

    elif spent >= WARNING_LIMIT:
        write_alert("WARNING",
            f"Biaya mendekati batas ${COST_LIMIT}.\n"
            f"Akumulasi: ${spent:.2f}\n"
            f"Siapkan model cadangan: {BACKUP_MODEL}")
        log(f"WARNING: ${spent:.2f} — mendekati limit ${COST_LIMIT}")

    else:
        log(f"Aman: ${spent:.2f} — di bawah limit")
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()

    print(f"SPENT={spent:.4f}")
    print(f"LIMIT={COST_LIMIT:.2f}")
    status = "SWITCHED" if spent >= COST_LIMIT else ("WARNING" if spent >= WARNING_LIMIT else "OK")
    print(f"STATUS={status}")

if __name__ == "__main__":
    main()