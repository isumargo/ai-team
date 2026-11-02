# Runtime Config Mapping — Lengkap + Dependency Matrix

**Tanggal:** 2026-11-02  
**Tujuan:** Peta lengkap siapa ambil dari mana, priority order, dan dependency.

---

## BAGIAN 1: CONFIG.YAML — Priority Precedence

### Lokasi Config

```
~/.hermes/config.yaml                          ← PRIMARY (global)
~/.hermes/profiles/<name>/config.yaml          ← OVERRIDE (per-profile)
~/.hermes/profiles/<name>/config.yaml          ← Fallback ke global jika key tidak set
```

### Priority Order (Yang Dibaca Hermes)

```
Level 1 (HIGHEST):  ~/.hermes/profiles/analyst/config.yaml
                    (jika ada key = pakai ini)
                    ↓
Level 2:           ~/.hermes/config.yaml
                    (jika key tidak ada di Level 1 = pakai ini)
                    ↓
Level 3 (LOWEST):  Hermes built-in default
                    (fallback terakhir, tidak pernah edit)
```

### Contoh: Model Setting

```yaml
# File: ~/.hermes/config.yaml (GLOBAL)
model:
  default: coding-high
  provider: custom

# File: ~/.hermes/profiles/developer/config.yaml (OVERRIDE)
model:
  default: coding-high-o3    ← Developer pakai ini
  provider: custom

# File: ~/.hermes/profiles/analyst/config.yaml (TIDAK ADA)
# → Analyst jatuh ke global: coding-high
```

**Hasilnya:**
- Developer → `coding-high-o3` (dari profile-specific)
- Analyst → `coding-high` (dari global)
- Guardian → `coding-high` (dari global, karena profile tidak override)

### Apa yang Bisa Override?

| Setting | Bisa Override? | Lokasi Override |
|---------|---|---|
| model.default | ✅ Yes | profiles/*/config.yaml |
| model.provider | ✅ Yes | profiles/*/config.yaml |
| tools (toolsets) | ✅ Yes | profiles/*/config.yaml |
| terminal.backend | ✅ Yes | profiles/*/config.yaml |
| display.skin | ⚠️ Per-session | CLI flag `-t skin:name` |
| memory_enabled | ✅ Yes | profiles/*/config.yaml |

---

## BAGIAN 2: SKILLS — Search Order

### Lokasi Skills

```
1. Project-local          /root/ai-team/workspace/skills/
   (jika configured)

2. Profile-specific       ~/.hermes/profiles/<name>/skills/
   (per-agent skills, jarang)

3. Global (PRIMARY)       ~/.hermes/skills/
   (RECOMMENDED — semua agen pakai)
```

### Priority Order (Hermes Cari Skills)

```
Saat analyst pakai /skill-name:

1. Cek: /root/ai-team/workspace/skills/<skill-name>/  ← Project-local first
   Jika ada → PAKAI ini
   ↓
2. Cek: ~/.hermes/profiles/analyst/skills/<skill-name>/  ← Profile-specific
   Jika ada → PAKAI ini
   ↓
3. Cek: ~/.hermes/skills/<skill-name>/  ← Global
   Jika ada → PAKAI ini
   ↓
404: Skill tidak ditemukan
```

**Contoh: Skill "github"**

```
Analyst pakai /github:

1. /root/ai-team/workspace/skills/github/   ← cek
   (tidak ada)
   ↓
2. ~/.hermes/profiles/analyst/skills/github/  ← cek
   (tidak ada)
   ↓
3. ~/.hermes/skills/github/  ← ADA!
   → Pakai skill ini
```

### Best Practice: Skills HARUS GLOBAL

**Alasan:**
- Jangan duplikasi per-profile
- Update sekali di `~/.hermes/skills/`, semua agen dapat
- Lebih mudah maintenance

**Kapan pakai per-profile skills:**
- Agent butuh skill KHUSUS yang tidak dipakai agen lain (jarang)
- Misalnya: Developer punya skill "docker-debug" yang hanya dev pakai
- → Letakkan di `~/.hermes/profiles/developer/skills/docker-debug/`

---

## BAGIAN 3: AGENTS.MD (PROJECT CONTEXT) — Discovery

### Lokasi AGENTS.md

```
/root/ai-team/AGENTS.md              ← CANONICAL (source of truth)
```

### Discovery Order (Hermes Auto-Discover)

```
Saat Hermes spawn di /root/ai-team/:

1. Cek: /root/ai-team/AGENTS.md          ← CWD pertama
   Jika ada → AUTO-LOAD
   ↓
2. Cek: /root/.hermes.md atau /root/AGENTS.md  ← Parent directories
   (jika CWD tidak ada AGENTS.md)
   ↓
3. Tidak ada → No project context
   (Hermes tetap jalan, pakai SOUL.md + config saja)
```

**Contoh: Sesuai CWD**

```
Developer spawn di /root/ai-team/:
  → Hermes load /root/ai-team/AGENTS.md ✓

Developer spawn di /root/ai-team/workspace/:
  → Hermes cari parent: /root/ai-team/AGENTS.md
  → Load parent AGENTS.md ✓

Developer spawn di ~/.hermes/:
  → Tidak ada .hermes.md, tidak ada AGENTS.md
  → Tanpa project context (hanya SOUL.md)
```

### Best Practice: AGENTS.md SATU di Project Root

```
/root/ai-team/AGENTS.md              ← SATU saja, canonical
                                        (tidak di ~/.hermes/)
                                        (tidak di workspace/)
```

---

## BAGIAN 4: SOUL.MD (PERSONALITY) — Per-Profile

### Lokasi SOUL.md

```
~/.hermes/SOUL.md                      ← DEFAULT PROFILE (EVE personality)
~/.hermes/profiles/analyst/SOUL.md    ← Analyst personality
~/.hermes/profiles/developer/SOUL.md  ← Developer personality
~/.hermes/profiles/<name>/SOUL.md     ← Setiap profile punya sendiri
```

### Discovery Order

```
Saat Developer profile jalan:

1. Cek: ~/.hermes/profiles/developer/SOUL.md
   Jika ada → PAKAI ini (personality Developer)
   ↓
2. Jika tidak ada → fallback ke ~/.hermes/SOUL.md
   (global personality = EVE)
```

### Best Practice: SOUL.md TETAP DI MASING-MASING PROFILE

**Alasan:**
- Setiap agen punya personality berbeda
- Analyst ≠ Developer ≠ Guardian
- Tidak ada duplikasi — masing-masing isolated

**Jangan consolidate SOUL.md!** ❌
- Kalau consolidate ke satu file → semua agen jadi EVE
- Personality akan mixing/confused

---

## BAGIAN 5: MEMORY — Global

### Lokasi Memory

```
~/.hermes/memories/USER.md          ← Global (siapa Cal)
~/.hermes/memories/MEMORY.md        ← Global (apa yang dipelajari)

~/.hermes/profiles/<name>/memories/ ← Per-profile (optional, jarang)
```

### Discovery Order

```
Saat ada agen (analyst, developer, dsb):

1. Cek: ~/.hermes/profiles/analyst/memories/USER.md
   Jika ada → PAKAI ini
   ↓
2. Jika tidak ada → ~/.hermes/memories/USER.md
   (global user profile = siapa Cal)
```

### Best Practice: Memory GLOBAL (Di ~/.hermes/memories/)

**Alasan:**
- Cal profil adalah global (siapa Cal, preferensi Cal)
- Semua agen harus tau: "ini kalanya prefer concise answers"
- Jangan duplicate per-profile

**Kapan per-profile memory:**
- Agent butuh private notes yang tidak shared
- Jarang. Biasanya memory global saja.

---

## BAGIAN 6: DEPENDENCY MATRIX — Kalau Berubah, Apa Affected?

### Jika Config.yaml Berubah (Global)

```
FILE: ~/.hermes/config.yaml

Berubah:                    → AFFECTED:
─────────────────────────────────────────
model.default (coding-high → coding-high-o3)
  → Semua profile tanpa override
  → Semua agen yang tidak punya profiles/*/config.yaml
  → Guardian, Analyst, Marketer (semuanya jadi o3)

tools (enable/disable browser)
  → Semua agen (global change)
  → Profile-specific tools masih override

display.skin (default theme)
  → Semua surface yang spawn dari ~/.hermes/
  → Desktop, CLI, TUI, gateway
```

### Jika Skills Berubah (Global)

```
FILE: ~/.hermes/skills/github/SKILL.md

Berubah:                    → AFFECTED:
─────────────────────────────────────────
github skill di-update
  → Analyst /github (kalau profile tidak override)
  → Developer /github (kalau profile tidak override)
  → Semua agen yang pakai /github

Tambah skill baru: /learn
  → Semua agen bisa akses (otomatis)
```

### Jika AGENTS.md Berubah (Project)

```
FILE: /root/ai-team/AGENTS.md

Berubah:                    → AFFECTED:
─────────────────────────────────────────
SOP Efisiensi Token (update)
  → Semua agen yang spawn di /root/ai-team/
  → Developer, Analyst, Guardian (CWD = project)
  → TIDAK affected agen di ~/.hermes/ (beda project)

Aturan team baru
  → System prompt berubah (sesi baru)
  → Session lama tetap pakai prompt lama
  → New session punya aturan baru
```

### Jika SOUL.md Berubah (Per-Profile)

```
FILE: ~/.hermes/profiles/developer/SOUL.md

Berubah:                    → AFFECTED:
─────────────────────────────────────────
Developer personality (update)
  → HANYA Developer profile
  → Analyst tidak affected (punya SOUL sendiri)
  → Guardian tidak affected
  → New session: punya personality baru
```

### Jika Memory Berubah (Global)

```
FILE: ~/.hermes/memories/USER.md

Berubah:                    → AFFECTED:
─────────────────────────────────────────
USER.md (Cal profile update)
  → Semua agen (Cal profil adalah global)
  → Analyst, Developer, Guardian (semuanya tau profil Cal baru)
  → New session: punya info Cal baru
  → Session lama: tetap pakai snapshot lama
```

---

## BAGIAN 7: DEPENDENCY GRAPH

```
HERMES SPAWN
    ↓
    ├─→ CWD?
    │   ├─ /root/ai-team/     → Load /root/ai-team/AGENTS.md ✓
    │   └─ ~/.hermes/         → No AGENTS.md (tidak project dir)
    ↓
    ├─→ Profile?
    │   ├─ analyst            → Load ~/.hermes/profiles/analyst/config.yaml
    │   │                         (override global ~/.hermes/config.yaml)
    │   └─ (default)          → Load ~/.hermes/config.yaml
    ↓
    ├─→ Model dari config
    │   └─ Precedence: profile > global > built-in
    ↓
    ├─→ SOUL.md (personality)
    │   ├─ Analyst: ~/.hermes/profiles/analyst/SOUL.md
    │   ├─ Developer: ~/.hermes/profiles/developer/SOUL.md
    │   └─ Default: ~/.hermes/SOUL.md (EVE)
    ↓
    ├─→ Memory (read-only di system prompt)
    │   ├─ USER.md: ~/.hermes/memories/USER.md (global)
    │   └─ MEMORY.md: ~/.hermes/memories/MEMORY.md (global)
    ↓
    ├─→ Skills (load on-demand)
    │   ├─ Priority: project-local > profile > global
    │   └─ /github → search skill di 3 location
    ↓
    └─→ READY! Session start dengan:
        - config (model, tools, etc.)
        - AGENTS.md (project rules)
        - SOUL.md (personality)
        - USER.md + MEMORY.md (memory)
        - Skills available (github, excalidraw, etc.)
```

---

## BAGIAN 8: DECISION TREE — Kalau Perlu Tambah/Ubah

```
Saya mau update X:

├─ Adalah shared behavior semua agen?
│  ├─ YES  → Edit ~/.hermes/config.yaml (GLOBAL)
│  └─ NO   → Edit ~/.hermes/profiles/<name>/config.yaml (PROFILE)
├─
├─ Adalah skill untuk semua agen?
│  ├─ YES  → Letakkan di ~/.hermes/skills/ (GLOBAL)
│  └─ NO   → Letakkan di ~/.hermes/profiles/<name>/skills/ (PROFILE)
├─
├─ Adalah team policy/SOP?
│  ├─ YES  → Edit /root/ai-team/AGENTS.md (PROJECT)
│  └─ NO   → Bukan concern kami
├─
├─ Adalah personality agen?
│  ├─ YES  → Edit ~/.hermes/profiles/<name>/SOUL.md (PROFILE)
│  └─ NO   → Bukan concern kami
├─
└─ Adalah Cal profil/preferensi?
   ├─ YES  → MEMORY.md atau USER.md (via memory tool)
   └─ NO   → Bukan concern kami
```

---

## BAGIAN 9: Current State (2026-11-02)

### ✅ CORRECT (Tidak perlu ubah)

```
Config:
  ✓ ~/.hermes/config.yaml ada + model set
  ✓ Setiap profile punya config.yaml sendiri
  ✓ Priority order bekerja

Skills:
  ✓ ~/.hermes/skills/ primary location
  ✓ Bundled skills ada
  ✓ Hub skills bisa install

Memory:
  ✓ ~/.hermes/memories/USER.md ada (Cal profil)
  ✓ ~/.hermes/memories/MEMORY.md ada
  ✓ Per-profile memory optional (correct)

SOUL.md:
  ✓ ~/.hermes/SOUL.md ada (EVE default)
  ✓ Setiap profile punya SOUL sendiri
  ✓ Tidak ada duplikasi

AGENTS.md:
  ✓ /root/ai-team/AGENTS.md canonical (baru saja)
  ✓ Duplikat sudah dihapus
  ✓ Auto-discover bekerja
```

### ⚠️ MONITOR (Watch for issues)

```
Nemotron rollback:
  ⚠️ Jika profile config tidak explicit set model
  → Profile fallback ke global
  → Global mungkin default ke nemotron (old)
  → Fix: Update semua profiles dengan model yang benar

Skills duplication:
  ⚠️ Jangan ada duplikasi skill nama di 3 location
  → Search order: project > profile > global
  → Kalau semua ada "github" → yang dipakai project saja

Memory per-profile:
  ⚠️ Jangan buat per-profile USER.md
  → Cal profil adalah global (shared)
  → Per-profile untuk special agent notes saja
```

---

## BAGIAN 10: Kesimpulan & Rules

### Priority Tabel Lengkap

| Item | Location | Type | Scope | Best Practice |
|------|----------|------|-------|---|
| **Config** | profile > global | Precedence | Per-agent + global | Override di profile jika needed |
| **Skills** | project > profile > global | Search | Shared/special | Global primary, profile untuk special |
| **AGENTS.md** | project root | Discovery | Project-wide | Satu canonical di /root/ai-team/ |
| **SOUL.md** | profile | Per-agent | Identity | Satu per profile (9 profiles) |
| **USER.md** | global + profile | Search | Cal profile | Global (shared semua agen) |
| **MEMORY.md** | global + profile | Search | Agent notes | Global prefer (shared knowledge) |

### Three Rules

1. **Config:** Profile override global. Update global untuk perubahan shared, profile untuk override.
2. **Skills:** Global primary. Jangan duplikasi. Project-local hanya jika config-specific.
3. **Context:** AGENTS.md di project root. SOUL.md per-profile. Memory global.

