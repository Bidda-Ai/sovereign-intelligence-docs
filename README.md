# Bidda Sovereign Intelligence — Developer Documentation

> **Public documentation repository.** Integration guides, API reference, and SDK documentation for [bidda.com](https://bidda.com).

---

## What is Bidda?

Bidda is the world's first source-verified, cryptographically-signed regulatory compliance intelligence registry — built for autonomous AI agents and compliance teams.

**2,408 verified nodes. 29 active sovereign pillars. $0.01 per node. $0.49–$9.99 per pillar bundle.**

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

// 1. Discover all 2,408 nodes (free, no auth)
const index = await agent.discover();
console.log(`Found ${index.length} nodes`);

// 2. Unlock a single node — $0.01
const node = await agent.fetchNode('nist-csf-2-0-govern');
console.log(node.bluf);
console.log(node.deterministic_workflow);

// 3. Unlock a full pillar bundle (enterprise)
const pillar = await agent.fetchPillar('cybersecurity'); // $1.99
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

## Integration Examples

### LangChain Tool (Python)

Wrap Bidda as a LangChain tool so any LLM agent can query compliance nodes inline:

```python
from langchain.tools import tool
import requests

BIDDA_BASE = "https://bidda.com/api/v1"

@tool
def bidda_get_node(node_id: str, skyfire_token: str) -> dict:
    """Fetch a verified compliance node from the Bidda Sovereign Intelligence Forest."""
    # Free discovery first — check hash before paying
    discovery = requests.get(f"{BIDDA_BASE}/nodes/{node_id}.json").json()

    # Unlock full node
    vault = requests.get(
        f"{BIDDA_BASE}/vault/nodes/{node_id}.json",
        headers={"skyfire-pay-id": skyfire_token}
    )
    if vault.status_code == 200:
        return vault.json()
    return {"error": vault.status_code, "detail": vault.text}

@tool
def bidda_discover(category: str = "") -> list:
    """List all available Bidda compliance nodes, optionally filtered by category slug."""
    index = requests.get(f"{BIDDA_BASE}/nodes/index.json").json()
    if category:
        return [n for n in index if n.get("domain_slug") == category]
    return index
```

### Fetch with Auto-Retry (JavaScript)

Handles the 402 → pay → retry cycle automatically for Path A (Skyfire):

```javascript
async function fetchNode(nodeId, skyfireToken) {
  const vaultUrl = `https://bidda.com/api/v1/vault/nodes/${nodeId}.json`;

  const res = await fetch(vaultUrl, {
    headers: { 'skyfire-pay-id': skyfireToken }
  });

  if (res.status === 200) return res.json();

  if (res.status === 402) {
    const body = await res.json();
    // body.payment_instructions.skyfire.amount_usd tells you the price
    console.log(`Payment required: $${body.payment_instructions.skyfire.amount_usd}`);
    // With a funded Skyfire token, retry immediately — payment is pre-authorized
    const retry = await fetch(vaultUrl, {
      headers: { 'skyfire-pay-id': skyfireToken }
    });
    if (retry.status === 200) return retry.json();
  }

  throw new Error(`Bidda fetch failed: ${res.status}`);
}
```

### Compliance Workflow Example (Node.js)

Fetch a node and execute its `deterministic_workflow` step-by-step:

```javascript
import BiddaClient from 'bidda-agent-sdk';

const client = new BiddaClient({
  baseUrl: 'https://bidda.com',
  skyfireToken: process.env.SKYFIRE_TOKEN
});

async function runComplianceCheck(nodeId, context) {
  const node = await client.fetchNode(nodeId);

  console.log(`\n[BIDDA] Running: ${node.title}`);
  console.log(`[BIDDA] BLUF: ${node.bluf}\n`);

  for (const step of node.deterministic_workflow) {
    console.log(`Step ${step.step}: ${step.logic}`);
    // Apply step.logic to your context — deterministic, no LLM inference
  }

  // Check thresholds from actionable_schema
  const schema = node.actionable_schema;
  if (schema.breach_notification_window_hours) {
    console.log(`Breach window: ${schema.breach_notification_window_hours}h`);
  }

  // Check dependencies — load the full compliance chain
  for (const depId of node.dependencies) {
    const dep = await client.fetchNode(depId); // $0.01 each
    console.log(`  → Dependency: ${dep.title}`);
  }

  return node;
}

// Example: GDPR Article 33 breach notification
await runComplianceCheck('gdpr-article-33-breach-notification', {
  incidentDate: new Date(),
  affectedRecords: 50000
});
```

### Direct USDC Payment (ethers.js)

For Path C — send USDC on Base without an account:

```javascript
import { ethers } from 'ethers';

const USDC_CONTRACT = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const USDC_ABI = ['function transfer(address to, uint256 amount) returns (bool)'];
const NODE_ID = 'nist-csf-2-0-govern';

async function payAndFetch(privateKey) {
  // 1. Get payment instructions from 402 response
  const res402 = await fetch(`https://bidda.com/api/v1/vault/nodes/${NODE_ID}.json`);
  const { payment_instructions } = await res402.json(); // status 402
  const { destination, amount_usd } = payment_instructions.direct_base;
  const amountUnits = BigInt(Math.round(amount_usd * 1_000_000)); // USDC has 6 decimals

  // 2. Send USDC on Base
  const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
  const signer = new ethers.Wallet(privateKey, provider);
  const usdc = new ethers.Contract(USDC_CONTRACT, USDC_ABI, signer);
  const tx = await usdc.transfer(destination, amountUnits);
  const receipt = await tx.wait();

  // 3. Fetch node with tx hash proof
  const node = await fetch(`https://bidda.com/api/v1/vault/nodes/${NODE_ID}.json`, {
    headers: { 'x-base-tx-hash': receipt.hash }
  });
  return node.json();
}
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/v1/nodes/index.json` | GET | None | Discovery index — all 2,408 nodes, 6 fields each |
| `/api/v1/nodes/{nodeId}.json` | GET | None | Single node discovery record (free) |
| `/api/v1/vault/nodes/{nodeId}.json` | GET | Required | Full 13-key node — **$0.01** |
| `/api/v1/vault/pillar/{slug}.json` | GET | Required | Full pillar bundle — **$0.49–$9.99** |
| `/api/v1/vault/pillar/_all.json` | GET | Required | Full registry bundle — **$9.99** |
| `/api/v1/openapi-skyfire.json` | GET | None | OpenAPI 3.0 specification |
| `/.well-known/ai-plugin.json` | GET | None | AI plugin manifest (ChatGPT/Copilot compatible) |
| `/llms.txt` | GET | None | Machine-readable registry summary for LLM crawlers |
| `/llms-full.txt` | GET | None | Full node listing for LLM crawlers |

---

## Authentication

Three payment paths are accepted on vault endpoints — choose the one that fits your stack:

### Path A — Skyfire `pay+jwt` (primary for AI agents)

```
skyfire-pay-id: <pay+jwt token string>
```

Get a token at [app.skyfire.xyz](https://app.skyfire.xyz). The token authorizes payment from your Skyfire balance.

The `402` response body includes `amount_usd` for the endpoint you requested — set that amount in your token before retrying.

**Best for:** autonomous AI agents, enterprise integrations, orchestration platforms.

### Path B — L402 / USDC on Base (Web3 / MetaMask)

```
Authorization: L402 web3:MACAROON:0xTX_HASH
```

Send $0.01 USDC on Base network and include the transaction hash as payment proof. Works with any Web3 wallet (MetaMask, Coinbase Wallet, etc.).

**Note:** L402 is available for single-node endpoints only. Pillar bundles require Skyfire.

**Best for:** developers with existing Web3 wallets, crypto-native integrations.

### Path C — Direct Base USDC (LIVE)

```
x-base-tx-hash: 0xYOUR_TX_HASH
```

No account required, no third-party dependency. Send USDC directly on Base to our payment address, include the transaction hash in the `x-base-tx-hash` header, and receive the full node JSON immediately. The worker verifies the transfer on-chain and records the hash in a replay-prevention store — the same transaction hash cannot be reused.

**Payment details:**
- Network: Base (chain ID 8453)
- USDC contract: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Destination: see `payment_instructions.direct_base.destination` in the 402 response
- Single node: exactly `0.01 USDC` (or above — overpayment accepted)
- Pillar bundle prices: see the 402 response body for `amount_usd`

**Agent flow (no human in the loop):**
```
1. GET /api/v1/vault/nodes/{id}.json  →  402 response with payment_instructions
2. Read destination address and amount_usd from the 402 body
3. Send USDC on Base, capture tx hash
4. Retry: GET /api/v1/vault/nodes/{id}.json  +  x-base-tx-hash: 0x...
5. Receive full 13-key node JSON
```

**Best for:** headless agents without Skyfire accounts, crypto-native teams, jurisdictions where Skyfire is unavailable.

---

## Pricing

### Single Node

| Endpoint | Price | Auth |
|---|---|---|
| `/api/v1/vault/nodes/{id}.json` | **$0.01** | Skyfire or L402 |

The $0.01 price is fixed. Agents making 1,000 calls pay $10 total. No subscription. No account. No friction.

### Pillar Bundles

| Slug | Pillar | Nodes | Price |
|---|---|---|---|
| `crypto` | Crypto & Sovereign Finance | 53 | $0.49 |
| `food` | Food & Hospitality | 56 | $0.49 |
| `media` | Creative, Content & Media IP | 48 | $0.49 |
| `gaming` | Gaming & Gambling | 42 | $0.49 |
| `mining` | Mining & Natural Resources | 44 | $0.49 |
| `biotech` | Biotech & Genomics | 41 | $0.49 |
| `workflow` | Workflow Automation | 12 | $0.49 |
| `medical` | Medical & Healthcare | 103 | $0.99 |
| `aviation` | Aviation, Defense & Quantum | 72 | $0.99 |
| `esg` | Sustainability & ESG | 125 | $0.99 |
| `sales` | Sales, Marketing & PR | 52 | $0.99 |
| `logistics` | Logistics & Supply Chain | 81 | $0.99 |
| `cloud` | Cloud & SaaS | 71 | $0.99 |
| `industrial` | Industrial IoT & Energy | 42 | $0.99 |
| `operations` | Operations & CX | 59 | $0.99 |
| `workplace` | Workplace | 146 | $0.99 |
| `education` | Education & Research | 50 | $0.99 |
| `telecoms` | Telecoms & Digital Infrastructure | 38 | $0.99 |
| `energy` | Energy & Utilities | 53 | $0.99 |
| `construction` | Construction & Real Estate | 56 | $0.99 |
| `insurance` | Insurance & Risk | 56 | $0.99 |
| `competition` | Competition & Antitrust | 49 | $0.99 |
| `automotive` | Automotive & Mobility | 58 | $0.99 |
| `tax` | Tax & Transfer Pricing | 61 | $1.99 |
| `pharma` | Pharmaceuticals & Life Sciences | 57 | $1.99 |
| `ai-governance` | AI Governance & Law | 139 | $1.99 |
| `finance` | Banking & Global Finance | 232 | $1.99 |
| `legal` | Legal & IP Sovereignty | 231 | $1.99 |
| `cybersecurity` | Cybersecurity | 281 | $1.99 |
| `_all` | Full Registry (all 2,408 nodes) | 2,408 | **$9.99** |

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
      "header": "Authorization",
      "format": "L402 web3:MACAROON:0xTX_HASH",
      "network": "Base",
      "chain_id": 8453,
      "amount_usd": 0.01,
      "note": "L402 USDC path available for single-node endpoints only"
    },
    "direct_base": {
      "header": "x-base-tx-hash",
      "format": "0xYOUR_TX_HASH",
      "network": "Base",
      "chain_id": 8453,
      "amount_usd": 0.01,
      "note": "No account required — send USDC directly on Base, pass tx hash as header"
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

## 29 Active Sovereign Pillars

| Slug | Pillar | Nodes |
|---|---|---|
| `cybersecurity` | Cybersecurity | 281 |
| `finance` | Banking & Global Finance | 232 |
| `legal` | Legal & IP Sovereignty | 231 |
| `workplace` | Workplace | 146 |
| `ai-governance` | AI Governance & Law | 139 |
| `esg` | Sustainability & ESG | 125 |
| `medical` | Medical & Healthcare | 103 |
| `logistics` | Logistics & Supply Chain | 81 |
| `aviation` | Aviation, Defense & Quantum | 72 |
| `cloud` | Cloud & SaaS | 71 |
| `tax` | Tax & Transfer Pricing | 61 |
| `operations` | Operations & CX | 59 |
| `automotive` | Automotive & Mobility | 58 |
| `pharma` | Pharmaceuticals & Life Sciences | 57 |
| `food` | Food & Hospitality | 56 |
| `construction` | Construction & Real Estate | 56 |
| `insurance` | Insurance & Risk | 56 |
| `crypto` | Crypto & Sovereign Finance | 53 |
| `energy` | Energy & Utilities | 53 |
| `sales` | Sales, Marketing & PR | 52 |
| `education` | Education & Research | 50 |
| `competition` | Competition & Antitrust | 49 |
| `media` | Creative, Content & Media IP | 48 |
| `mining` | Mining & Natural Resources | 44 |
| `industrial` | Industrial IoT & Energy | 42 |
| `gaming` | Gaming & Gambling | 42 |
| `biotech` | Biotech & Genomics | 41 |
| `telecoms` | Telecoms & Digital Infrastructure | 38 |
| `workflow` | Workflow Automation | 12 |

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

## SDK Downloads

| File | Language | Description |
|---|---|---|
| `bidda-agent-sdk.js` | JavaScript / Node.js | Full SDK |
| `bidda_agent_sdk.py` | Python | Full SDK |

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

## Links

- Website: [bidda.com](https://bidda.com)
- Intelligence Forest: [bidda.com/intelligence](https://bidda.com/intelligence)
- Developer Portal: [bidda.com/developers](https://bidda.com/developers)
- Sovereign Insights: [bidda.com/insights](https://bidda.com/insights)
- OpenAPI Spec: [bidda.com/api/v1/openapi-skyfire.json](https://bidda.com/api/v1/openapi-skyfire.json)
- LLM Discovery: [bidda.com/llms.txt](https://bidda.com/llms.txt)
- Contact: info@bidda.com
