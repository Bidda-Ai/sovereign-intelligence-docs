# Bidda Sovereign Intelligence — Developer Documentation

> **Public documentation repository.** Integration guides, API reference, and SDK documentation for [bidda.com](https://bidda.com).

---

## What is Bidda?

Bidda is the world's first source-verified, cryptographically-signed regulatory compliance intelligence registry — built for autonomous AI agents and compliance teams.

**7,243 verified nodes. 34 active sovereign pillars. $0.01 per node. $5–$49 per pillar bundle.**

Each Bidda node is a machine-readable JSON object distilled from primary legal sources (legislation, ISO standards, NIST frameworks, ICAO regulations, etc.) into deterministic, citable compliance logic. Zero inference. Zero hallucination. Every claim traceable to clause.

Every vault unlock returns a **compliance receipt** — a cryptographic record of what intelligence your agent consulted, when, and which version of the law was in force. Suitable for regulatory audit submissions.

### Source-grounded by design

New nodes are generated against the **verbatim official text** of the underlying instrument — fetched directly from regulator corpora (EUR-Lex, US eCFR, legislation.gov.uk, NIST OSCAL, MITRE ATT&CK/ATLAS, OFAC SDN). Every citation in a node is then forensically checked against that source text before the node enters the registry: structural references (Article N, Section N, Part N, CFR §, USC §) must appear verbatim in the source or the node is rejected.

That's why a Bidda node citing "GDPR Article 33" is genuinely about Article 33 — not a model's confident-sounding paraphrase of what Article 33 *might* say.

---

## Quick Start

### JavaScript / Node.js

```javascript
// Skyfire agent (primary path for AI agents)
const vaultUrl = 'https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern.json';

const res = await fetch(vaultUrl, {
  headers: { 'skyfire-pay-id': 'YOUR_SKYFIRE_PAY_JWT' }
});

const node = await res.json();
console.log(node.bluf);
console.log(node.deterministic_workflow);

// The _receipt block is always included on vault responses
console.log(node._receipt.statement); // → audit-ready string
```

### Python

```python
import requests

vault_url = 'https://bidda.com/api/v1/vault/nodes/eu-gdpr-article-33.json'

res = requests.get(vault_url, headers={'skyfire-pay-id': 'YOUR_SKYFIRE_PAY_JWT'})
node = res.json()

print(node['bluf'])
print(node['_receipt']['integrity_hash'])   # SHA-256 of node content at access time
print(node['_receipt']['accessed_at'])      # ISO 8601 timestamp
print(node['_receipt']['txid'])             # On-chain payment proof
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

# Unlock a node via Direct Base USDC
curl https://bidda.com/api/v1/vault/nodes/nist-csf-2-0-govern.json \
  -H "x-base-tx-hash: 0xYourBaseTxHash"

# Unlock a full pillar bundle
curl https://bidda.com/api/v1/vault/pillar/cybersecurity.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Unlock multiple pillars in one call (sum pricing)
curl "https://bidda.com/api/v1/vault/bundle?pillars=finance,crypto,legal" \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"
```

---

## Compliance Receipts & Audit Trail

Every vault unlock — single node, pillar bundle, or multi-pillar bundle — returns a `_receipt` block appended to the JSON response. This is your audit record.

### Receipt structure

```json
{
  "_receipt": {
    "node_id":        "eu-gdpr-article-33",
    "version":        "2.1.3",
    "integrity_hash": "sha256:a3f9c2e1b4d8f7a6...",
    "accessed_at":    "2026-05-01T09:32:14.000Z",
    "txid":           "0x7a3b8f1c2d4e5f6a...",
    "amount_usd":     "0.01",
    "currency":       "USDC/Base",
    "registry":       "Bidda Sovereign Intelligence",
    "statement":      "Access to eu-gdpr-article-33 v2.1.3 verified at 2026-05-01T09:32:14.000Z. Integrity hash sha256:a3f9... recorded at time of access."
  }
}
```

### What each field proves

| Field | What it establishes |
|---|---|
| `node_id` | Which regulation your agent consulted |
| `version` | Which version of that regulation (laws change — the version matters) |
| `integrity_hash` | The content was not tampered with — matches the signed registry hash |
| `accessed_at` | Exact ISO 8601 timestamp of the consultation |
| `txid` | On-chain payment proof — immutable record on the Base blockchain |
| `amount_usd` | Confirms a real transaction occurred |
| `statement` | Human-readable audit string — paste directly into audit documentation |

### Why this matters for compliance teams

Regulators increasingly require organisations to document what AI systems were acting on when making compliance decisions. The `_receipt` block answers:

- *What did your AI consult?* → `node_id` + `version`
- *Was it authentic?* → `integrity_hash` verifiable against `https://bidda.com/api/v1/registry-health.json`
- *When?* → `accessed_at`
- *Can you prove it?* → `txid` on Base blockchain, publicly verifiable

**Recommended practice:** Store the full `_receipt` object in your compliance audit log alongside the action your agent took. The `statement` field is formatted for direct inclusion in audit submissions.

### Source integrity chain

Beyond the receipt, every Bidda source URL is fingerprinted weekly:
- **TLS SPKI hash** — detects certificate substitution and DNS hijacking
- **SHA-256 content hash** — detects silent regulatory content changes
- Committed to git — every weekly check creates a new commit, forming a Merkle-anchored audit trail
- Public endpoint: `GET https://bidda.com/api/v1/registry-health.json`

This means you can verify not just what your agent was told, but that the underlying source document hasn't changed since Bidda last verified it.

### Source coverage

Nodes are derived from official regulator corpora. Current corpus stack:

| Jurisdiction / Source | Coverage |
|---|---|
| **EUR-Lex (EU)** | 57,702 indexed instruments (Regulations, Directives, Decisions); 43,610 with English HTML available for verbatim grounding |
| **US Code of Federal Regulations** | 1,453 Parts across Titles 12 (Banks), 14 (Aeronautics/FAA), 17 (Securities), 21 (Food and Drugs/FDA), 45 (Public Welfare/HIPAA) — 22,913 sections |
| **UK Public General Acts** | Data Protection Act 2018, Financial Services and Markets Act 2000, Equality Act 2010, and selected statutory instruments |
| **NIST OSCAL** | 2,643 controls across SP 800-53 rev4 + rev5, CSF v2.0, SP 800-171 rev3, SP 800-172 rev3, SP 800-218 (SSDF) |
| **MITRE ATT&CK + ATLAS** | 1,510 adversarial-technique IDs across Enterprise, Mobile, ICS, Pre, and AI/ML |
| **OFAC sanctions programs** | 74 active sanctions programs covering 18,959 designated entities across 145+ countries |
| **International standards** | ISO/IEC, IEEE, IEC, Basel, IOSCO, FATF, IAIS, ICAO, IMO, IAEA, OECD, WIPO, WHO, FSB, BCBS, and others |
| **National authorities** | 80+ jurisdictions: US (SEC/CFTC/FDA/FRB/OCC/FDIC/CFPB/EPA/DOJ/FTC/HHS/DOD/DOL/FERC), UK (FCA/PRA/ICO), Singapore (PDPC/MAS/IMDA), Korea (PIPC/FSC), Japan (PPC/FSA), Australia (APRA/AUSTRAC/OAIC), Canada (OPC/OSFI), South Africa (FSCA/SARB), India (MeitY/SEBI/RBI), Brazil (ANPD/BCB), UAE (SCA/DIFC), and many more |

Coverage is updated continuously. The corpus indexes themselves are the asset that lets a Bidda node cite "21 CFR Part 11" and have it actually be 21 CFR Part 11.

### Version history

Every amendment to a node increments its version (`1.0.3 → 1.0.4`). Version history is preserved — you can demonstrate which version of GDPR Article 33 your agent was operating under in Q1 2025 versus Q2 2026.

**Enterprise:** Multi-node chain attestation, signed PDF export, and W3C Verifiable Credential export are available on the Enterprise plan. Contact info@bidda.com.

---

## Integration Examples

### LangChain Tool (Python)

```python
from langchain.tools import tool
import requests

BIDDA_BASE = "https://bidda.com/api/v1"

@tool
def bidda_get_node(node_id: str, skyfire_token: str) -> dict:
    """Fetch a verified compliance node from the Bidda Sovereign Intelligence registry."""
    vault = requests.get(
        f"{BIDDA_BASE}/vault/nodes/{node_id}.json",
        headers={"skyfire-pay-id": skyfire_token}
    )
    if vault.status_code == 200:
        node = vault.json()
        # Store receipt for audit trail
        audit_log.append(node.get("_receipt"))
        return node
    return {"error": vault.status_code, "detail": vault.text}
```

### Compliance Workflow with Audit Trail (Node.js)

```javascript
async function runComplianceCheck(nodeId, skyfireToken) {
  const res = await fetch(
    `https://bidda.com/api/v1/vault/nodes/${nodeId}.json`,
    { headers: { 'skyfire-pay-id': skyfireToken } }
  );

  const node = await res.json();

  // Save receipt to your audit log
  await auditLog.record({
    action:   'compliance_node_consulted',
    receipt:  node._receipt,   // full cryptographic record
    agent_id: 'my-agent-v2',
  });

  // Execute deterministic workflow
  for (const step of node.deterministic_workflow) {
    console.log(`Step ${step.step}: ${step.logic}`);
  }

  // Load full compliance chain (each dep also returns a receipt)
  for (const depId of node.dependencies) {
    const dep = await fetch(
      `https://bidda.com/api/v1/vault/nodes/${depId}.json`,
      { headers: { 'skyfire-pay-id': skyfireToken } }
    );
    const depNode = await dep.json();
    await auditLog.record({ action: 'dependency_consulted', receipt: depNode._receipt });
  }

  return node;
}
```

### Direct USDC Payment — Path C (ethers.js)

```javascript
import { ethers } from 'ethers';

const USDC_CONTRACT = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const USDC_ABI = ['function transfer(address to, uint256 amount) returns (bool)'];
const NODE_ID = 'nist-csf-2-0-govern';

async function payAndFetch(privateKey) {
  // 1. Get payment instructions from 402 response
  const res402 = await fetch(`https://bidda.com/api/v1/vault/nodes/${NODE_ID}.json`);
  const { payment_instructions } = await res402.json();
  const { destination, amount_usd } = payment_instructions.direct_base;
  const amountUnits = BigInt(Math.round(amount_usd * 1_000_000));

  // 2. Send USDC on Base
  const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
  const signer = new ethers.Wallet(privateKey, provider);
  const usdc = new ethers.Contract(USDC_CONTRACT, USDC_ABI, signer);
  const tx = await usdc.transfer(destination, amountUnits);
  const chainReceipt = await tx.wait();

  // 3. Fetch node with tx hash — Bidda injects compliance receipt
  const res = await fetch(`https://bidda.com/api/v1/vault/nodes/${NODE_ID}.json`, {
    headers: { 'x-base-tx-hash': chainReceipt.hash }
  });
  const node = await res.json();

  // node._receipt.txid === chainReceipt.hash — same proof, two places
  return node;
}
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/v1/nodes/index.json` | GET | None | Discovery index — all 7,243 nodes, 6 fields each |
| `/api/v1/nodes/{nodeId}.json` | GET | None | Single node discovery record (free) |
| `/api/v1/nodes/latest.json` | GET | None | 20 most recently updated nodes |
| `/api/v1/vault/nodes/{nodeId}.json` | GET | Required | Full 13-key node + receipt — **$0.01** |
| `/api/v1/vault/pillar/{slug}.json` | GET | Required | Full pillar bundle + receipt — **$5–$49** |
| `/api/v1/vault/pillar/_all.json` | GET | Required | Full registry — **Enterprise subscription** |
| `/api/v1/vault/bundle?pillars=X,Y,Z` | GET | Required | Multi-pillar bundle + receipt — **sum of pillar prices** |
| `/api/v1/graph.json` | GET | None | Full dependency graph (all node relationships) |
| `/api/v1/registry-health.json` | GET | None | Weekly source integrity status |
| `/api/v1/openapi-skyfire.json` | GET | None | OpenAPI 3.0 specification |
| `/.well-known/ai-plugin.json` | GET | None | AI plugin manifest (ChatGPT/Copilot compatible) |
| `/.well-known/agent-card.json` | GET | None | A2A agent card |
| `/llms.txt` | GET | None | Machine-readable registry summary for LLM crawlers |
| `/llms-full.txt` | GET | None | Full node listing for LLM crawlers |

---

## Authentication

Three payment paths on vault endpoints:

### Path A — Skyfire `pay+jwt` (primary for AI agents)

```
skyfire-pay-id: <pay+jwt token string>
```

Get a token at [app.skyfire.xyz](https://app.skyfire.xyz). **Best for:** autonomous AI agents, enterprise integrations.

### Path B — L402 / USDC on Base

```
Authorization: L402 web3:MACAROON:0xTX_HASH
```

Send $0.01 USDC on Base, include the tx hash. **Best for:** Web3 wallets (MetaMask, Coinbase Wallet).

### Path C — Direct Base USDC (simplest)

```
x-base-tx-hash: 0xYOUR_TX_HASH
```

No account required. Send USDC directly on Base to the treasury wallet, pass the tx hash. The worker verifies on-chain and blocks replay. **Best for:** headless agents, crypto-native teams.

**Agent flow:**
```
1. GET /api/v1/vault/nodes/{id}.json  →  402 + payment_instructions
2. Read destination and amount_usd from 402 body
3. Send USDC on Base, capture tx hash
4. GET /api/v1/vault/nodes/{id}.json  +  x-base-tx-hash: 0x...
5. Receive full 13-key node JSON with _receipt block
```

---

## Pricing

### Pay-as-you-go — Single Node

**$0.01 per node** — fixed, forever. No account, no subscription. Agents making 1,000 calls pay $10 total. Three payment paths: Skyfire JWT, L402 / USDC on Base, or Direct Base USDC.

### Pillar Bundles (one-time frozen snapshot)

A pillar bundle is a point-in-time snapshot of every node in that domain. One-time bundles do not receive live regulatory updates — auto-update is a subscription feature.

| Tier | Price | Pillars |
|---|---|---|
| Workflow | $5 | `workflow` |
| Standard | $9 | `crypto`, `food`, `media`, `operations`, `gaming`, `biotech`, `mining`, `space`, `maritime`, `industrial`, `energy`, `construction`, `telecoms`, `tax`, `pharma`, `insurance`, `competition`, `automotive`, `education`, `sales` |
| Premium | $19 | `aviation`, `medical`, `esg`, `logistics`, `cloud` |
| MITRE cross-cut | $29 | `mitre` (ATT&CK + ATLAS + D3FEND + CAPEC) |
| Large | $34 | `workplace` |
| Enterprise pillar | $39 | `ai-governance` |
| Flagship | $49 | `finance`, `legal`, `cybersecurity` |

Multi-pillar: `GET /api/v1/vault/bundle?pillars=finance,crypto,legal` — price = sum of individual pillar prices.

### Subscriptions (billed in ZAR via Paystack; USD shown at the equivalent rate)

| Plan | Price | Included |
|---|---|---|
| Starter | $49 / month | 100 node unlocks per month (single nodes) |
| Professional | $199 / month | 1,000 nodes per month, pillar-bundle access, always-latest versions (auto-update on every call) |
| Enterprise | $499 / month | Unlimited nodes — single, pillar, or full registry — plus API keys, audit log, and compliance attestation |

Annual billing saves 20% on every tier. Full-registry access is an Enterprise feature. Volume contracts from $2,500/month — contact info@bidda.com.

---

## 402 Payment Required — Response Format

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
      "amount_usd": 0.01
    },
    "direct_base": {
      "header": "x-base-tx-hash",
      "format": "0xYOUR_TX_HASH",
      "network": "Base",
      "chain_id": 8453,
      "amount_usd": 0.01,
      "destination": "0xD5eF3584bFa5D0ECE885A1101d00E431D3b6654A"
    }
  }
}
```

`amount_usd` reflects the correct price for the endpoint requested.

---

## Node JSON Structure (13-key schema + receipt)

**Discovery tier** (free) returns: `node_id`, `title`, `domain`, `version`, `bluf`, `paywall`

**Vault tier** (paid) returns all 13 keys plus `_receipt`:

```json
{
  "node_id": "eu-gdpr-article-33",
  "title": "GDPR Article 33 — Personal Data Breach Notification",
  "domain": "Cybersecurity",
  "version": "2.1.3",
  "last_updated": "2026-04-01",
  "bluf": "Controllers must notify the supervisory authority of a personal data breach within 72 hours of becoming aware of it, unless the breach is unlikely to result in risk to individuals.",
  "paywall": { "status": "gated", "unlock_cost_usd": "0.01" },
  "verification": {
    "authority": "Bidda Sovereign Trust",
    "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679",
    "integrity_hash": "sha256:a3f9c2e1b4d8f7a6...",
    "status": "VERIFIED",
    "jurisdiction": "EU",
    "instrument_type": "REGULATION",
    "effective_date": "2018-05-25"
  },
  "crosswalks": {
    "nist_csf": "RS.CO-2",
    "iso_27001": "A.16.1.3"
  },
  "dependencies": ["gdpr-article-4-definitions", "gdpr-article-34-notification"],
  "actionable_schema": {
    "breach_notification_window_hours": 72,
    "mandatory_supervisory_notification": true
  },
  "deterministic_workflow": [
    { "step": 1, "logic": "Determine whether a personal data breach has occurred within the meaning of GDPR Article 4(12)." },
    { "step": 2, "logic": "Assess the risk to the rights and freedoms of natural persons." },
    { "step": 3, "logic": "If risk is not unlikely, notify the competent supervisory authority within 72 hours of becoming aware." }
  ],
  "primary_citations": [
    "GDPR Article 33 — Notification of a personal data breach to the supervisory authority, Regulation (EU) 2016/679",
    "EDPB Guidelines 9/2022 on personal data breach notification under GDPR"
  ],
  "_receipt": {
    "node_id":        "eu-gdpr-article-33",
    "version":        "2.1.3",
    "integrity_hash": "sha256:a3f9c2e1b4d8f7a6...",
    "accessed_at":    "2026-05-01T09:32:14.000Z",
    "txid":           "0x7a3b8f1c2d4e5f6a...",
    "amount_usd":     "0.01",
    "currency":       "USDC/Base",
    "registry":       "Bidda Sovereign Intelligence",
    "statement":      "Access to eu-gdpr-article-33 v2.1.3 verified at 2026-05-01T09:32:14.000Z. Integrity hash sha256:a3f9... recorded at time of access."
  }
}
```

---

## 34 Active Sovereign Pillars

Node counts per pillar (live registry). Bundle pricing is by tier — see the [Pricing](#pricing) section.

| Slug | Pillar | Nodes |
|---|---|---|
| `cybersecurity` | Cybersecurity | 1,947 |
| `legal` | Legal & IP Sovereignty | 697 |
| `finance` | Banking & Global Finance | 581 |
| `ai-governance` | AI Governance & Law | 566 |
| `medical` | Medical & Healthcare | 325 |
| `esg` | Sustainability & ESG | 286 |
| `workplace` | Workplace | 281 |
| `aviation` | Aviation, Defense & Quantum | 119 |
| `competition` | Competition & Antitrust | 116 |
| `food` | Food & Hospitality | 112 |
| `logistics` | Logistics & Supply Chain | 111 |
| `crypto` | Crypto & Sovereign Finance | 110 |
| `insurance` | Insurance & Risk | 110 |
| `tax` | Tax & Transfer Pricing | 106 |
| `gaming` | Gaming & Gambling | 105 |
| `cloud` | Cloud & SaaS | 103 |
| `biotech` | Biotech & Genomics | 103 |
| `education` | Education & Research | 102 |
| `maritime` | Maritime & Shipping | 101 |
| `space` | Space & Satellite Law | 101 |
| `industrial` | Industrial IoT & Energy | 100 |
| `energy` | Energy & Utilities | 100 |
| `sales` | Sales, Marketing & PR | 99 |
| `pharma` | Pharmaceuticals & Life Sciences | 99 |
| `telecoms` | Telecoms & Digital Infrastructure | 98 |
| `operations` | Operations & CX | 95 |
| `construction` | Construction & Real Estate | 95 |
| `mining` | Mining & Natural Resources | 94 |
| `automotive` | Automotive & Mobility | 92 |
| `media` | Creative, Content & Media IP | 91 |
| `workflow` | Workflow Automation | 88 |
| `immigration` | Immigration & Border Control | 57 |
| `water` | Water & Environmental Resources | 37 |
| `agriculture` | Agriculture & Agritech | 16 |

---

## Node Freshness & Drift Detection

```javascript
// 1. Free discovery call — check the live hash
const live = await fetch('https://bidda.com/api/v1/nodes/eu-gdpr-article-33.json');
const { version, verification } = await live.json();

// 2. Compare against your cached hash
if (cached.integrity_hash !== verification.integrity_hash) {
  // Regulation updated — re-unlock for $0.01 to get fresh content + new receipt
  const fresh = await fetch('https://bidda.com/api/v1/vault/nodes/eu-gdpr-article-33.json', {
    headers: { 'skyfire-pay-id': skyfireToken }
  });
  const updated = await fresh.json();
  cache.set('eu-gdpr-article-33', updated);
  auditLog.record({ event: 'node_refreshed', receipt: updated._receipt });
}
```

The hash check eliminates the risk of executing against an outdated legal framework. When a regulation is amended, the node version increments and the hash changes — agents can detect this without paying.

---

## Registry Health

```bash
curl https://bidda.com/api/v1/registry-health.json
```

Returns: node count, sources tracked, change count for the last 7 days, next check schedule, and source integrity summary. Updated every Monday at 02:00 UTC by the source watcher.

---

## Links

- Website: [bidda.com](https://bidda.com)
- Intelligence Forest: [bidda.com/intelligence](https://bidda.com/intelligence)
- Developer Portal: [bidda.com/developers](https://bidda.com/developers)
- Audit Trail Guide: [bidda.com/audit](https://bidda.com/audit)
- Pricing: [bidda.com/pricing](https://bidda.com/pricing)
- Registry Health: [bidda.com/api/v1/registry-health.json](https://bidda.com/api/v1/registry-health.json)
- OpenAPI Spec: [bidda.com/api/v1/openapi-skyfire.json](https://bidda.com/api/v1/openapi-skyfire.json)
- LLM Discovery: [bidda.com/llms.txt](https://bidda.com/llms.txt)
- Contact: info@bidda.com
