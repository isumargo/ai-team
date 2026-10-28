#!/usr/bin/env python3
"""Generate truth-map.excalidraw — Peta Sumber Kebenaran AI Team Ical.

Standar: skill creative/excalidraw (font >= 16, tanpa emoji, arrow binding,
z-order: zone -> shape -> bound text -> arrow).
Canonical data: /root/ai-team/docs/truth-map.md
"""
import json
import os
import random

random.seed(20261028)

OUT = "/root/ai-team/docs/truth-map.excalidraw"

BLUE = "#a5d8ff"     # primary / input
GREEN = "#b2f2bb"    # success / output
ORANGE = "#ffd8a8"   # warning / external
PURPLE = "#d0bfff"   # processing / special
RED = "#ffc9c9"      # error / critical
YELLOW = "#fff3bf"   # notes / decisions
TEAL = "#c3fae8"     # storage / data
GREY = "#e9ecef"     # neutral
INK = "#1e1e1e"
MUTED = "#757575"

els = []
_seq = [0]
BOXES = {}


def nid(p):
    _seq[0] += 1
    return f"{p}{_seq[0]:03d}"


def _common(t, idr, x, y, w, h, stroke, bg, dashed, sw):
    return {
        "type": t, "id": idr, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
        "strokeWidth": sw, "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "seed": random.randint(1, 2 ** 31), "version": 2,
        "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False,
        "boundElements": None, "updated": 1793189000000, "link": None, "locked": False,
    }


def box(x, y, w, h, text, bg=GREY, stroke=INK, fs=16, dashed=False, sw=1.5):
    """Rectangle + bound text (container binding)."""
    rid = nid("r")
    r = _common("rectangle", rid, x, y, w, h, stroke, bg, dashed, sw)
    els.append(r)
    BOXES[rid] = (x, y, w, h)
    if text:
        tid = nid("t")
        lines = text.count("\n") + 1
        r["boundElements"] = [{"id": tid, "type": "text"}]
        els.append({
            "type": "text", "id": tid, "x": x + 8, "y": y + 8, "width": w - 16,
            "height": fs * 1.25 * lines, "angle": 0, "strokeColor": INK,
            "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
            "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
            "frameId": None, "roundness": None, "seed": random.randint(1, 2 ** 31),
            "version": 2, "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False,
            "boundElements": None, "updated": 1793189000000, "link": None, "locked": False,
            "text": text, "fontSize": fs, "fontFamily": 1, "textAlign": "center",
            "verticalAlign": "middle", "containerId": rid, "originalText": text,
            "autoResize": True, "lineHeight": 1.25,
        })
    return rid


def zone(x, y, w, h, title, stroke=MUTED):
    """Dashed background zone + standalone title label."""
    zid = nid("z")
    z = _common("rectangle", zid, x, y, w, h, stroke, "transparent", True, 1)
    els.append(z)
    tid = nid("zt")
    els.append({
        "type": "text", "id": tid, "x": x + 12, "y": y + 8, "width": w - 24,
        "height": 24, "angle": 0, "strokeColor": MUTED, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
        "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
        "seed": random.randint(1, 2 ** 31), "version": 2,
        "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False,
        "boundElements": None, "updated": 1793189000000, "link": None, "locked": False,
        "text": title, "fontSize": 20, "fontFamily": 1, "textAlign": "left",
        "verticalAlign": "top", "containerId": None, "originalText": title,
        "autoResize": True, "lineHeight": 1.25,
    })
    return zid


def free_text(x, y, text, fs=18, color=INK):
    tid = nid("ft")
    lines = text.count("\n") + 1
    els.append({
        "type": "text", "id": tid, "x": x, "y": y, "width": 10,
        "height": fs * 1.25 * lines, "angle": 0, "strokeColor": color,
        "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
        "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": None, "roundness": None, "seed": random.randint(1, 2 ** 31),
        "version": 2, "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False,
        "boundElements": None, "updated": 1793189000000, "link": None, "locked": False,
        "text": text, "fontSize": fs, "fontFamily": 1, "textAlign": "left",
        "verticalAlign": "top", "containerId": None, "originalText": text,
        "autoResize": True, "lineHeight": 1.25,
    })
    return tid


FIXED = {"top": [0.5, 0], "bottom": [0.5, 1], "left": [0, 0.5], "right": [1, 0.5]}


def anchor(bid, side):
    x, y, w, h = BOXES[bid]
    if side == "top":
        return x + w / 2, y
    if side == "bottom":
        return x + w / 2, y + h
    if side == "left":
        return x, y + h / 2
    return x + w, y + h / 2


def arrow(src, s_side, dst, d_side, label=None, stroke=INK, dashed=False, sw=1.5):
    x1, y1 = anchor(src, s_side)
    x2, y2 = anchor(dst, d_side)
    aid = nid("a")
    bx, by = min(x1, x2), min(y1, y2)
    a = _common("arrow", aid, bx, by, abs(x2 - x1), abs(y2 - y1), stroke,
                "transparent", dashed, sw)
    a["roundness"] = None
    a["points"] = [[x1 - bx, y1 - by], [x2 - bx, y2 - by]]
    a["lastCommittedPoint"] = None
    a["startBinding"] = {"elementId": src, "fixedPoint": FIXED[s_side]}
    a["endBinding"] = {"elementId": dst, "fixedPoint": FIXED[d_side]}
    a["startArrowhead"] = None
    a["endArrowhead"] = "arrow"
    els.append(a)
    if label:
        tid = nid("at")
        a["boundElements"] = [{"id": tid, "type": "text"}]
        els.append({
            "type": "text", "id": tid, "x": (x1 + x2) / 2 - 60, "y": (y1 + y2) / 2 - 12,
            "width": 120, "height": 18, "angle": 0, "strokeColor": MUTED,
            "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
            "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
            "frameId": None, "roundness": None, "seed": random.randint(1, 2 ** 31),
            "version": 2, "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False,
            "boundElements": None, "updated": 1793189000000, "link": None, "locked": False,
            "text": label, "fontSize": 16, "fontFamily": 1, "textAlign": "center",
            "verticalAlign": "middle", "containerId": aid, "originalText": label,
            "autoResize": True, "lineHeight": 1.25,
        })
    return aid


# ===================== TITLE =====================
free_text(60, 30, "Peta Sumber Kebenaran, Workflow, dan Struktur Data", 28, INK)
free_text(60, 72, "AI Team Ical - VPS Hostinger - audit 28 Oktober 2026", 18, MUTED)

# ===================== EKSTERNAL =====================
zone(60, 150, 340, 1330, "EKSTERNAL")
b_ical = box(90, 200, 280, 120, "Ical (Irzal S. Ramin)\nPemilik & sumber\nkeputusan bisnis", YELLOW)
b_adam = box(90, 350, 280, 120, "Adam\nLead Architect\ndi workstation Ical,\nbukan di VPS ini", ORANGE)
b_tg = box(90, 500, 280, 100, "Telegram\nDM 7759144590", ORANGE)
b_gh = box(90, 630, 280, 100, "GitHub\nisumargo/ai-team", ORANGE)
b_or = box(90, 760, 280, 130, "OpenRouter\ntier gratis\nsisa kredit $0.14\ndari $10", ORANGE)
b_sync = box(90, 920, 280, 120, "Syncera\napi.syncera.id\n503: upstream penuh\nprovider utama EVE", ORANGE)
b_dns = box(90, 1070, 280, 100, "DNS + SSL\nRumahweb\nLet's Encrypt", ORANGE)
b_rules = box(90, 1200, 280, 240, "ATURAN KUNCI\n\n1. Retry maks 3x\n2. Output padat, tanpa basa-basi\n3. Hasil kerja wajib lewat Auditor\n4. Komunikasi antar-agen via file\n5. Selesai kerja -> push GitHub\n6. Dilarang catat nama model di memori", GREY, MUTED)

# ===================== VPS =====================
zone(440, 150, 1940, 1330, "VPS HOSTINGER - Ubuntu, 96G disk, RAM 7.7G, 2 core", "#1971c2")

zone(480, 210, 900, 600, "RUNTIME HERMES - yang benar-benar dieksekusi")
b_gw = box(510, 255, 400, 120, "Hermes Gateway\nsystemd user service\nUP, stabil 7+ hari\nrestart otomatis exit 75", BLUE)
b_mux = box(950, 255, 400, 120, "Multiplex 10 profil\n1 proses melayani\nsemua profil agent", BLUE)
b_eve = box(510, 405, 400, 110, "EVE (profil default)\nChief of Staff\nSOUL.md + bot Telegram utama", BLUE)
b_dasi = box(950, 405, 400, 110, "Dasiyah (pm-distribusi)\nProject Manager\nbot Telegram ke-2", BLUE)
b_prof8 = box(510, 545, 400, 110, "8 profil lain\ndeveloper guardian analyst\nauditor designer marketer\nsales strategist", BLUE)
b_audit = box(510, 680, 400, 110, "Alur audit 2 lapis\nL1 Auditor (teknis)\nL2 EVE (substansi)\nbaru lapor ke Ical", PURPLE)
b_db = box(950, 545, 400, 250, "state.db - pusat state\n\n47 sesi\n4071 pesan\n114 catatan pemakaian model\n11 obligation pengiriman\n8 delegasi async\n32 system prompt\n+ index pencarian FTS", TEAL)

zone(480, 850, 900, 290, "OTOMASI CRON - no_agent, 0 token")
b_cron = box(510, 900, 400, 100, "Cron scheduler\ndi dalam proses gateway\ncatch_up_missed: true", GREY, MUTED)
b_jobs = box(510, 1030, 400, 90, "3 job aktif\n30 menit / 6 jam / 15 menit", GREY, MUTED)
b_scripts = box(950, 900, 400, 220, "Script Python murni\n\ncheck_usage.py\ncek kredit, auto-switch model\n\nbackup.py\ntar.gz ke /root/backups\n\nsession_monitor.py\nmonitor sesi", GREY, MUTED)

zone(480, 1180, 900, 260, "CONFIG, MEMORI, DOKUMENTASI")
b_cfg = box(510, 1230, 270, 170, "config.yaml (112KB)\n+ .env\n\nrouting model\n+ kredensial", YELLOW)
b_st = box(800, 1230, 270, 170, "status/*.json\n+ ROLE.md\n\ndokumentasi manual\nsering basi", RED)
b_memo = box(1090, 1230, 270, 170, "memo/\n\nEVE <-> Adam\nkoordinasi lintas\nworkstation", YELLOW)

zone(1420, 210, 920, 1230, "APLIKASI WEB, BOT, DAN SERVICE")
b_nginx = box(1450, 260, 860, 110, "nginx :80 / :443 - 4 virtual host\nhermes.raminesia.com | mc.raminesia.com | distro.raminesia.com | 9router.raminesia.com", GREEN)
b_django = box(1450, 410, 410, 210, "Django Distribusi - DOWN\nport 8080 mati, 2 proses sisa\n\nModel: Product, Reseller,\nStockMovement, Transaction,\nChatSession (SQLite)", RED)
b_ruang = box(1910, 410, 400, 210, "Ruang 3D Office - DOWN\nruang.service tak jalan\nport 3001 mati\nmembaca status/*.json", RED)
b_dash = box(1450, 660, 410, 160, "Hermes Dashboard - UP\nport 9119\nbaca state.db langsung\nhermes.raminesia.com", GREEN)
b_router = box(1910, 660, 400, 160, "9router - UP\nport 20128\nrouter model lokal\n\nOllama - UP\nport 11434, qwen3.5:2b", GREEN)
b_bot = box(1450, 860, 410, 190, "Pipeline bot Dasiyah\nwebhook -> parser.py\n-> agent.py -> OpenRouter\n\ninkling:free + fallback Llama-3.3\nchat multi-turn di ChatSession", PURPLE)
b_relay = box(1910, 860, 400, 190, "bot_relay/\nantrian pesan saat\ngateway restart\n\nMonarx - UP\nport 65529, security scanner", GREY, MUTED)
b_mem = box(1450, 1090, 860, 140, "Memori & skill\nmemories/MEMORY.md (15 fakta) | USER.md (preferensi) | SOUL.md (persona EVE)\n55 skill di 13 kategori di skills/", TEAL)
b_bkp = box(1450, 1270, 860, 140, "Backup & log\n/root/backups 13 tar.gz = 189MB dari cap 200MB (mepet, belum exclude venv + node_modules)\nlogs/ 18MB - errors.log mencatat 503 Syncera dan LLM smart-approval gagal", TEAL)

# ===================== ARROWS =====================
arrow(b_ical, "bottom", b_tg, "top", "chat")
arrow(b_ical, "right", b_adam, "left", "memo", dashed=True)
arrow(b_tg, "right", b_eve, "left", "ke EVE")
arrow(b_tg, "right", b_dasi, "left", "ke Dasiyah")
arrow(b_gw, "right", b_mux, "left", "route")
arrow(b_gw, "bottom", b_db, "top", "state", dashed=True)
arrow(b_eve, "right", b_prof8, "right", "delegasi", dashed=True)
arrow(b_prof8, "bottom", b_audit, "top", "laporan")
arrow(b_audit, "left", b_eve, "bottom", "LULUS")
arrow(b_cron, "bottom", b_jobs, "top")
arrow(b_cron, "right", b_scripts, "left", "eksekusi")
arrow(b_eve, "bottom", b_cfg, "top", "routing", dashed=True)
arrow(b_prof8, "right", b_st, "left", "tulis status", dashed=True)
arrow(b_eve, "right", b_memo, "left", "koordinasi", dashed=True)
arrow(b_adam, "right", b_memo, "left", "koordinasi", dashed=True)
arrow(b_eve, "left", b_gh, "right", "push", dashed=True)
arrow(b_eve, "left", b_sync, "right", "primary", dashed=True)
arrow(b_dasi, "bottom", b_bot, "top")
arrow(b_bot, "left", b_or, "right", "chat_completions")
arrow(b_scripts, "left", b_gh, "right", "GET /credits", dashed=True)
arrow(b_nginx, "bottom", b_dash, "top", "9119")
arrow(b_nginx, "bottom", b_django, "top", "8080 mati", "#e03131")
arrow(b_nginx, "bottom", b_ruang, "top", "3001 mati", "#e03131")
arrow(b_dash, "bottom", b_db, "bottom", "baca", dashed=True)
arrow(b_ruang, "left", b_st, "right", "baca status", dashed=True)
arrow(b_prof8, "bottom", b_mem, "bottom", "", dashed=True)
arrow(b_scripts, "bottom", b_bkp, "bottom", "tar.gz 6 jam", dashed=True)

# ===================== TEMUAN =====================
zone(60, 1520, 2320, 300, "TEMUAN AUDIT - YANG PERLU DIPERBAIKI", "#e03131")
box(100, 1580, 540, 210, "1. Dua sumber kebenaran\nROLE.md vs SOUL.md ditulis 2x\nstatus/*.json hanya 5 dari 9 agen\nprofiles/developer/config.yaml = 109KB\n\nKonsekuensi: yang dibaca != yang jalan", RED)
box(660, 1580, 540, 210, "2. Tiga service mati\nDjango distro (8080)\nRuang (3001)\nsystemd user bus (DBUS)\n\nKonsekuensi: 2 domain 502, restart manual", RED)
box(1220, 1580, 540, 210, "3. Biaya & kuota\nOpenRouter sisa $0.14\nlimit $5 sudah terlewati\nSyncera 503 terus\n\nKonsekuensi: agent yang perlu kualitas tersendat", RED)
box(1780, 1580, 560, 210, "4. SOP bolong\nPush GitHub terakhir 23 Okt\nBackup 189/200MB\nNama model bocor di 5 file\nSOP hemat kuota cuma di 1 versi\n\nKonsekuensi: aturan tidak dijalankan konsisten", RED)

doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "hermes-agent",
    "elements": els,
    "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
    "files": {},
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)

txt = [e for e in els if e["type"] == "text"]
print(f"OK {len(els)} el | rect {sum(1 for e in els if e['type']=='rectangle')} | "
      f"text {len(txt)} | arrow {sum(1 for e in els if e['type']=='arrow')}")
print(f"font < 16: {sum(1 for e in txt if e.get('fontSize',16) < 16)}")
print(f"emoji di teks: {sum(1 for e in txt if any(ord(c) > 0x2500 for c in e['text']))}")
print(f"-> {OUT}")
