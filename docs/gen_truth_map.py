#!/usr/bin/env python3
'''Generate truth-map.excalidraw — peta sumber kebenaran AI Team Ical (2026-10-28).'''
import json, random, datetime

random.seed(20261028)
NOW = int(datetime.datetime.now().timestamp() * 1000)
els = []

def _base(t, idr, x, y, w, h, stroke, bg, dashed=False, fill="solid", sw=1.5):
    return {
        "type": t, "id": idr, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": sw, "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": {"type": 3} if t == "rectangle" else None,
        "seed": random.randint(1, 2**31), "version": 2, "versionNonce": random.randint(1, 2**31),
        "isDeleted": False, "boundElements": None, "updated": NOW, "link": None, "locked": False,
    }

_seq = [0]
def nid(p):
    _seq[0] += 1
    return f"{p}{_seq[0]:03d}"

def rect(x, y, w, h, text, stroke, bg, fs=14, dashed=False, sw=1.5, fill="solid"):
    rid = nid("r")
    r = _base("rectangle", rid, x, y, w, h, stroke, bg, dashed=dashed, fill=fill, sw=sw)
    els.append(r)
    if text:
        tid = nid("t")
        lines = text.count("\n") + 1
        r["boundElements"] = [{"id": tid, "type": "text"}]
        els.append({
            "type": "text", "id": tid, "x": x + 8, "y": y + 6, "width": w - 16, "height": 16 * lines,
            "angle": 0, "strokeColor": "#e9ecef", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
            "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
            "seed": random.randint(1, 2**31), "version": 2, "versionNonce": random.randint(1, 2**31),
            "isDeleted": False, "boundElements": None, "updated": NOW, "link": None, "locked": False,
            "text": text, "fontSize": fs, "fontFamily": 1, "textAlign": "left",
            "verticalAlign": "middle", "containerId": rid, "originalText": text,
            "autoResize": True, "lineHeight": 1.25,
        })
    return rid

def label(x, y, text, fs=20, color="#e9ecef"):
    tid = nid("x")
    lines = text.count("\n") + 1
    els.append({
        "type": "text", "id": tid, "x": x, "y": y, "width": fs * 0.6 * max(len(l) for l in text.split("\n")),
        "height": fs * lines, "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
        "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
        "seed": random.randint(1, 2**31), "version": 2, "versionNonce": random.randint(1, 2**31),
        "isDeleted": False, "boundElements": None, "updated": NOW, "link": None, "locked": False,
        "text": text, "fontSize": fs, "fontFamily": 1, "textAlign": "left",
        "verticalAlign": "top", "containerId": None, "originalText": text,
        "autoResize": True, "lineHeight": 1.25,
    })

def arrow(x1, y1, x2, y2, txt=None, stroke="#868e96", dashed=False, both=False):
    aid = nid("a")
    a = _base("arrow", aid, x1, y1, abs(x2 - x1), abs(y2 - y1), stroke, "transparent", dashed=dashed, fill="solid", sw=1.5)
    a["roundness"] = None
    a["points"] = [[0, 0], [x2 - x1, y2 - y1]]
    a["lastCommittedPoint"] = None
    a["startBinding"] = None
    a["endBinding"] = None
    a["startArrowhead"] = "arrow" if both else None
    a["endArrowhead"] = "arrow"
    els.append(a)
    if txt:
        lid = nid("l")
        a["boundElements"] = [{"id": lid, "type": "text"}]
        els.append({
            "type": "text", "id": lid, "x": (x1 + x2) / 2 - 60, "y": (y1 + y2) / 2 - 10,
            "width": 120, "height": 15, "angle": 0, "strokeColor": "#ced4da",
            "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
            "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": random.randint(1, 2**31), "version": 2,
            "versionNonce": random.randint(1, 2**31), "isDeleted": False, "boundElements": None,
            "updated": NOW, "link": None, "locked": False, "text": txt, "fontSize": 12,
            "fontFamily": 1, "textAlign": "center", "verticalAlign": "middle",
            "containerId": aid, "originalText": txt, "autoResize": True, "lineHeight": 1.25,
        })
    return aid

GOLD, RED, GRN, BLU, ORG, GRY, YLW = "#d9a520", "#fa5252", "#51cf66", "#4dabf7", "#ffa94d", "#adb5bd", "#ffd43b"

# ============ TITLE & LEGEND ============
label(340, 15, "PETA SUMBER KEBENARAN — AI TEAM ICAL (2026-10-28)", 24, "#74c0fc")
label(40, 1480, "🟢 UP   🔴 DOWN   🟡 runtime Hermes   🔵 database/state   ✅ sumber kebenaran   ←→ dua arah", 14, GRY)

# ============ EXTERNAL (kolom kiri) ============
rect(40, 120, 180, 100, "👤 Ical\n(Irzal S. Ramin)\nOwner — sumber\nkeputusan bisnis", GOLD, "transparent")
rect(40, 260, 180, 120, "🧠 Adam\nLead Architect\n(di workstation Ical,\nbukan di VPS)\nIDE + memo file", GOLD, "transparent")
rect(40, 420, 180, 80, "💬 Telegram\nDM 7759144590", GOLD, "transparent")
rect(40, 560, 180, 100, "☁️ OpenRouter\nmodel :free\n(Nemotron · Inkling\n· MiniMax) — sisa\nkredit $0.14", GOLD, "transparent")
rect(40, 690, 180, 90, "☁️ Syncera\napi.syncera.id\n/anthropic\n503 — penuh", GOLD, "transparent")
rect(40, 810, 180, 70, "🐙 GitHub\nisumargo/ai-team", GOLD, "transparent")
rect(40, 910, 180, 80, "🌐 DNS Rumahweb\n*.raminesia.com", GOLD, "transparent")

# ============ VPS FRAME ============
rect(300, 60, 1620, 1080, "", "#74c0fc", "#1c2329", sw=2)
label(316, 68, "VPS HOSTINGER — Ubuntu, bare metal", 18, "#74c0fc")

# --- B1: RUNTIME HERMES ---
rect(330, 110, 700, 640, "", YLW, "transparent", dashed=False, sw=1.2)
label(346, 118, "RUNTIME HERMES (dieksekusi)", 15, YLW)
rect(350, 150, 300, 130, "🚪 Hermes Gateway\nsystemd user service\nUP · pid 1646520 (7+ hari)\nRestart=always · exit 75", YLW, "#4d3900")
rect(350, 310, 300, 80, "🔀 multiplex_profiles: true\nserved: default + 9 profile", YLW, "transparent")
rect(350, 420, 300, 70, "🟣 default = EVE\nSOUL.md + Telegram bot utama", YLW, "#4d3900")
rect(350, 510, 300, 70, "🚬 pm-distribusi = Dasiyah\nbot Telegram ke-2 (chat sama)", YLW, "#4d3900")
rect(350, 600, 300, 130, "⚙️ 8 profile lain:\ndeveloper · guardian · analyst\nauditor · designer · marketer\nsales · strategist", YLW, "transparent")
rect(690, 150, 310, 330, "🗄️ state.db — PUSAT STATE\nsessions: 47\nmessages: 4071\nsession_model_usage: 114\ndelivery_obligations: 11\nasync_delegations: 8\nsystem_prompts: 32\n+ FTS index pencarian", BLU, "#1d3a5f")
rect(690, 500, 310, 230, "✅ SUMBER SEBENARNYA\nPER-AGEN:\nprofiles/<nama>/\n ├ SOUL.md (persona aktif)\n ├ config.yaml (model+fallback)\n ├ cron/ · sessions/ · memories/\n └ skills/\n(root/ai-team ROLE+status\n = salinan manual, basi)", GRN, "#1d3a1d", fs=13)

# --- B2: CRON ---
rect(330, 770, 700, 330, "", GRY, "transparent", dashed=False, sw=1.2)
label(346, 778, "OTOMASI CRON (no_agent — 0 token)", 15, GRY)
rect(350, 810, 300, 110, "⏰ Cron scheduler\ndalam proses gateway\njobs.json + executions.db\ncatch_up_missed: true", GRY, "#333a40")
rect(350, 960, 300, 110, "🛡️ skrip Python murni\ncheck_usage.py\nbackup.py\nsession_monitor.py", GRY, "transparent", fs=13)
rect(690, 810, 310, 290, "📋 3 cron job:\n• guardian-openrouter-check\n  tiap 30m → check_usage.py\n  cek kredit OpenRouter\n  tulis status/usage-log\n• guardian-backup tiap 6 jam\n  backup.py → /root/backups\n• session-monitor-v2 tiap 15m\n  session_monitor.py", GRY, "transparent", fs=13)

# --- B3: APLIKASI WEB ---
rect(1060, 110, 860, 990, "", GRN, "transparent", dashed=False, sw=1.2)
label(1076, 118, "APLIKASI WEB & BOT", 15, GRN)
rect(1080, 150, 820, 80, "🟢 nginx :80/:443 — 4 vhost · SSL Let's Encrypt\nhermes.raminesia.com→9119 · mc→3001(MATI) · distro→8080(MATI) · 9router→20128(UP)", GRN, "transparent", fs=13)
rect(1080, 250, 400, 200, "🔴 Django Distro — DOWN\nport 8080 mati → distro.\nraminesia.com 502\n2 buah runserver sisa\n(pid 405555 + 817100) barebut\n\nmodels: Product · Reseller\nStockMovement · Transaction\nChatSession (SQLite)\nadmin: admin/admin123", RED, "transparent", fs=13)
rect(1500, 250, 400, 150, "🟢 Hermes Dashboard\nUP :9119 — baca state.db\n(Next dev 5173: konfigurasi\nnginx ada, server tidak jalan)", GRN, "transparent", fs=13)
rect(1080, 470, 400, 160, "🤖 Dasiyah bot (runtime di gateway)\nprofil pm-distribusi: SOUL.md\nparser.py → agent.py → OpenRouter\ninkling:free + fallback Llama-3.3\nChatSession: konteks multi-turn", "#82c91e", "transparent", fs=13)
rect(1500, 420, 400, 120, "🛡️ Monarx Agent\nsecurity scanner (systemd)\nlistening :65529", "#82c91e", "transparent", fs=13)
rect(1500, 560, 400, 130, "🔀 9router — UP :20128\nrouter model lokal (Next.js)\n9router.raminesia.com\nenv: JWT + pass di unit svc", "#82c91e", "transparent", fs=13)
rect(1080, 650, 400, 140, "🔴 Ruang (3D office) — DOWN\nruang.service tak jalan\nport 3001 mati\nmc.raminesia.com → 502\ndesain: baca status/*.json", RED, "transparent", fs=13)
rect(1500, 710, 400, 130, "🧠 Ollama — UP :11434\nqwen3.5:2b (2.6GB) Q8_0\nbackup lokal gratis", GRN, "transparent", fs=13)
rect(1080, 810, 400, 170, "🗄️ memori & skill\nmemories/MEMORY.md: 15 fakta\nUSER.md: preferensi Ical\nSOUL.md: persona EVE\nskills/: 55 skill (13 kategori)\n⚠ MEMORY.md menyebut limit\n$20 vs $5 — 2 versi beda", BLU, "#1d3a5f", fs=13)
rect(1500, 860, 400, 120, "📦 bot_relay/\nantrian relay Telegram saat\ngateway mati · roster.json\nplatforms/pairing (kosong)", GRY, "transparent", fs=13)

# --- B4: CONFIG/MEMORI/OPS ---
rect(330, 1120, 1620, 330, "", ORG, "transparent", dashed=False, sw=1.2)
label(346, 1128, "CONFIG, GIT & OPS", 15, ORG)
rect(350, 1160, 340, 190, "⚙️ ~/.hermes/config.yaml (112KB)\nmodel.default → Syncera claude\nprovider: anthropic\nfallback → openrouter\n minimax-m3.1-flash:free\n⚠ hanya utk default (EVE);\n9 profile punya config.yaml\nmasing-masing (openrouter free)", YLW, "#4d3900", fs=13)
rect(710, 1160, 280, 90, "🔒 .env\nkredensial: token Telegram,\nAPI key, DB", GOLD, "transparent", fs=13)
rect(710, 1270, 280, 150, "🚨 ai-team/status/*.json\nhanya 5 dari 9 agen\n4 agen tak difile\nkebanyakan basi (17 Okt)", RED, "transparent", fs=13)
rect(1010, 1160, 330, 190, "💾 /root/backups\n13 tar.gz · 189MB\ncap 200MB → hampir penuh\nbelum exclude venv +\nnode_modules\nbackup.py tiap 6 jam\n(0 token)", RED, "transparent", fs=13)
rect(1360, 1160, 560, 120, "🐙 repo git ~/ai-team → GitHub isumargo/ai-team\nbranch main ↔ origin/main · push terakhir 23 Okt\n5 file tertunda (memo + guardian reports)", GRY, "transparent", fs=13)
rect(1360, 1300, 560, 130, "📋 logs/ 18MB — gateway.log · agent.log · errors.log\n503 Syncera (upstream penuh) tercatat di errors.log\nsmart-approvals LLM gagal saat provider down", GRY, "transparent", fs=13)

# ============ ARROWS ============
arrow(140, 220, 140, 420, "chat DM", GOLD)
arrow(140, 370, 130, 260, "", GOLD, dashed=True)
arrow(220, 460, 350, 215, "EVE & Dasiyah (chat ID sama)", GOLD)
arrow(220, 315, 330, 315, "memo file · review", GOLD, dashed=True)
arrow(660, 215, 690, 215, "baca/tulis", YLW, both=True)
arrow(500, 390, 500, 420, "rute chat → profil", YLW)
arrow(500, 720, 500, 810, "tick", GRY)
arrow(450, 940, 450, 960, "", GRY)
arrow(690, 865, 220, 610, "GET /credits", GRY)
arrow(660, 1010, 1010, 1240, "tar.gz tiap 6 jam", GRY)
arrow(1290, 230, 1290, 250, "8080 ✗", RED)
arrow(1750, 230, 1700, 560, "20128 ✓", GRN)
arrow(1850, 230, 1700, 710, "9119 ✓", GRN)
arrow(1150, 230, 1280, 650, "3001 ✗→502", RED)
arrow(1030, 535, 1080, 535, "multi-turn", "#82c91e")
arrow(1080, 550, 220, 605, "chat_completions\nPOST /api/v1", "#82c91e")
arrow(355, 1255, 130, 700, "HTTPS", YLW)
arrow(1360, 1220, 220, 845, "git push (5 file tertunda)", GRY, dashed=True)
arrow(1080, 715, 992, 1280, "baca status/*.json", RED)
arrow(660, 1015, 710, 1300, "tulis status", GRY)

doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "eve-vps-audit",
    "files": {},
    "appState": {"gridSize": None, "viewBackgroundColor": "#121212"},
    "elements": els,
}
out = "/root/ai-team/docs/truth-map.excalidraw"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
print(f"OK {len(els)} elements → {out}")