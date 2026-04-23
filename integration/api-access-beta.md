# API Access & Payment Integration Guide

Bidda nodes are served through a live two-tier API. The discovery tier is always free. The vault tier requires a $0.01 USDC micropayment — settled via Skyfire (primary path for AI agents), L402 / USDC on Base (Web3 path), or Direct Base USDC (no account required).

Registry: **2,408 verified nodes across 29 sovereign pillars.**

---

## Discovery Tier (Free — No Auth)

Use the discovery tier for agent planning, node listing, and freshness checks.

```bash
# List all 2,408 nodes
curl https://bidda.com/api/v1/nodes/index.json

# Fetch a single node's discovery metadata
curl https://bidda.com/api/v1/nodes/iso-42001-risk-assess.json
```

**Discovery response fields:**

```json
{
  "node_id": "iso-42001-risk-assess",
  "title": "ISO/IEC 42001 AI Risk Assessment Protocol",
  "domain": "AI Governance & Law",
  "version": "1.2.0",
  "last_updated": "2026-04-01",
  "bluf": "Structured framework for assessing and mitigating AI system risks under ISO/IEC 42001 Annex A.",
  "verification": {
    "integrity_hash": "sha256:8a2f4c...",
    "status": "VERIFIED"
  },
  "paywall": {
    "status": "gated",
    "unlock_cost_usd": "0.01"
  }
}
```

---

## Vault Tier — Three Payment Paths

The vault tier returns the full 13-key payload including `actionable_schema`, `deterministic_workflow`, and `primary_citations`.

### Path A — Skyfire `pay+jwt` (Primary for AI Agents)

The simplest path for any platform integrated with [Skyfire](https://app.skyfire.xyz). No on-chain transactions required.

```bash
# Single node — $0.01
curl https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Full pillar bundle — $1.99 (AI Governance)
curl https://bidda.com/api/v1/vault/pillar/ai-governance.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Full registry — $9.99
curl https://bidda.com/api/v1/vault/pillar/_all.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"
```

Header: `skyfire-pay-id` (not Authorization). Accepted token types: `pay` and `kya-pay`.

**Python example:**
```python
import requests

node = requests.get(
    'https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json',
    headers={'skyfire-pay-id': 'YOUR_SKYFIRE_PAY_JWT'}
).json()

print(node['bluf'])
for step in node['deterministic_workflow']:
    print(f"Step {step['step']}: {step['logic']}")
```

---

### Path B — L402 / USDC on Base (Web3 / MetaMask)

Single-node endpoints only. Send $0.01 USDC on Base and include the tx hash.

```bash
curl https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json \
  -H "Authorization: L402 web3:token:0xYourBaseTxHash"
```

---

### Path C — Direct Base USDC (No Account Required — LIVE)

Send USDC directly to the payment address on Base. No Skyfire account needed.

**Step 1: Get payment details from the 402 response**

```bash
curl -i https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json
# Returns 402 with full payment_instructions in body
```

```json
{
  "error": "402 Payment Required",
  "payment_instructions": {
    "direct_base": {
      "header": "x-base-tx-hash",
      "network": "Base",
      "chain_id": 8453,
      "amount_usd": 0.01,
      "destination": "0x...",
      "usdc_contract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    }
  }
}
```

Always read `destination` and `amount_usd` from the 402 response — do not hardcode them.

**Step 2: Send USDC on Base (Python / web3.py)**

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
usdc = w3.eth.contract(
    address='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    abi=[{
        "name": "transfer",
        "type": "function",
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool"}]
    }]
)

# amount_usd * 1,000,000 (USDC has 6 decimals)
tx = usdc.functions.transfer(
    destination_address,  # from 402 response
    10000                 # 0.01 USDC
).build_transaction({
    'from': your_wallet,
    'chainId': 8453,
    'gas': 60000,
    'nonce': w3.eth.get_transaction_count(your_wallet),
})
signed = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction).hex()
```

**Step 3: Present tx hash as payment proof**

```bash
curl https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json \
  -H "x-base-tx-hash: 0xYourTxHash"
```

```python
node = requests.get(
    'https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json',
    headers={'x-base-tx-hash': tx_hash}
).json()
```

The worker verifies the transfer on-chain and records the hash in a replay-prevention store. Allow up to 30 seconds for block indexing before retrying on a `402` response.

---

## Pillar Bundles (Skyfire only)

Unlock an entire regulatory domain in one call — more cost-effective at scale:

```bash
# AI Governance & Law — $1.99 (139 nodes)
curl https://bidda.com/api/v1/vault/pillar/ai-governance.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Cybersecurity — $1.99 (281 nodes)
curl https://bidda.com/api/v1/vault/pillar/cybersecurity.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"

# Full registry — $9.99 (2,408 nodes)
curl https://bidda.com/api/v1/vault/pillar/_all.json \
  -H "skyfire-pay-id: YOUR_SKYFIRE_PAY_JWT"
```

See the [pricing table](../README.md#pricing) for all 29 pillar slugs and prices.

---

## Hash-Staleness & Regulatory Drift Detection

**The most important integration pattern.** Regulations change. When a source law is amended, Bidda updates the node and the `integrity_hash` in the free discovery response changes.

Check freshness before executing compliance logic:

```python
import requests

def is_node_stale(node_id: str, cached_hash: str) -> bool:
    """Returns True if the node has been updated since last purchase."""
    live = requests.get(f'https://bidda.com/api/v1/nodes/{node_id}.json').json()
    return live['verification']['integrity_hash'] != cached_hash

cached = load_node_from_memory('iso-42001-risk-assess')

if is_node_stale('iso-42001-risk-assess', cached['verification']['integrity_hash']):
    # Regulation updated — repurchase for $0.01
    fresh_node = requests.get(
        'https://bidda.com/api/v1/vault/nodes/iso-42001-risk-assess.json',
        headers={'skyfire-pay-id': SKYFIRE_TOKEN}
    ).json()
    save_node_to_memory('iso-42001-risk-assess', fresh_node)
    node = fresh_node
else:
    node = cached

# Execute deterministic workflow
for step in node['deterministic_workflow']:
    run_step(step)
```

The hash check is a free API call. The $0.01 repurchase only fires when the law has actually changed.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `402` after submitting tx hash | Block not yet indexed | Wait 30s, retry with same hash |
| `"Verification Failed"` | Wrong USDC amount or wrong chain | Confirm `10000` units on Base (chain 8453) |
| `403` on vault | Missing payment header | Add `skyfire-pay-id` or `x-base-tx-hash` header |
| `401` on vault | Wrong auth format for L402 | Format must be `L402 web3:token:0x...` |
| Stale `integrity_hash` | Node updated since last purchase | Re-fetch discovery, check hash, repurchase if changed |

---

## Rate Limits

- Discovery endpoints (`/api/v1/nodes/*`): 100 requests/minute per IP
- Vault endpoints (`/api/v1/vault/*`): Unlimited for valid credentials

---

## Contact

Enterprise access, volume pricing, and Skyfire integration support: `info@bidda.com`
