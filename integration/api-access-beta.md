# API Access & L402 Integration Guide

Bidda nodes are served through a live two-tier API. The discovery tier is always free. The vault tier requires a $0.01 USDC micropayment settled on the Base network via the L402 / x402 protocol, or a Skyfire bearer token for enterprise integrations.

---

## Discovery Tier (Free — No Auth)

Use the discovery tier for agent planning, node listing, and freshness checks.

```bash
# List all 784 nodes
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
  "last_updated": "2026-03-15",
  "bluf": "Structured framework for assessing and mitigating AI system risks under ISO/IEC 42001 Annex A.",
  "verification": {
    "integrity_hash": "sha256:8a2f4c...",
    "status": "VERIFIED"
  },
  "paywall": {
    "status": "LOCKED",
    "unlock_cost_usd": "0.01",
    "skyfire_id": "bidda-iso-42001-risk-assess"
  }
}
```

---

## Vault Tier — L402 / x402 Protocol

The vault tier returns the full 13-key payload including `actionable_schema`, `deterministic_workflow`, and `primary_citations`.

### Step 1: Hit the vault endpoint — receive a 402

```bash
curl -i https://bidda.com/api/v1/vault/iso-42001-risk-assess.json
# HTTP/1.1 402 Payment Required
# X-Payment-Required: {"amount":"10000","currency":"USDC","network":"base","payee":"0xD5eF3584..."}
```

The 402 response body contains the payment parameters. Parse the `amount`, `currency`, `network`, and `payee` fields to construct your Base USDC transaction.

### Step 2: Settle $0.01 USDC on Base

Send exactly `10000` (6-decimal USDC) to the payee address on Base (chain ID 8453).

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
usdc = w3.eth.contract(address='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', abi=ERC20_ABI)

tx = usdc.functions.transfer(
    '0xD5eF3584bFa5D0ECE885A1101d00E431D3b6654A',  # Bidda treasury
    10000  # 0.01 USDC (6 decimals)
).build_transaction({
    'from': your_wallet,
    'chainId': 8453,
    'gas': 60000,
    'nonce': w3.eth.get_transaction_count(your_wallet),
})
signed = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
```

### Step 3: Present the transaction hash as your L402 credential

```bash
curl https://bidda.com/api/v1/vault/iso-42001-risk-assess.json \
  -H "Authorization: L402 web3:token:0xYourBaseTxHash"
```

The Cloudflare Worker validates the hash against the live Base network via JSON-RPC. Allow up to 30 seconds for block indexing before retrying on a `402` response.

---

## Vault Tier — Skyfire Bearer Token

If your platform is integrated with [Skyfire](https://skyfire.xyz), you can pay using a Skyfire `pay` or `kya-pay` bearer token instead of a raw transaction hash.

```bash
curl https://bidda.com/api/v1/vault/iso-42001-risk-assess.json \
  -H "Authorization: Bearer <skyfire-pay-token>"
```

Accepted token types: `pay` and `kya-pay`. The `kya` token type alone is not accepted.

---

## Hash-Staleness & Regulatory Drift

**The single most important integration pattern.**

Regulations change. When a node's source law is amended, Bidda updates the node and the `integrity_hash` in the free discovery response changes.

Your agent must check hash freshness before executing compliance logic:

```python
import requests, json

def is_node_stale(node_id: str, cached_hash: str) -> bool:
    """Returns True if the node has been updated since last purchase."""
    live = requests.get(f'https://bidda.com/api/v1/nodes/{node_id}.json').json()
    return live['verification']['integrity_hash'] != cached_hash

# In your compliance workflow:
cached = load_node_from_memory('iso-42001-risk-assess')

if is_node_stale('iso-42001-risk-assess', cached['verification']['integrity_hash']):
    # Cached node is non-compliant — repurchase
    fresh_node = fetch_vault_node('iso-42001-risk-assess')  # triggers $0.01 settlement
    save_node_to_memory('iso-42001-risk-assess', fresh_node)
    node = fresh_node
else:
    node = cached

# Execute using node['deterministic_workflow']
```

**Why this matters:** Running workflow logic from a stale node means executing against an outdated legal framework. The hash check is a 1-line free API call that eliminates this risk. The $0.01 repurchase is a freshness fee, not a re-access fee.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `402` after submitting hash | Block not yet indexed | Wait 30s, retry with same hash |
| `"Verification Failed"` | Wrong USDC amount or wrong chain | Confirm `10000` units (not 0.01) on Base (chain 8453) |
| `401 Unauthorized` | Missing or malformed Authorization header | Ensure format is `L402 web3:token:0x...` |
| Stale `integrity_hash` | Node updated since last purchase | Re-fetch discovery, settle new payment |

---

## Rate Limits

- Discovery endpoints (`/api/v1/nodes/*`): 100 requests/minute per IP
- Vault endpoints (`/api/v1/vault/*`): Unlimited for valid credentials

---

## Contact

Enterprise access, volume pricing, and Skyfire integration support: `api@bidda.com`
