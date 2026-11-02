# Provider Integration Status — 2026-11-02

**Session:** EVE (Chief of Staff)  
**Duration:** 2026-11-02 15:00 – 17:00 UTC  
**Status:** Completed & Tested ✓

---

## Ringkasan Pekerjaan

Integrasi tiga provider (Clouvia, Kiro, OpenRouter) ke dalam ekosistem Hermes Agent via 9Router local proxy di port 20128.

### Hasil Akhir:
- **616 total model** terindeks di Hermes Desktop model picker (9router provider)
- **Routing prefix:**
  - `kr/...` (Kiro, ~30 model)
  - `clouvia/...` (Clouvia, ~113 model)
  - `openrouter/...` (OpenRouter, ~451 model)
- **Testing:** End-to-end success ✓

---

## Detailed Actions & Status

### 1. Clouvia Router Integration

**Objective:** Add direct & proxied access ke Clouvia (`https://router.clouvia.id/v1`)

| Item | Action | Result |
|------|--------|--------|
| API Key | Append `CLOUVIA_API_KEY=[redacted]` to `/root/.hermes/.env` | ✓ Stored |
| Direct Provider | `hermes config set` provider `custom:clouvia` with base_url, model `coding-high`, max_tokens 32768 | ✓ Configured |
| CLI Test | `hermes -z "Balas satu kata: siap" --provider custom:clouvia -m coding-high` | ✓ Response: "Siap" |
| 9router Node | Registered API key to 9router node `openai-compatible-chat-8068f905-87bf-49a4-940e-8b1e8ca66600` | ✓ Active |
| Node Rename | Renamed DB entry from `openai` to `Clouvia` | ✓ Done |
| Proxy Test | `hermes -z "Balas satu kata: aman" --provider custom:9router -m clouvia/coding-high` | ✓ Response: "Aman" |

**Files Modified:**
- `/root/.hermes/.env` → added `CLOUVIA_API_KEY`
- `/root/.hermes/config.yaml` → `model.default: coding-high`, `providers.clouvia.*`
- `/root/.9router/db/data.sqlite` → node renamed to "Clouvia"

---

### 2. 9router Model Cache Update

**Objective:** Populate Hermes Desktop model picker with live 9router models

| Item | Action | Result |
|------|--------|--------|
| Live Fetch | GET `http://127.0.0.1:20128/v1/models` with NINEROUTER_API_KEY | ✓ 165 models (initial) |
| Cache Write | Write to `/root/.hermes/provider_models_cache.json` key `custom:http://127.0.0.1:20128/v1#d37c89c53d3db280` | ✓ Cached |
| Verification | `list_picker_providers()` confirms 165 models for 9router in picker | ✓ Verified |

**Model Breakdown (After Clouvia):**
- Kiro: 30 models
- Clouvia: 113 models
- Ollama: 22 models

---

### 3. OpenRouter Integration

**Objective:** Register OpenRouter as node in 9router, fetch & cache all models

| Item | Action | Result |
|------|--------|--------|
| API Key | Added `OPENROUTER_API_KEY=[redacted]` to `/root/.hermes/.env` | ✓ Stored |
| Node Registration | `api.createApiKeyProvider()` with provider type `openrouter`, API key from .env | ✓ Connection ID: `639dd247-b6f8-4649-81da-272077a2d88b` |
| Connection Test | `api.testConnection(connId)` | ✓ Valid: true |
| Model Fetch | GET `https://openrouter.ai/api/v1/models` with OpenRouter API key | ✓ 451 models fetched |
| Cache Integration | Filter out old `openrouter/` entries, append 451 live models to 9router cache | ✓ Total now: 616 models |
| Proxy Test | `hermes -z "Balas satu kata: mantap" --provider custom:9router -m openrouter/deepseek/deepseek-chat` | ✓ Response: "mantap" |

**Files Modified:**
- `/root/.hermes/.env` → added `OPENROUTER_API_KEY`
- `/root/.hermes/provider_models_cache.json` → appended 451 openrouter/* entries to 9router key

**Model Count After Integration:**
- Kiro (kr/): 30
- Clouvia (clouvia/): 113
- OpenRouter (openrouter/): 451
- Other (ollama, deepseek-web, etc.): 22
- **Total: 616 models**

---

## Pending Questions (User Confirmation Needed)

1. **Kiro Tier:** What plan is Cal using? (Free 50/mo? Pro $20/mo? Pro+ $40/mo?)
2. **Clouvia Billing:** Is this a paid subscription? Per-month or per-usage?
3. **OpenRouter Account:** Fresh free account or does it have prepaid credits?

→ Answer these to finalize routing strategy & failover priority.

---

## Current Configuration

### Hermes Desktop (`/root/.hermes/config.yaml`):
```yaml
model:
  default: coding-high
  provider: custom:clouvia
providers:
  clouvia:
    name: clouvia
    base_url: https://router.clouvia.id/v1
    key_env: CLOUVIA_API_KEY
    default_model: coding-high
    max_tokens: 32768
  9router:
    name: 9router
    base_url: http://127.0.0.1:20128/v1
    key_env: NINEROUTER_API_KEY
    default_model: kr/auto (or any prefix)
```

### 9Router Database (`/root/.9router/db/data.sqlite`):
- **3 Active Provider Nodes:**
  1. `Clouvia` (openai-compatible-chat-...) — Status: active, tested ✓
  2. `openrouter` (native provider type) — Status: active, tested ✓
  3. `ollama-local` — Status: inactive
  4. `kiro` (oauth) — Status: active via OAuth

### Model Cache (`/root/.hermes/provider_models_cache.json`):
- Key: `custom:http://127.0.0.1:20128/v1#d37c89c53d3db280`
- Models: 616 entries
- Last updated: 2026-11-02 16:22 UTC
- Format: Simple string array `["kr/...", "clouvia/...", "openrouter/...", ...]`

---

## Architecture & Routing

```
Hermes CLI/Desktop
    ↓
    ├─→ Provider: custom:clouvia (direct)
    │   └─→ https://router.clouvia.id/v1 (coding-high, penalaran)
    │
    ├─→ Provider: custom:9router (proxy/aggregator)
    │   └─→ http://127.0.0.1:20128/v1
    │       ├─→ kr/... → Kiro OAuth
    │       ├─→ clouvia/... → https://router.clouvia.id/v1 (sub-proxy)
    │       └─→ openrouter/... → https://openrouter.ai/v1 (sub-proxy)
```

**Sub-model Routing:** 9Router transparently routes prefix + model ID:
- `clouvia/coding-high` → Clouvia router with model "coding-high"
- `openrouter/deepseek/deepseek-chat` → OpenRouter with "deepseek/deepseek-chat"
- `kr/auto` → Kiro router with "auto" model

---

## Testing Summary

| Test | Command | Provider | Model | Result |
|------|---------|----------|-------|--------|
| Direct Clouvia | `hermes -z ...` | custom:clouvia | coding-high | ✓ "Siap" |
| Proxied Clouvia | `hermes -z ...` | custom:9router | clouvia/coding-high | ✓ "Aman" |
| Proxied OpenRouter | `hermes -z ...` | custom:9router | openrouter/deepseek/deepseek-chat | ✓ "mantap" |
| Model Picker | Desktop UI inspect | custom:9router | (all 616) | ✓ Loads all |

---

## Next Steps

### Phase 2: Failover & Routing Strategy (Pending Cal's Input)

1. **Determine Priority Order** based on Cal's plan tiers:
   - Primary: Kiro (if Pro tier) or Clouvia (if unlimited)?
   - Secondary: Failover to OpenRouter (free daily-limit) if primary exhausted?

2. **Create Combo (Virtual Router)** in 9Router:
   - Name: `auto-fallback` or `super-coder`
   - Chain: [Primary] → [Secondary] → [Emergency]
   - Test: Simulate primary rate-limit, verify auto-fallback

3. **Optional: Cost Monitoring Cron**
   - Track token/credit burn across all 3 providers
   - Alert if usage > threshold per day

---

## Files & Locations

| File | Purpose | Status |
|------|---------|--------|
| `/root/.hermes/.env` | API keys (Clouvia, OpenRouter, 9router) | ✓ Updated |
| `/root/.hermes/config.yaml` | Hermes provider config | ✓ Updated |
| `/root/.hermes/provider_models_cache.json` | Desktop model picker cache | ✓ Updated |
| `/root/.9router/db/data.sqlite` | 9router provider DB | ✓ Updated |
| `/root/ai-team/memo/provider-integration-status.md` | This doc | ✓ Created |

---

## Credentials Reference

All API keys are stored in `/root/.hermes/.env` and referenced via environment variables:
- `CLOUVIA_API_KEY` — Clouvia router key
- `OPENROUTER_API_KEY` — OpenRouter account key
- `NINEROUTER_API_KEY` — Local 9router authentication

**Security:** Keys are [REDACTED] in logs; never echoed in chat or git commits.

---

**Last Sync:** 2026-11-02 16:54 UTC  
**Session Owner:** EVE (Chief of Staff)  
**Push Status:** Pending (awaiting documentation completion)
