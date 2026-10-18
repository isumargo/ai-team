#!/usr/bin/env python3
"""
Session Monitor v2 — baca state.db langsung.
Alert kalo session mendekati compression threshold, ada compression failure,
atau cost per-session mulai tinggi. Silent stdout = no alert.
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/root/.hermes/state.db")
COOLDOWN_FILE = Path("/root/ai-team/guardian/reports/session-alert-cooldown.json")
COOLDOWN_MINUTES = 30  # jangan spam alert

# Threshold (DeepSeek V4 Pro context = 1,048,576)
CONTEXT_LIMIT = 1_048_576
YELLOW_PCT = 0.50   # 524K — warning
RED_PCT = 0.80       # 838K — critical

# Cost threshold per session
COST_WARN = 1.00     # $1 — notice
COST_CRITICAL = 3.00  # $3 — alert


def get_active_sessions():
    """Ambil session yang belum ended, sorted by input_tokens DESC."""
    if not DB.exists():
        return []
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    rows = db.execute(
        """SELECT id, title, source, model,
                  input_tokens, output_tokens, cache_read_tokens,
                  estimated_cost_usd,
                  compression_fallback_streak,
                  compression_overload_streak,
                  compression_ineffective_count
           FROM sessions
           WHERE ended_at IS NULL
           ORDER BY input_tokens DESC"""
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def check_cooldown(session_id: str) -> bool:
    """True = masih cooldown, jangan alert."""
    if not COOLDOWN_FILE.exists():
        return False
    try:
        data = json.loads(COOLDOWN_FILE.read_text())
        last = datetime.fromisoformat(data["last_alert"])
        same_session = data.get("session") == session_id
        now = datetime.now(timezone.utc)
        delta = (now - last).total_seconds() / 60
        return same_session and delta < COOLDOWN_MINUTES
    except Exception:
        return False


def set_cooldown(session_id: str):
    COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOLDOWN_FILE.write_text(json.dumps({
        "last_alert": datetime.now(timezone.utc).isoformat(),
        "session": session_id,
    }))


def format_alert(sessions: list) -> str | None:
    """Generate alert text. Return None if nothing to report."""
    alerts = []
    total_cost = sum(s["estimated_cost_usd"] or 0 for s in sessions)

    for s in sessions:
        tokens = s["input_tokens"] or 0
        sid = s["id"][:16]
        title = s.get("title") or "untitled"

        # Token level
        if tokens >= RED_PCT * CONTEXT_LIMIT:
            alerts.append(
                f"🔴 **KRITIS — {title}**\n"
                f"   Token: {tokens:,} / {CONTEXT_LIMIT:,} ({tokens/CONTEXT_LIMIT*100:.0f}%)\n"
                f"   Segera `/new` sebelum compression failure!"
            )
        elif tokens >= YELLOW_PCT * CONTEXT_LIMIT:
            alerts.append(
                f"🟡 **WARNING — {title}**\n"
                f"   Token: {tokens:,} / {CONTEXT_LIMIT:,} ({tokens/CONTEXT_LIMIT*100:.0f}%)\n"
                f"   Pertimbangkan `/new` atau `/compress`."
            )

        # Compression health
        if s["compression_fallback_streak"] > 0:
            alerts.append(
                f"⚠️ **Compression failure streak: {s['compression_fallback_streak']}**\n"
                f"   Session: {title} ({sid}...)\n"
                f"   Compression udah gagal {s['compression_fallback_streak']}x berturut-turut.\n"
                f"   `/new` sekarang — lanjut di session fresh."
            )
        if s["compression_overload_streak"] > 0:
            alerts.append(
                f"🔥 **Compression OVERLOAD: {s['compression_overload_streak']}**\n"
                f"   Session: {title} — HARUS `/new` sekarang!"
            )

        # Cost per session
        cost = s["estimated_cost_usd"] or 0
        if cost >= COST_CRITICAL:
            alerts.append(
                f"💰 **Cost kritis: ${cost:.2f}** — session `{title}`\n"
                f"   Pertimbangkan `/new` buat reset konteks & hemat token."
            )

    if total_cost >= COST_WARN and not alerts:
        alerts.append(
            f"📊 Total cost sesi aktif: **${total_cost:.2f}** — masih aman."
        )

    if not alerts:
        return None

    header = "📡 **Session Monitor Report**\n"
    return header + "\n\n".join(alerts)


def main():
    sessions = get_active_sessions()
    if not sessions:
        return  # no active session

    # Find the session with highest tokens for cooldown check
    main_session = sessions[0]
    if check_cooldown(main_session["id"]):
        return  # cooldown

    alert = format_alert(sessions)
    if alert is None:
        return

    set_cooldown(main_session["id"])
    print(alert)


if __name__ == "__main__":
    main()