#!/usr/bin/env python3
"""Guardian: OpenRouter cost sanitizer & auto-switch.

- Alerts every $1 increment ($1, $2, $3, $4) via alert file
- Auto-switch at $5
- Silent otherwise (stdout empty = no notification to chat)
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


def load_env(path="/root/.hermes/.env"):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, val = line.partition("=")
                    env[key.strip()] = val.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return env


# --- Config ---
_env = load_env()
API_KEY = _env.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))
CREDITS_URL = "https://openrouter.ai/api/v1/credits"

BACKUP_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
COST_LIMIT = 5.00

TEAM_DIR = Path("/root/ai-team")
REPORT_DIR = TEAM_DIR / "guardian" / "reports"
USAGE_LOG = REPORT_DIR / "usage-log.json"
ALERT_FILE = REPORT_DIR / "usage-alert.md"
STATE_FILE = REPORT_DIR / "alert-state.json"


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
    ALERT_FILE.write_text(f"""# OpenRouter Usage Alert

**Waktu:** {ts()}
**Status:** {status}

{details}
""")


def get_last_dollar():
    try:
        return json.loads(STATE_FILE.read_text()).get("last_dollar", -1)
    except (FileNotFoundError, json.JSONDecodeError):
        return -1


def save_last_dollar(d):
    STATE_FILE.write_text(json.dumps({"last_dollar": d}))


def switch_model(new_model):
    log(f"Switching model to: {new_model}")
    result = subprocess.run(
        ["hermes", "config", "set", "model.default", new_model],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        log(f"FAILED: {result.stderr}")
        return False
    log(f"Switched OK: {result.stdout.strip()}")
    return True


def fetch_credits():
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

    dollar_now = int(spent)
    last_dollar = get_last_dollar()

    log(f"Spent: ${spent:.4f} / ${total_credits:.2f} (${remaining:.4f} remaining)")

    # Auto-switch at $5
    if spent >= COST_LIMIT:
        write_alert("SWITCHED",
            f"Biaya melewati ${COST_LIMIT}.\n"
            f"Akumulasi: ${spent:.2f}\n"
            f"Beralih ke: {BACKUP_MODEL}")
        log("AUTO-SWITCH!")
        if switch_model(BACKUP_MODEL):
            save_last_dollar(dollar_now)
        else:
            log("Switch FAILED")
            sys.exit(1)
        print(f"⚠️ Biaya ${spent:.2f} — beralih ke {BACKUP_MODEL}")

    # Alert every $1
    elif dollar_now > last_dollar:
        write_alert("ALERT",
            f"Biaya mencapai ${dollar_now}.00\n"
            f"Akumulasi: ${spent:.2f} dari ${total_credits:.2f}")
        log(f"ALERT: ${dollar_now}.00")
        save_last_dollar(dollar_now)
        print(f"💰 Biaya OpenRouter: ${dollar_now}.00 / ${COST_LIMIT}.00")

    else:
        log(f"Aman: ${spent:.2f} — di bawah limit")

    # Clean state below $1
    if spent < 1.0:
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        if STATE_FILE.exists():
            STATE_FILE.unlink()


if __name__ == "__main__":
    main()
