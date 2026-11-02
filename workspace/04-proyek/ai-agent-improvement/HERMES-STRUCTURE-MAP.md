# Hermes Best Practice: Folder Structure Map

**Date:** 2026-11-02  
**Purpose:** Clear, non-overlapping layout to prevent conflicts and errors.  
**Applies to:** All profiles + project + runtime.

---

## PART 1: Runtime Default & Discovery

### Runtime Default = `~/.hermes/` (OR `$HERMES_HOME`)

This is Hermes framework root. Everything else depends on this.

```
~/.hermes/
├─ config.yaml              ← PRIMARY: global model, provider, tools config
├─ .env                     ← SECRETS: API keys (never git)
├─ SOUL.md                  ← Agent personality (EVE's persona for default profile)
├─ state.db                 ← Session store (SQLite, never touch)
├─ memories/                ← Persistent memory (read-only from user's view)
│  ├─ USER.md              ← User profile (who is Cal)
│  └─ MEMORY.md            ← Agent notes (learned facts)
├─ skills/                  ← PRIMARY skills directory (source of truth)
├─ profiles/                ← Per-agent isolated homes
│  ├─ analyst/
│  ├─ developer/
│  ├─ guardian/
│  └─ ... (8 total)
└─ ... (scripts, cron, sessions, logs, backups)
```

**Key:** `~/.hermes/` is the RUNTIME DEFAULT that Hermes loads on startup.  
**No user edits here except:** `config.yaml`, `.env`, `SOUL.md`.  
**Never edit manually:** `state.db`, `sessions/`, `memories/` (agent owns these).

---

## PART 2: Profiles — Each Agent Gets Its Own Home

### Profile Structure: `~/.hermes/profiles/<agent-name>/`

Each of the 9 agents (analyst, auditor, designer, developer, guardian, marketer, pm-distribusi, sales, strategist) gets **isolated config + state**.

```
~/.hermes/profiles/developer/
├─ config.yaml              ← Developer-specific: model (e.g. coding-high), provider, toolsets
├─ .env                     ← Developer-specific: secrets (if any)
├─ SOUL.md                  ← Developer personality (override default)
├─ state.db                 ← Developer's own sessions
├─ memories/
│  ├─ USER.md              ← (optional: developer-specific user profile)
│  └─ MEMORY.md            ← Developer's own notes
└─ skills/                  ← (optional: developer-specific skills)
```

**RULE: Never point 2 agents to same profile.**  
If you do: both write to same `state.db` + `memories/` → state corrupts → cache breaks.

**Memory in profiles:** Each profile CAN have its own `memories/USER.md` + `MEMORY.md`, but it's optional. If absent, uses global `~/.hermes/memories/`.

---

## PART 3: Skills — Where Are They?

### Skills Priority (First Match Wins)

```
1. Project-LOCAL skills   ← /root/ai-team/workspace/skills/ (if trusted + configured)
2. Profile skills         ← ~/.hermes/profiles/<name>/skills/ (per-agent, if exists)
3. Global skills          ← ~/.hermes/skills/  (PRIMARY source of truth)
```

**Best Practice: Skills go in `~/.hermes/skills/` (global).**

Why?
- Single source of truth
- All agents share
- No per-profile duplication
- Easier maintenance

**When to use per-profile skills:**
- Agent needs ONLY its own custom skills
- Never share skills across agents via per-profile storage — use global instead

**When to use project-local skills:**
- Project has `SKILL.md` files inside workspace
- Configure in `config.yaml`:
  ```yaml
  skills:
    external_dirs:
      - /root/ai-team/workspace/skills/
  ```
- Requires **explicit trust** (user opts-in per project)

---

## PART 4: Config Precedence — Which `config.yaml` Wins?

### Config Discovery Order

When you run `hermes` or spawn a profile:

```
1. Profile-specific         ← ~/.hermes/profiles/<name>/config.yaml    (HIGHEST priority)
2. Global default           ← ~/.hermes/config.yaml
3. Hermes built-in          ← (fallback, never edit)
```

**Example:**
```
~/.hermes/config.yaml:
  model:
    default: coding-high
    
~/.hermes/profiles/developer/config.yaml:
  model:
    default: coding-high-o3   ← Developer overrides global
```

Developer agent uses `coding-high-o3`. Other agents use `coding-high`.

**KEY RULE:** Profile config keys OVERRIDE global. Unset keys inherit from global.

**"Why does Hermes rollback to Nemotron?" — likely cause:**
- Global `config.yaml` has `default: nemotron` (fallback/old)
- Profile doesn't explicitly override
- Hermes falls back to global
- **Fix:** Update profile's `config.yaml` with the correct model.

---

## PART 5: Memory — `USER.md` vs `MEMORY.md`

### Memory Discovery Order

```
1. Profile-specific         ← ~/.hermes/profiles/<name>/memories/USER.md   (if exists)
2. Global default           ← ~/.hermes/memories/USER.md

Same for MEMORY.md
```

**Best Practice: Keep memory GLOBAL (in `~/.hermes/memories/`).**

Why?
- One canonical source of truth
- All agents see Cal's preferences (who Cal is)
- No per-profile duplication

**When to use per-profile memory:**
- Agent needs ONLY its own private notes
- Share global memory + agent-specific memory: use global USER.md + per-profile MEMORY.md

---

## PART 6: Context Files — AGENTS.md, SOUL.md

### Context Files (Project Instructions)

```
/root/ai-team/AGENTS.md           ← Canonical: team policy + SOP
/root/ai-team/workspace/           ← Project context (auto-discovered)
```

**Discovery:**
- Hermes auto-loads AGENTS.md from **current working directory** (CWD)
- If running in `/root/ai-team/` → loads `/root/ai-team/AGENTS.md`
- If running in `~/.hermes/` → no AGENTS.md (not a project dir)

**Best Practice:**
- One AGENTS.md per project
- Put it at project root (`/root/ai-team/AGENTS.md`)
- Delete duplicates (`/root/AGENTS.md`, `~/.hermes/AGENTS.md`, workspace copies)

---

## PART 7: Validation Checklist — To Prevent Errors

Before making structural changes, verify:

### ✅ Config Validation
- [ ] Global `~/.hermes/config.yaml` has model + provider set
- [ ] Each profile's `config.yaml` explicitly sets model (no inheriting surprises)
- [ ] No hardcoded paths pointing to old locations

### ✅ Profile Validation
- [ ] Each profile has exactly ONE agent (not 2 agents → 1 profile)
- [ ] Profile path matches agent name: `~/.hermes/profiles/developer/` for developer agent
- [ ] Each profile has own `state.db` (never shared)

### ✅ Memory Validation
- [ ] Global `~/.hermes/memories/USER.md` exists (Cal's profile)
- [ ] `USER.md` has no duplicate entries per profile
- [ ] Per-profile `memories/` only used when necessary (not default)

### ✅ Skills Validation
- [ ] Primary source: `~/.hermes/skills/` (non-empty)
- [ ] No duplicate skill names across sources
- [ ] Project-local skills explicitly configured (if used)
- [ ] Per-profile skills only when agent has special needs (rare)

### ✅ Context Files Validation
- [ ] ONE AGENTS.md per project (at project root)
- [ ] No floating AGENTS.md in `/root/`
- [ ] No duplicate AGENTS.md in `~/.hermes/` (delete it)
- [ ] Hermes auto-discovers from CWD (no hardcoding needed)

### ✅ Secrets Validation
- [ ] API keys in `.env` (never in git)
- [ ] Each profile can have own `.env` (if isolated credentials needed)
- [ ] No credentials in config.yaml

---

## PART 8: Deployment Impact Map

### If You Move/Change These Files → Error Risk

| File/Folder | Change | Impact | Fix |
|---|---|---|---|
| `~/.hermes/config.yaml` | Delete | Hermes won't start | Restore from backup or run setup |
| `~/.hermes/state.db` | Delete | All sessions lost | Restore from backup |
| `~/.hermes/profiles/<name>/` | Delete | Agent loses config + memory | Restore or recreate profile |
| `/root/AGENTS.md` | Delete | Team policy unreachable (if CWD is root) | Move to `/root/ai-team/AGENTS.md` |
| `~/.hermes/skills/` | Delete | All custom skills lost | Restore from backup |
| `~/.hermes/profiles/<name>/memories/` | Delete | Agent loses notes | Restore from backup |

---

## PART 9: Decision Tree — Where Should I Put It?

```
┌─ Is it an API key / secret?
│  └─ YES → ~/.hermes/.env (or profile-specific .env)
│
├─ Is it team policy / SOP?
│  └─ YES → /root/ai-team/AGENTS.md (at project root)
│
├─ Is it agent personality?
│  └─ YES → ~/.hermes/SOUL.md (global) or ~/.hermes/profiles/<name>/SOUL.md (override)
│
├─ Is it Cal's profile (preferences, name)?
│  └─ YES → ~/.hermes/memories/USER.md (global)
│
├─ Is it agent notes / learned facts?
│  └─ YES → ~/.hermes/memories/MEMORY.md (global)
│
├─ Is it a reusable skill / procedure?
│  └─ YES → ~/.hermes/skills/<category>/ (global)
│
├─ Is it project-specific workspace data?
│  └─ YES → /root/ai-team/workspace/
│
└─ Is it a working folder (inbox, temp)?
   └─ YES → /root/ai-team/workspace/00-inbox/ or workspace/05-status/
```

---

## PART 10: Why You Got This Map

**Problem statement (from Cal):**
- 4 AGENTS.md files floating around (conflict)
- 3 backup.py files with hardcoded paths (maintenance nightmare)
- Per-profile skills scattered (confusion)
- Config precedence unclear (why Nemotron rollback?)
- No clear best practice

**Solution:**
- One canonical per data type
- Clear precedence (profile > global > default)
- Validation checklist (prevent future errors)
- Decision tree (where to put new data)

**After consolidation:**
- Delete 3 of 4 AGENTS.md
- Move canonical to `/root/ai-team/AGENTS.md`
- Update 2 backup.py paths
- Git commit + push
- Document in this map
- Future changes follow decision tree

---

## Appendix: Current State (2026-11-02)

### ✅ What's CORRECT
- `~/.hermes/config.yaml` exists, model set
- Each profile has config.yaml
- `~/.hermes/memories/USER.md` exists (Cal profile)
- Global `~/.hermes/skills/` is primary
- Profiles are isolated (no sharing)

### ⚠️ What Needs FIXING
- Multiple AGENTS.md files (consolidate)
- Hardcoded paths in backup.py (update)
- sync_policy.py generating to 4 targets (simplify to 1)
- `.gitignore` not protecting workspace runtime output (update)

### 📋 Checklist Before Next Session
1. [ ] Consolidate AGENTS.md to `/root/ai-team/AGENTS.md`
2. [ ] Update backup.py paths (2 files)
3. [ ] Update sync_policy.py targets (1 file)
4. [ ] Delete duplicate AGENTS.md files
5. [ ] Update .gitignore
6. [ ] Git commit + push
7. [ ] Test: spawn Hermes in `/root/ai-team/` → loads AGENTS.md ✓

