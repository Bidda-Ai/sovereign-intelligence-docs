# Bidda Sovereign Intelligence — Developer Documentation

> **Public documentation repository.** Integration guides, API reference, and SDK documentation for [bidda.com](https://bidda.com).

---

## What is Bidda?

Bidda is the world's first source-verified, cryptographically-signed regulatory compliance intelligence registry — built for autonomous AI agents and compliance teams.

**2,995 verified nodes. 31 active sovereign pillars. $0.01 per node. $0.49–$49.99 per pillar bundle.**

Each Bidda node is a machine-readable JSON object distilled from primary legal sources (legislation, ISO standards, NIST frameworks, ICAO regulations, etc.) into deterministic, citable compliance logic. Zero inference. Zero hallucination. Every claim traceable to clause.

---

## MCP Server — Free Discovery

Bidda is live as an MCP server. Connect to Claude.ai, Claude Desktop, or any MCP-compatible AI tool and immediately query 2,995 compliance nodes with no account, no API key, no payment.

**Endpoint:** `https://bidda.com/mcp`

### Connect to Claude.ai

Settings → **Connectors** → **Add Connector** → paste `https://bidda.com/mcp`

### Connect to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bidda": {
      "command": "npx",
      "args": ["mcp-remote", "https://bidda.com/mcp"]
    }
  }
}
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_pillars` | List all 31 sovereign pillars with node counts and descriptions |
| `search_nodes` | Full-text search across 2,995 nodes — returns title, BLUF, domain |
| `get_node` | Fetch a single discovery record (node_id, title, domain, version, bluf, paywall) |

All MCP tools query the free discovery tier. Full node unlock ($0.01) goes through the Vault API.

**Listed on:** [smithery.ai](https://smithery.ai) · [mcp.so](https://mcp.so) · [glama.ai](https://glama.ai)

---

## Quick Start

### JavaScript / Node.js

```javascript
import BiddaClient from 'bidda-agent-sdk';
// or: import BiddaClient from './sdk/bidda-agent-sdk.js';

// Path A — Skyfire agent (primary path for AI agents)
const agent = new BiddaClient({
  baseUrl: 'https://bidda.com',
  skyfireToken: 'YOUR_SKYFIRE_PAY_JWT'
});

// 1. Discover all 2,995 nodes (free, no auth)
const index = await agent.discover();
console.log(`Found ${index.length} nodes`);

// 2. Unlock a single node — $0.01
const node = await agent.fetchNode('nist-csf-2-0-govern-function');
console.log(node.bluf);
console.log(node.deterministic_workflow);

// 3. Unlock a full pillar bundle
const pillar = await agent.fetchPillar('cybersecurity'); // $2.99
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

node = agent.fetch_node('eu-ai-act-high-risk-systems')
print(node['bluf'])

pillar = agent.fetch_pillar('ai-governance')  # $2.49
print(f"{pillar['node_count']} nodes in AI Governance bundle")
```

### curl

```bash
# Discover all nodes (free)
curl https://bidda.com/api/v1/nodes/index.json

# Discover a single node (free)
curl https://bidda.com/api/v1/nodes/nist-csf-2-0-govern-function.json

# Unlock a node — Path A: Skyfire
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern-function.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Unlock a node — Path B: Direct Base USDC (no account required)
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern-function.json \
  -H "x-base-tx-hash: 0xYOUR_BASE_TX_HASH"

# Unlock a node — Path C: L402 / MetaMask
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern-function.json \
  -H "Authorization: L402 web3:token:0xYourBaseTxHash"

# Unlock a pillar bundle via Skyfire
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
    """Fetch a verified compliance node from the Bidda registry."""
    discovery = requests.get(f"{BIDDA_BASE}/nodes/{node_id}.json").json()

    vault = requests.get(
        f"{BIDDA_BASE}/vault/nodes/{node_id}.json",
        headers={"skyfire-pay-id": skyfire_token}
    )
    if vault.status_code == 200:
        return vault.json()
    return {"error": vault.status_code, "detail": vault.text}

@tool
def bidda_discover(domain: str = "") -> list:
    """List all available Bidda compliance nodes, optionally filtered by domain."""
    index = requests.get(f"{BIDDA_BASE}/nodes/index.json").json()
    if domain:
        return [n for n in index if n.get("domain") == domain]
    return index
```

### Compliance Workflow Executor (Node.js)

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
    console.log(`Step ${step.step}: ${step.action}`);
    if (step.condition) console.log(`  Condition: ${step.condition}`);
  }

  // Check thresholds from actionable_schema
  const schema = node.actionable_schema;
  if (schema.breach_notification_window_hours) {
    console.log(`Breach window: ${schema.breach_notification_window_hours}h`);
  }

  // Load the full compliance dependency chain
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

### Node Freshness Check (drift detection)

Each node carries a SHA-256 `integrity_hash` in its `verification` object. Check free discovery before paying to detect updates:

```javascript
// 1. Free discovery — compare hash against your cached version
const live = await fetch('https://bidda.com/api/v1/nodes/nist-csf-2-0-govern-function.json');
const { verification } = await live.json();

// 2. Only pay if the regulation has changed
if (cached.integrity_hash !== verification.integrity_hash) {
  const fresh = await agent.fetchNode('nist-csf-2-0-govern-function');
  cache.set('nist-csf-2-0-govern-function', fresh);
}
```

### Direct USDC Payment — Path B (ethers.js)

Send USDC on Base without any account — ideal for headless agents:

```javascript
import { ethers } from 'ethers';

const USDC_CONTRACT = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const USDC_ABI = ['function transfer(address to, uint256 amount) returns (bool)'];
const NODE_ID = 'nist-csf-2-0-govern-function';

// Treasury address — send exactly 10000 units ($0.01, 6 decimals)
const TREASURY = '0xD5eF3584bFa5D0ECE885A1101d00E431D3b6654A';

async function payAndFetch(privateKey) {
  const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
  const signer = new ethers.Wallet(privateKey, provider);
  const usdc = new ethers.Contract(USDC_CONTRACT, USDC_ABI, signer);

  // Send $0.01 USDC on Base (10000 units at 6 decimals)
  const tx = await usdc.transfer(TREASURY, 10000n);
  const receipt = await tx.wait();

  // Unlock node using tx hash as proof
  const node = await fetch(`https://bidda.com/api/v1/vault/nodes/${NODE_ID}.json`, {
    headers: { 'x-base-tx-hash': receipt.hash }
  });
  return node.json();
}
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/nodes/index.json` | GET | None | Discovery index — all 2,995 nodes, 6 fields each |
| `/api/v1/nodes/{nodeId}.json` | GET | None | Single node discovery record (free) |
| `/api/v1/vault/nodes/{nodeId}.json` | GET | Required | Full 13-key node — **$0.01** |
| `/api/v1/vault/pillar/{slug}.json` | GET | Required | Full pillar bundle — **$0.49–$49.99** |
| `/mcp` | GET/POST | None | MCP server — free discovery for AI tools |
| `/api/v1/openapi-skyfire.json` | GET | None | OpenAPI 3.0 specification |
| `/.well-known/mcp.json` | GET | None | MCP discovery manifest |
| `/.well-known/ai-plugin.json` | GET | None | AI plugin manifest (ChatGPT/Copilot compatible) |
| `/llms.txt` | GET | None | Machine-readable registry summary for LLM crawlers |
| `/llms-full.txt` | GET | None | Full node listing for LLM crawlers |

---

## Authentication — Three Payment Paths

### Path A — Skyfire `pay+jwt` (primary for AI agents)

```
skyfire-pay-id: <pay+jwt token string>
```

Get a token at [app.skyfire.xyz](https://app.skyfire.xyz). The token authorises payment from your Skyfire balance. The `402` response includes `amount_usd` for the endpoint requested — set that amount in your token configuration before retrying.

**Best for:** autonomous AI agents, enterprise integrations, orchestration platforms.

### Path B — Direct Base USDC (headless, no account required)

```
x-base-tx-hash: 0xYOUR_TX_HASH
```

Send exactly $0.01 USDC on Base, then pass the transaction hash as payment proof. No account, no third-party dependency — works headlessly from any language.

| Constant | Value |
|----------|-------|
| Receiver | `0xD5eF3584bFa5D0ECE885A1101d00E431D3b6654A` |
| USDC contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Amount | `10000` (= $0.01, 6 decimals — exact) |
| Chain ID | `8453` (Base mainnet) |

Each tx hash is single-use (replay protection active). Wait 30 seconds after sending for Base indexing before retrying.

**Best for:** headless agents, crypto-native teams, jurisdictions where Skyfire is unavailable.

### Path C — L402 / USDC on Base (Web3 / MetaMask)

```
Authorization: L402 web3:MACAROON:0xTX_HASH
```

Send $0.01 USDC on Base via MetaMask or any Web3 wallet, include the transaction hash. L402 is available for single-node endpoints only — pillar bundles require Path A (Skyfire).

**Best for:** developers with existing Web3 wallets.

---

## Pricing

### Single Node — $0.01

Fixed price. An agent making 1,000 node calls pays $10 total. No subscription, no account, no friction.

### Pillar Bundles

| Slug | Pillar | Nodes | Price |
|------|--------|-------|-------|
| `workflow` | Workflow Automation | 25 | $0.49 |
| `gaming` | Gaming & Gambling | 56 | $0.99 |
| `biotech` | Biotech & Genomics | 41 | $0.99 |
| `mining` | Mining & Natural Resources | 53 | $0.99 |
| `space` | Space & Aerospace Technology | 38 | $0.99 |
| `maritime` | Maritime & Shipping | 51 | $0.99 |
| `industrial` | Industrial IoT & Energy | 51 | $0.99 |
| `food` | Food & Hospitality | 93 | $0.99 |
| `media` | Creative, Content & Media IP | 83 | $0.99 |
| `crypto` | Crypto & Sovereign Finance | 75 | $0.99 |
| `operations` | Operations & CX | 60 | $0.99 |
| `competition` | Competition & Antitrust | 57 | $0.99 |
| `automotive` | Automotive & Mobility | 64 | $0.99 |
| `education` | Education & Research | 56 | $0.99 |
| `telecoms` | Telecoms & Digital Infrastructure | 74 | $0.99 |
| `tax` | Tax & Transfer Pricing | 75 | $0.99 |
| `pharma` | Pharmaceuticals & Life Sciences | 64 | $0.99 |
| `insurance` | Insurance & Risk | 87 | $0.99 |
| `construction` | Construction & Real Estate | 57 | $0.99 |
| `energy` | Energy & Utilities | 56 | $0.99 |
| `sales` | Sales, Marketing & PR | 84 | $0.99 |
| `aviation` | Aviation, Defense & Quantum | 98 | $1.49 |
| `medical` | Medical & Healthcare | 106 | $1.49 |
| `esg` | Sustainability & ESG | 145 | $1.49 |
| `logistics` | Logistics & Supply Chain | 89 | $1.49 |
| `cloud` | Cloud & SaaS | 93 | $1.49 |
| `workplace` | Workplace | 152 | $1.99 |
| `ai-governance` | AI Governance & Law | 142 | $2.49 |
| `finance` | Banking & Global Finance | 326 | $2.99 |
| `legal` | Legal & IP Sovereignty | 261 | $2.99 |
| `cybersecurity` | Cybersecurity | 283 | $2.99 |
| `_all` | Full Registry (all 2,995 nodes) | 2,995 | $49.99 |

---

## 402 Payment Required — Response Format

```json
{
  "error": "402 Payment Required",
  "message": "No payment token provided.",
  "payment_instructions": {
    "skyfire": {
      "header": "skyfire-pay-id",
      "service_id": "41779894-ece2-4163-9761-b3b1b76e19b0",
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
      "note": "L402 single-node only. Pass tx hash as x-base-tx-hash header."
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
  "node_id": "nist-csf-2-0-govern-function",
  "title": "NIST Cybersecurity Framework 2.0 — GOVERN Function",
  "domain": "Cybersecurity",
  "version": "1.0.0",
  "last_updated": "2026-04-01",
  "bluf": "Dense executive summary — what the regulation requires and why it matters.",
  "paywall": {
    "status": "gated",
    "unlock_cost_usd": "0.01",
    "skyfire_id": "41779894-ece2-4163-9761-b3b1b76e19b0"
  },
  "verification": {
    "authority": "NIST",
    "source_url": "https://www.nist.gov/cyberframework",
    "audit_timestamp": "2026-04-01T00:00:00Z",
    "integrity_hash": "sha256:...",
    "status": "VERIFIED"
  },
  "crosswalks": {
    "iso_27001": "A.5.1 — Information security policies",
    "nist_framework": "GV.OC — Organizational context"
  },
  "dependencies": ["nist-sp-800-53-r5", "iso-27001-2022"],
  "actionable_schema": {
    "risk_threshold_score": 0.85,
    "mandatory_review_cadence": "annual",
    "breach_notification_window_hours": 72
  },
  "deterministic_workflow": [
    {
      "step": 1,
      "condition": "organizational_context_defined == false",
      "action": "Establish and document the organizational context per GV.OC-01.",
      "fallback": "Engage executive leadership to define and approve context statement."
    }
  ],
  "primary_citations": [
    "NIST Cybersecurity Framework 2.0, GOVERN Function (GV), February 2024"
  ]
}
```

---

## 31 Active Sovereign Pillars

| Slug | Pillar | Nodes |
|------|--------|-------|
| `cybersecurity` | Cybersecurity | 283 |
| `finance` | Banking & Global Finance | 326 |
| `legal` | Legal & IP Sovereignty | 261 |
| `workplace` | Workplace | 152 |
| `esg` | Sustainability & ESG | 145 |
| `ai-governance` | AI Governance & Law | 142 |
| `medical` | Medical & Healthcare | 106 |
| `cloud` | Cloud & SaaS | 93 |
| `logistics` | Logistics & Supply Chain | 89 |
| `insurance` | Insurance & Risk | 87 |
| `sales` | Sales, Marketing & PR | 84 |
| `media` | Creative, Content & Media IP | 83 |
| `aviation` | Aviation, Defense & Quantum | 98 |
| `food` | Food & Hospitality | 93 |
| `tax` | Tax & Transfer Pricing | 75 |
| `crypto` | Crypto & Sovereign Finance | 75 |
| `telecoms` | Telecoms & Digital Infrastructure | 74 |
| `automotive` | Automotive & Mobility | 64 |
| `pharma` | Pharmaceuticals & Life Sciences | 64 |
| `operations` | Operations & CX | 60 |
| `competition` | Competition & Antitrust | 57 |
| `construction` | Construction & Real Estate | 57 |
| `gaming` | Gaming & Gambling | 56 |
| `education` | Education & Research | 56 |
| `energy` | Energy & Utilities | 56 |
| `industrial` | Industrial IoT & Energy | 51 |
| `maritime` | Maritime & Shipping | 51 |
| `mining` | Mining & Natural Resources | 53 |
| `space` | Space & Aerospace Technology | 38 |
| `biotech` | Biotech & Genomics | 41 |
| `workflow` | Workflow Automation | 25 |

---

## SDK Downloads

| File | Language | Description |
|------|----------|-------------|
| `bidda-agent-sdk.js` | JavaScript / Node.js | SDK v2.1.0 — all three payment paths |
| `bidda_agent_sdk.py` | Python | SDK v2.1.0 — all three payment paths |

Download ZIP: `https://bidda.com/sdk/bidda-sdk.zip`  
Download page: `https://bidda.com/sdk/`

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

MCP discovery manifest:

```
https://bidda.com/.well-known/mcp.json
```

---

## Links

- Website: [bidda.com](https://bidda.com)
- Intelligence Forest: [bidda.com/intelligence](https://bidda.com/intelligence)
- Developer Portal: [bidda.com/developers](https://bidda.com/developers)
- MCP Server: [bidda.com/mcp](https://bidda.com/mcp)
- OpenAPI Spec: [bidda.com/api/v1/openapi-skyfire.json](https://bidda.com/api/v1/openapi-skyfire.json)
- LLM Discovery: [bidda.com/llms.txt](https://bidda.com/llms.txt)
- Contact: info@bidda.com
