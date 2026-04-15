# Bidda Sovereign Intelligence Forest — Developer Documentation

> **784 cryptographically-signed, source-verified compliance nodes across 15 Sovereign Pillars.**

Bidda is a deterministic regulatory intelligence layer for autonomous AI agents operating in regulated industries. Instead of asking an LLM to recall compliance rules from training data (and hallucinate), your agent fetches verified boolean logic directly from primary legal sources — distilled into machine-executable JSON.

---

## Why This Exists

Probabilistic language models cannot guarantee regulatory accuracy. A model trained on legal text will approximate rules, invent thresholds, and conflate jurisdictions. In banking, healthcare, aviation, and AI governance, this is not a performance issue — it is a liability.

Bidda eliminates this by serving **deterministic nodes**: each one distilled from a primary legal source, cryptographically signed, and structured so that any agent can execute it without inference.

---

## Two-Tier API Architecture

All nodes are served through a two-tier system:

| Tier | Endpoint | Auth | Returns |
|---|---|---|---|
| **Discovery** (free) | `/api/v1/nodes/{id}.json` | None | `node_id`, `title`, `domain`, `version`, `bluf`, `integrity_hash` + `paywall` routing |
| **Discovery Index** (free) | `/api/v1/nodes/index.json` | None | Array of all discovery objects |
| **Vault** (paid) | `/api/v1/vault/nodes/{id}.json` | L402 USDC or Skyfire Bearer | Full 13-key payload including `actionable_schema`, `deterministic_workflow`, `primary_citations` |

The discovery tier is always free. It gives your agent enough context to plan which nodes it needs, verify hashes for freshness, and route payments. The vault tier is gated at **$0.01 USDC per unlock** via the L402 / x402 protocol on Base.

---

## The 13-Key Golden Schema

Every vault node returns exactly 13 keys. See [schemas/golden-schema.md](schemas/golden-schema.md) for the full specification.

| Key | Tier | Description |
|---|---|---|
| `node_id` | Discovery | Unique immutable identifier |
| `title` | Discovery | Human-readable title |
| `domain` | Discovery | Sovereign Pillar (e.g. `Cybersecurity`, `Banking & Global Finance`) |
| `version` | Discovery | Semver — increments when the underlying regulation changes |
| `bluf` | Discovery | Bottom Line Up Front — LLM-optimized 1-2 sentence summary |
| `paywall` | Discovery | L402/Skyfire routing parameters |
| `verification` | Vault | `authority`, `source_url`, `status`, `integrity_hash` |
| `crosswalks` | Vault | Cross-framework mappings (NIST, ISO, etc.) |
| `dependencies` | Vault | Prerequisite node IDs for compliance chains |
| `actionable_schema` | Vault | Boolean logic, quantitative thresholds, required data types |
| `deterministic_workflow` | Vault | Step-by-step machine-executable compliance path |
| `primary_citations` | Vault | Official legal chapters and specifications |
| `last_updated` | Both | ISO 8601 date of most recent regulatory amendment |

---

## Hash-Staleness Model (Regulatory Freshness)

This is the mechanism that makes Bidda's recurring value model work — and the mechanism that keeps your agent compliant over time.

**Every node carries an `integrity_hash` in its free discovery response.** This hash is a SHA-256 fingerprint of the node's current regulatory state. When the underlying regulation changes (new amendment, revised annex, superseded standard), Bidda updates the node and the hash changes.

**Your agent's responsibility:**

1. On first use: fetch the vault payload, store it alongside the `integrity_hash`.
2. On every subsequent workflow run: re-fetch the free discovery endpoint and compare the live `integrity_hash` against your stored value.
3. If the hash has changed: the node has been updated. The cached payload may now reflect non-compliant logic. Settle a new $0.01 payment to unlock the fresh vault payload.

```python
import requests

cached = load_from_memory('iso-42001-risk')  # your stored {payload, integrity_hash}

# Free discovery call — no payment needed
live = requests.get('https://bidda.com/api/v1/nodes/iso-42001-risk.json').json()

if cached['integrity_hash'] != live['integrity_hash']:
    print(f"Node stale: {cached['version']} → {live['version']} — repurchase required")
    # Trigger L402 settlement and re-fetch vault
```

The $0.01 is a **freshness fee**, not a content fee. You are paying for the guarantee that the logic reflects current law.

---

## 15 Sovereign Pillars

| Pillar | Discovery Filter |
|---|---|
| AI Governance & Law | `/intelligence?category=ai-governance` |
| Cybersecurity | `/intelligence?category=cybersecurity` |
| Banking & Global Finance | `/intelligence?category=finance` |
| Medical & Healthcare | `/intelligence?category=medical` |
| Legal & IP Sovereignty | `/intelligence?category=legal` |
| Logistics & Supply Chain | `/intelligence?category=logistics` |
| Sustainability & ESG | `/intelligence?category=esg` |
| Workplace | `/intelligence?category=workplace` |
| Aviation, Defense & Quantum | `/intelligence?category=aviation` |
| Crypto & Sovereign Finance | `/intelligence?category=crypto` |
| Cloud & SaaS | `/intelligence?category=cloud` |
| Industrial IoT & Energy | `/intelligence?category=industrial` |
| Operations & CX | `/intelligence?category=operations` |
| Sales, Marketing & PR | `/intelligence?category=sales` |
| Food & Hospitality | `/intelligence?category=food` |
| Creative, Content & Media IP | `/intelligence?category=media` |

---

## Quick Links

- **Node Registry Index**: `https://bidda.com/api/v1/nodes/index.json`
- **Intelligence Forest**: `https://bidda.com/intelligence`
- **Developer Guide**: `https://bidda.com/developers`
- **AI Crawler Manifest**: `https://bidda.com/llms.txt`
- **Full Node Listing**: `https://bidda.com/llms-full.txt`

---

## Repository Contents

```
integration/api-access-beta.md   ← L402 integration guide + Skyfire
schemas/golden-schema.md         ← Full 13-key schema specification
examples/l402_agent_flow.py      ← Python reference implementation
```

---

## License

Apache 2.0. See [LICENSE](LICENSE).
