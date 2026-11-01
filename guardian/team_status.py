#!/usr/bin/env python3
"""
team_status.py — writer tunggal status tim live.

Sumber kebenaran (runtime):
  - ~/.hermes/state.db                 -> sessions, gateway_heartbeats (default/EVE)
  - ~/.hermes/profiles/<agen>/state.db -> sessions per agen
  - ~/.hermes/cron/executions.db       -> health job cron
  - ~/.hermes/cron/jobs.json           -> definisi job cron (jadwal, next run)
  - workspace/05-status/guardian.json   -> status biaya Guardian (writer lain)
  - /proc, free, df                    -> kesehatan VPS

Output (canonical, satu file):
  workspace/05-status/team.json

Aturan:
  - SATU writer. Tidak ada agen lain yang menulis file ini.
  - Script Python biasa, tanpa LLM -> nol token / nol kuota.
  - Tidak menulis nama model, tier, atau asumsi runtime ke dalam file.
  - Tidak pernah menulis secret/credential.

Dijalankan tiap 10 menit oleh cron Hermes (no_agent).
"""
import json
import os
import sqlite3
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TEAM_DIR = Path("/root/ai-team")
WORKSPACE = TEAM_DIR / "workspace"
STATUS_DIR = WORKSPACE / "05-status"
OUT_FILE = STATUS_DIR / "team.json"

HERMES = Path("/root/.hermes")
PROFILES_DIR = HERMES / "profiles"
CRON_DIR = HERMES / "cron"

# Profil = agen. "default" adalah EVE (Chief of Staff).
AGENTS = {
    "default": {
        "id": "default",
        "nama": "EVE",
        "peran": "Chief of Staff",
        "runtime_profile": "default",
    },
    "analyst": {
        "id": "analyst",
        "nama": "Analyst",
        "peran": "Riset pasar, margin, pricing, forecasting",
        "runtime_profile": "analyst",
    },
    "auditor": {
        "id": "auditor",
        "nama": "Auditor",
        "peran": "QA & review hasil kerja agen (Layer 1)",
        "runtime_profile": "auditor",
    },
    "designer": {
        "id": "designer",
        "nama": "Designer",
        "peran": "UI/UX, branding, visual",
        "runtime_profile": "designer",
    },
    "developer": {
        "id": "developer",
        "nama": "Developer",
        "peran": "Tracking system, app, automasi",
        "runtime_profile": "developer",
    },
    "guardian": {
        "id": "guardian",
        "nama": "Guardian",
        "peran": "SysAdmin VPS, monitoring resource, self-healing, sanitasi biaya",
        "runtime_profile": "guardian",
    },
    "marketer": {
        "id": "marketer",
        "nama": "Marketer",
        "peran": "Copywriting, sosmed, SEO, konten",
        "runtime_profile": "marketer",
    },
    "pm-distribusi": {
        "id": "pm-distribusi",
        "nama": "PM Distribusi",
        "peran": "Manajer proyek Distribusi Madju PRO & Sukses Alami",
        "runtime_profile": "pm-distribusi",
    },
    "sales": {
        "id": "sales",
        "nama": "Sales",
        "peran": "Pitch deck, proposal, follow-up",
        "runtime_profile": "sales",
    },
    "strategist": {
        "id": "strategist",
        "nama": "Strategist",
        "peran": "Roadmap, scaling, monetisasi",
        "runtime_profile": "strategist",
    },
}

# Ambang status (menit). Ini tampilan/penanda, bukan logic bisnis Guardian.
AKTIF_MENIT = 30      # ada aktivitas < 30 menit lalu -> "aktif"
TERLAMBAT_MENIT = 1440  # > 24 jam tanpa aktivitas -> "terlambat"
OFFLINE_MENIT = 4320   # > 3 hari tanpa aktivitas -> "tidak aktif"


def iso(ts):
    """Epoch float -> ISO8601 UTC, atau None."""
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(float(ts), timezone.utc).isoformat().replace("+00:00", "Z")
    except (TypeError, ValueError, OSError):
        return None


def now():
    return datetime.now(timezone.utc)


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return default


def ro_db(path):
    """Buka sqlite read-only; None kalau tidak ada / rusak."""
    if not Path(path).exists():
        return None
    try:
        return sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    except sqlite3.Error:
        return None


def q(conn, sql, args=()):
    try:
        return conn.execute(sql, args).fetchall()
    except sqlite3.Error:
        return []


def profile_db_path(profile):
    if profile == "default":
        return HERMES / "state.db"
    return PROFILES_DIR / profile / "state.db"


def agent_status(spec, now_dt):
    """Ringkasan satu agen dari state.db profile-nya."""
    out = dict(spec)
    out.update(
        {
            "state": "unknown",
            "last_activity": None,
            "minutes_since_activity": None,
            "sessions_total": 0,
            "sessions_open": 0,
            "messages_total": 0,
            "tokens_in": 0,
            "tokens_out": 0,
            "estimated_cost_usd": 0.0,
            "db": None,
            "error": None,
        }
    )

    db = profile_db_path(spec["runtime_profile"])
    out["db"] = str(db)
    conn = ro_db(db)
    if conn is None:
        out["state"] = "no_db"
        out["error"] = "state.db tidak terbaca"
        return out

    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        total = q(conn, "SELECT COUNT(*) FROM sessions")[0][0]
        out["sessions_total"] = total

        if "ended_at" in cols:
            open_n = q(conn, "SELECT COUNT(*) FROM sessions WHERE ended_at IS NULL")[0][0]
        else:
            open_n = 0
        out["sessions_open"] = open_n

        if "message_count" in cols:
            out["messages_total"] = q(
                conn, "SELECT COALESCE(SUM(message_count),0) FROM sessions")[0][0]
        if "input_tokens" in cols:
            row = q(
                conn,
                "SELECT COALESCE(SUM(input_tokens),0), COALESCE(SUM(output_tokens),0) "
                "FROM sessions",
            )[0]
            out["tokens_in"], out["tokens_out"] = row[0], row[1]
        if "estimated_cost_usd" in cols:
            out["estimated_cost_usd"] = round(
                float(q(conn, "SELECT COALESCE(SUM(estimated_cost_usd),0) FROM sessions")[0][0]), 4)

        last = None
        for col in ("last_activity_at", "started_at"):
            if col in cols:
                v = q(conn, f"SELECT MAX({col}) FROM sessions")[0][0]
                if v:
                    last = float(v) if last is None else max(last, float(v))
        out["last_activity"] = iso(last)
        if last:
            delta = (now_dt.timestamp() - last) / 60.0
            out["minutes_since_activity"] = round(delta, 1)
            if delta <= AKTIF_MENIT:
                out["state"] = "aktif"
            elif delta <= TERLAMBAT_MENIT:
                out["state"] = "idle"
            elif delta <= OFFLINE_MENIT:
                out["state"] = "terlambat"
            else:
                out["state"] = "tidak_aktif"
        else:
            out["state"] = "tidak_aktif"
    finally:
        conn.close()

    return out


def job_status(now_dt):
    """Health job cron Hermes dari executions.db + jobs.json."""
    jobs_meta = {}
    raw_jobs = read_json(CRON_DIR / "jobs.json", {}) or {}
    for j in raw_jobs.get("jobs", []) if isinstance(raw_jobs, dict) else []:
        jobs_meta[j.get("id")] = {
            "id": j.get("id"),
            "name": j.get("name"),
            "schedule": (j.get("schedule") or {}).get("display"),
            "enabled": j.get("enabled"),
            "last_status": j.get("last_status"),
            "last_run_at": j.get("last_run_at"),
            "next_run_at": j.get("next_run_at"),
            "failure_streak": j.get("failure_streak"),
            "script": j.get("script"),
            "no_agent": j.get("no_agent"),
        }

    per_job = {}
    conn = ro_db(CRON_DIR / "executions.db")
    if conn:
        try:
            for r in q(
                conn,
                "SELECT job_id, status, started_at, finished_at, error "
                "FROM executions ORDER BY started_at DESC",
            ):
                jid = r[0]
                if jid in per_job:
                    continue
                per_job[jid] = {
                    "last_status": r[1],
                    "last_run_at": r[2],
                    "last_error": r[4],
                }
        finally:
            conn.close()

    out = []
    for jid, meta in jobs_meta.items():
        ex = per_job.get(jid, {})
        last_run = meta.get("last_run_at") or ex.get("last_status")
        status = ex.get("last_status") or meta.get("last_status") or "unknown"
        item = dict(meta)
        item["last_execution_status"] = ex.get("last_status")
        item["last_error"] = ex.get("last_error")
        item["health"] = "ok" if status in ("completed", "ok", "success") else "gagal"
        out.append(item)

    # Job yang punya eksekusi tapi tidak terdaftar di jobs.json
    for jid, ex in per_job.items():
        if jid not in jobs_meta:
            out.append(
                {
                    "id": jid,
                    "name": jid,
                    "schedule": None,
                    "enabled": None,
                    "health": "ok" if ex.get("last_status") == "completed" else "gagal",
                    "last_execution_status": ex.get("last_status"),
                    "last_run_at": ex.get("last_run_at"),
                    "last_error": ex.get("last_error"),
                    "script": None,
                    "no_agent": None,
                }
            )

    out.sort(key=lambda x: (x.get("name") or ""))
    return out


def system_status():
    """Kesehatan VPS ringkas."""
    out = {}
    try:
        with open("/proc/uptime") as f:
            out["uptime_seconds"] = int(float(f.read().split()[0]))
    except (OSError, ValueError):
        out["uptime_seconds"] = None

    try:
        res = subprocess.run(
            ["free", "-b"], capture_output=True, text=True, timeout=10
        )
        for line in res.stdout.splitlines():
            if line.startswith("Mem:"):
                parts = line.split()
                out["mem_total"] = int(parts[1])
                out["mem_used"] = int(parts[2])
                out["mem_available"] = int(parts[6]) if len(parts) > 6 else None
                break
    except (OSError, subprocess.SubprocessError, ValueError):
        pass

    try:
        res = subprocess.run(
            ["df", "-B1", "/"], capture_output=True, text=True, timeout=10
        )
        lines = res.stdout.splitlines()
        if len(lines) > 1:
            parts = lines[1].split()
            out["disk_total"] = int(parts[1])
            out["disk_used"] = int(parts[2])
            out["disk_use_percent"] = parts[4].rstrip("%")
    except (OSError, subprocess.SubprocessError, ValueError):
        pass

    try:
        out["load_average"] = [
            round(float(x), 2) for x in os.getloadavg()
        ]
    except OSError:
        pass

    return out


def gateway_status():
    """Heartbeat gateway Hermes per profile."""
    conn = ro_db(HERMES / "state.db")
    out = []
    if not conn:
        return out
    try:
        rows = q(
            conn,
            "SELECT profile, pid, started_at, last_heartbeat FROM gateway_heartbeats "
            "ORDER BY last_heartbeat DESC",
        )
        seen = set()
        for profile, pid, started, hb in rows:
            if profile in seen:
                continue
            seen.add(profile)
            delta = None
            if hb:
                delta = round((time.time() - float(hb)) / 60.0, 1)
            out.append(
                {
                    "profile": profile,
                    "pid": pid,
                    "started_at": iso(started),
                    "last_heartbeat": iso(hb),
                    "minutes_since_heartbeat": delta,
                    "alive": bool(delta is not None and delta <= 5),
                }
            )
    finally:
        conn.close()
    return out


def cost_status():
    """Status biaya dari writer Guardian (check_usage.py)."""
    raw = read_json(STATUS_DIR / "guardian.json", {}) or {}
    return {
        "cost_current": raw.get("cost_current"),
        "cost_limit": raw.get("cost_limit"),
        "cost_remaining": raw.get("cost_remaining"),
        "last_activity": raw.get("last_activity"),
        "source": "guardian/check_usage.py",
        "threshold_conflict": (
            "config.json=$5 vs memories/MEMORY.md=$20 -- item review Guardian (belum diubah)"
        ),
    }


def build():
    now_dt = now()
    agents = [agent_status(spec, now_dt) for spec in AGENTS.values()]
    return {
        "schema_version": 1,
        "generated_at": now_dt.isoformat().replace("+00:00", "Z"),
        "generator": "guardian/team_status.py",
        "agents": agents,
        "jobs": job_status(now_dt),
        "gateway": gateway_status(),
        "cost": cost_status(),
        "system": system_status(),
    }


def main():
    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    data = build()
    tmp = OUT_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, OUT_FILE)
    print(
        f"team_status: wrote {OUT_FILE} "
        f"agents={len(data['agents'])} jobs={len(data['jobs'])}"
    )


if __name__ == "__main__":
    main()
