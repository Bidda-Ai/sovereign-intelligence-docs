# Bidda Sovereign Intelligence — Developer Documentation

> **Public documentation repository.** Integration guides, API reference, and SDK documentation for [bidda.com](https://bidda.com).

---

## What is Bidda?

Bidda is the world's first source-verified, cryptographically-signed regulatory compliance intelligence registry — built for autonomous AI agents and compliance teams.

**995 verified nodes. 16 regulatory pillars. $0.01 per node. $0.49–$9.99 per pillar bundle.**

Each Bidda node is a machine-readable JSON object distilled from primary legal sources (legislation, ISO standards, NIST frameworks, ICAO regulations, etc.) into deterministic, citable compliance logic. Zero inference. Zero hallucination. Every claim traceable to clause.

---

## Quick Start

### JavaScript / Node.js

```javascript
import BiddaClient from 'bidda-agent-sdk';
// or: import BiddaClient from './sdk/bidda-agent-sdk.js';

// Skyfire agent (primary path for AI agents)
const agent = new BiddaClient({
  baseUrl: 'https://bidda.com',
  skyfireToken: 'YOUR_SKYFIRE_PAY_JWT'
});

// 1. Discover all 995 nodes (free, no auth)
const index = await agent.discover();
console.log(`Found ${index.length} nodes`);

// 2. Unlock a single node — $0.01
const node = await agent.fetchNode('nist-csf-2-0-govern');
console.log(node.bluf);
console.log(node.deterministic_workflow);

// 3. Unlock a full pillar bundle (enterprise)
const pillar = await agent.fetchPillar('cybersecurity'); // $0.99
console.log(`${pillar.node_count} nodes in Cybersecurity bundle`);
```

### Python

```python
from bidda_agent_sdk import BiddaClient

agent = BiddaClient(
    base_url='https://bidda.com',
    skyfire_token='YOUR_SKYFIRE_PAY_JWT'
)

nodes = agent.discover()
print(f"Found {len(nodes)} nodes")

node = agent.fetch_node('eu-ai-act-high-risk')
print(node['bluf'])

pillar = agent.fetch_pillar('ai-governance')  # $1.99
print(f"{pillar['node_count']} nodes in AI Governance bundle")
```

### curl

```bash
# Discover all nodes (free)
curl https://bidda.com/api/v1/nodes/index.json

# Discover a single node (free)
curl https://bidda.com/api/v1/nodes/nist-csf-2-0-govern.json

# Unlock a node via Skyfire (AI agents — primary path)
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Unlock a node via L402 / USDC on Base (Web3 fallback)
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern.json \
  -H "Authorization: L402 web3:token:0xYourBaseTxHash"

# Unlock a full pillar bundle via Skyfire
curl https://bidda.com/api/v1/vault/pillar/cybersecurity.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/v1/nodes/index.json` | GET | None | Discovery index — all 995 nodes, 6 fields each |
| `/api/v1/nodes/{nodeId}.json` | GET | None | Single node discovery record (free) |
| `/api/v1/vault/nodes/{nodeId}.json` | GET | Required | Full 13-key node — **$0.01** |
| `/api/v1/vault/pillar/{slug}.json` | GET | Required | Full pillar bundle — **$0.49–$9.99** |
| `/api/v1/openapi-skyfire.json` | GET | None | OpenAPI 3.0 specification |
| `/.well-known/ai-plugin.json` | GET | None | AI plugin manifest (ChatGPT/Copilot compatible) |
| `/llms.txt` | GET | None | Machine-readable registry summary for LLM crawlers |
| `/llms-full.txt` | GET | None | Full node listing for LLM crawlers |

---

## Authentication

Two payment paths are accepted on vault endpoints:

### Path A — Skyfire `pay+jwt` (primary for AI agents)

```
skyfire-pay-id: <pay+jwt token string>
```

Get a token at [app.skyfire.xyz](https://app.skyfire.xyz). The token authorizes payment from your Skyfire balance.

The `402` response body includes `amount_usd` for the endpoint you requested — set that amount in your token before retrying.

### Path B — L402 / USDC on Base (Web3 / MetaMask)

```
Authorization: L402 web3:MACAROON:0xTX_HASH
```

Send $0.01 USDC on Base network and use the transaction hash as payment proof.

**Note:** L402 is available for single-node endpoints only. Pillar bundles require Skyfire.

---

## Pricing

### Single Node

| Endpoint | Price | Auth |
|---|---|---|
| `/api/v1/vault/nodes/{id}.json` | $0.01 | Skyfire or L402 |

### Pillar Bundles

| Slug | Pillar | Price |
|---|---|---|
| `crypto` | Crypto & Sovereign Finance | $0.49 |
| `food` | Food & Hospitality | $0.49 |
| `media` | Creative, Content & Media IP | $0.49 |
| `workplace` | Workplace | $0.49 |
| `operations` | Operations & CX | $0.49 |
| `medical` | Medical & Healthcare | $0.99 |
| `aviation` | Aviation, Defense & Quantum | $0.99 |
| `esg` | Sustainability & ESG | $0.99 |
| `sales` | Sales, Marketing & PR | $0.99 |
| `logistics` | Logistics & Supply Chain | $0.99 |
| `cloud` | Cloud & SaaS | $0.99 |
| `industrial` | Industrial IoT & Energy | $0.99 |
| `ai-governance` | AI Governance & Law | $1.99 |
| `finance` | Banking & Global Finance | $1.99 |
| `legal` | Legal & IP Sovereignty | $1.99 |
| `cybersecurity` | Cybersecurity | $1.99 |
| `_all` | Full Registry (all 995 nodes) | $9.99 |

---

## 402 Payment Required — Response Format

When no token is provided:

```json
{
  "error": "402 Payment Required",
  "message": "No payment token provided.",
  "payment_instructions": {
    "skyfire": {
      "header": "skyfire-pay-id",
      "token_types_accepted": ["pay", "kya-pay"],
      "amount_usd": 0.01,
      "docs": "https://docs.skyfire.xyz"
    },
    "l402": {
      "network": "Base",
      "chain_id": 8453,
      "amount_usd": 0.01,
      "note": "L402 USDC path available for single-node endpoints only"
    }
  }
}
```

`amount_usd` reflects the correct price for the endpoint requested (higher for pillar bundles).

---

## Node JSON Structure (13-key schema)

**Discovery tier** (free) returns: `node_id`, `title`, `domain`, `version`, `bluf`, `paywall`

**Vault tier** (paid) returns all 13 keys:

```json
{
  "node_id": "nist-csf-2-0-govern",
  "title": "NIST Cybersecurity Framework 2.0 — GOVERN",
  "domain": "Cybersecurity",
  "version": "1.0.0",
  "last_updated": "2026-04-01",
  "bluf": "Dense executive summary — what the regulation requires and why it matters.",
  "paywall": {
    "status": "gated",
    "unlock_cost_usd": "0.01"
  },
  "verification": {
    "authority": "Bidda Sovereign Trust",
    "source_url": "https://www.nist.gov/cyberframework",
    "audit_timestamp": "2026-04-01T00:00:00Z",
    "integrity_hash": "sha256:...",
    "status": "VERIFIED"
  },
  "crosswalks": {
    "iso_27001": "A.5.1 — Information security policies"
  },
  "dependencies": ["nist-sp-800-53-r5", "iso-27001-2022"],
  "actionable_schema": {
    "risk_threshold_score": 0.85,
    "mandatory_review_cadence": "annual",
    "breach_notification_window_hours": 72
  },
  "deterministic_workflow": [
    { "step": 1, "logic": "Establish and maintain an asset inventory covering all hardware, software, and data assets in scope." }
  ],
  "primary_citations": [
    "NIST Cybersecurity Framework 2.0, GOVERN Function (GV), February 2024"
  ]
}
```

---

## 16 Sovereign Pillars

| Slug | Pillar | Node Count |
|---|---|---|
| `ai-governance` | AI Governance & Law | 77 |
| `cybersecurity` | Cybersecurity | 216 |
| `finance` | Banking & Global Finance | 113 |
| `legal` | Legal & IP Sovereignty | 122 |
| `medical` | Medical & Healthcare | 46 |
| `logistics` | Logistics & Supply Chain | 59 |
| `esg` | Sustainability & ESG | 52 |
| `workplace` | Workplace | 49 |
| `aviation` | Aviation, Defense & Quantum | 45 |
| `crypto` | Crypto & Sovereign Finance | 22 |
| `cloud` | Cloud & SaaS | 55 |
| `industrial` | Industrial IoT & Energy | 8 |
| `operations` | Operations & CX | 25 |
| `sales` | Sales, Marketing & PR | 38 |
| `food` | Food & Hospitality | 35 |
| `media` | Creative, Content & Media IP | 33 |

---

## SDK Downloads

| File | Language | Description |
|---|---|---|
| `bidda-agent-sdk.js` | JavaScript / Node.js | Full SDK v2.0.0 |
| `bidda_agent_sdk.py` | Python | Full SDK v2.0.0 |

Download from: `https://bidda.com/sdk/`

---

## OpenAPI Specification

Machine-readable API spec for Skyfire, ChatGPT plugins, and agent frameworks:

```
https://bidda.com/api/v1/openapi-skyfire.json
```

AI plugin manifest (ChatGPT / Copilot / agent discovery):

```
https://bidda.com/.well-known/ai-plugin.json
```

---

## Node Freshness & Drift Detection

Every node carries a `version` string and a SHA-256 `integrity_hash` in its `verification` object. These are updated when the underlying regulation changes.

**Agent-side drift check (pseudocode):**

```javascript
// 1. Free discovery call — check the live hash
const live = await fetch('https://bidda.com/api/v1/nodes/nist-csf-2-0-govern.json');
const { verification } = await live.json();

// 2. Compare against your cached hash
if (cached.integrity_hash !== verification.integrity_hash) {
  // Regulation updated — re-unlock for $0.01
  const fresh = await agent.fetchNode('nist-csf-2-0-govern');
  cache.set('nist-csf-2-0-govern', fresh);
}
```

The hash check eliminates the risk of executing against an outdated legal framework in regulated workflows.

---

## Links

- Website: [bidda.com](https://bidda.com)
- Intelligence Forest: [bidda.com/intelligence](https://bidda.com/intelligence)
- Developer Docs: [bidda.com/developer](https://bidda.com/developer)
- OpenAPI Spec: [bidda.com/api/v1/openapi-skyfire.json](https://bidda.com/api/v1/openapi-skyfire.json)
- LLM Discovery: [bidda.com/llms.txt](https://bidda.com/llms.txt)
- Contact: info@bidda.com
