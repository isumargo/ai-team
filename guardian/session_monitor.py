#!/usr/bin/env python3
"""Monitor session history length from agent.log.
If history exceeds threshold, print alert → cron delivers to Telegram.
Silent otherwise (empty stdout = no notification).
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("/root/.hermes/logs/agent.log")
THRESHOLD = 50          # warn when conversation reaches this many messages
COOLDOWN_FILE = Path("/root/ai-team/guardian/reports/session-alert-cooldown.json")
COOLDOWN_MINUTES = 60   # don't re-alert within this window


def get_current_history():
    """Parse agent.log for the latest session's history count."""
    if not LOG_FILE.exists():
        return None, None

    # Read last 200 lines — enough to find the most recent turn
    lines = []
    try:
        with open(LOG_FILE, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            chunk_size = 8192
            pos = size
            while pos > 0 and len(lines) < 200:
                read_size = min(chunk_size, pos)
                pos -= read_size
                f.seek(pos)
                chunk = f.read(read_size).decode("utf-8", errors="ignore")
                lines = chunk.split("\n") + lines
    except Exception:
        return None, None

    # Find latest turn_context line
    pattern = re.compile(
        r"agent\.turn_context:.*\bhistory=(\d+)\b.*\bsession=(\S+)\b"
    )
    for line in reversed(lines):
        m = pattern.search(line)
        if m:
            return int(m.group(1)), m.group(2)

    return None, None


def should_alert():
    """Check if we should send an alert."""
    history, session = get_current_history()
    if history is None:
        return None

    if history < THRESHOLD:
        return None

    # Check cooldown
    if COOLDOWN_FILE.exists():
        try:
            import json
            data = json.loads(COOLDOWN_FILE.read_text())
            last_alert = data.get("last_alert", "")
            last_session = data.get("session", "")
            if last_session == session:
                # Same session, check cooldown
                last_time = datetime.fromisoformat(last_alert)
            else:
                last_time = datetime.fromisoformat(last_alert)
        except Exception:
            last_time = None
    else:
        last_time = None

    now = datetime.now(timezone.utc)
    if last_time:
        delta = (now - last_time).total_seconds() / 60
        if delta < COOLDOWN_MINUTES:
            return None  # still in cooldown

    # Update cooldown
    COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    import json
    COOLDOWN_FILE.write_text(json.dumps({
        "last_alert": now.isoformat(),
        "session": session,
        "history": history,
    }))

    return history


def main():
    result = should_alert()

    if result is None:
        # Silent — no delivery
        return

    history = result
    print(
        f"⚠️ **Sesi kita udah {history} pesan!**\n\n"
        f"Biar hemat token, mending `/new` aja — aku bisa lanjut kok "
        f"tanpa history ini. Kecuali ada konteks penting yang belum selesai."
    )


if __name__ == "__main__":
    main()