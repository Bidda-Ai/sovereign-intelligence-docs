# The Bidda "Golden Schema" (13-Key Architecture)

To guarantee deterministic execution and absolute compliance, every node within the Bidda Sovereign Intelligence Forest adheres to a strict, mathematically verifiable 13-key JSON structure. 

This schema bridges the gap between natural language legal text and machine-readable boolean logic. It eliminates LLM hallucination risk by enforcing a standardized payload that enterprise agents can natively parse, execute, and verify.

## Schema Definition

Every Bidda Node payload is guaranteed to return the following 13 root keys. *(Note: If a specific node does not require a field, the key will still be present and return `null` or `[]` to prevent parser errors).*

### 1. `node_id` (String)
A unique, immutable alphanumeric identifier for the regulatory node (e.g., `bitcoin-lightning-l402`).

### 2. `title` (String)
The human-readable title of the regulation, standard, or protocol.

### 3. `domain` (String)
The primary enterprise sector this node governs (e.g., `Aviation`, `Defense`, `Finance`, `ESG`).

### 4. `version` (String)
Semantic versioning (e.g., `1.1.0`) tracking the iteration of the node. This increments automatically when the underlying regulation is updated.

### 5. `last_updated` (String)
ISO 8601 timestamp (YYYY-MM-DD) indicating the date of the most recent regulatory amendment or schema update.

### 6. `bluf` (String)
*Bottom Line Up Front.* A dense, highly optimized 1-2 sentence summary designed specifically for LLM context windows. It provides immediate context to the querying agent before it processes the boolean logic.

### 7. `paywall` (Object)
Contains the Web3/Skyfire routing parameters required for autonomous agents to negotiate HTTP 402 payment challenges.
* `status`: Current lock state (e.g., `LOCKED`, `UNLOCKED`).
* `unlock_cost_usd`: The USDC micropayment threshold.
* `skyfire_id`: The routing address for the Skyfire SDK.

### 8. `verification` (Object)
The cryptographic proof of the node's authenticity and source origin. 
* `authority`: The official governing body or standard issuer.
* `source_url`: Permalink to the raw, official source text.
* `status`: Verification state (e.g., `VERIFIED`).
* `timestamp`: ISO 8601 timestamp of the exact moment the hash was generated.
* `integrity_hash`: A SHA-256 cryptographic hash of the node. Agents must compute the hash of the payload and compare it to this key to guarantee the logic has not suffered from AI drift or tampering.

### 9. `crosswalks` (Object)
Maps the specific rule to equivalent international frameworks to ensure cross-departmental compliance.
* `nist_framework`: Corresponding NIST controls.
* `iso_standard`: Corresponding ISO standards.

### 10. `dependencies` (Array)
An array of `node_id` strings linking to prerequisite regulations. This allows agents to autonomously traverse the Sovereign Intelligence Forest to build complete, multi-node compliance chains.

### 11. `actionable_schema` (Object)
**The Core Engine.** A nested object translating the legal text into strict boolean logic, quantitative thresholds, and required data types. Agents use this to programmatically validate their planned actions against the hardcoded rule.

### 12. `deterministic_workflow` (Array of Objects)
A machine-readable, step-by-step execution path mapping the regulation into software logic. Each step contains:
* `step`: Integer representing the sequence order.
* `condition`: The specific state or trigger required to initiate the step.
* `action`: The deterministic function the agent must perform.
* `fallback`: The required failover action if the primary condition fails or is violated.

### 13. `primary_citations` (Array)
An array of strings listing the official legal chapters, articles, or technical specifications referenced within the node logic.

---

## Example Payload

```json
{
  "node_id": "bitcoin-lightning-l402",
  "title": "Bitcoin Lightning L402 Protocol Standard",
  "domain": "Web3 & Autonomous Payments",
  "version": "1.1.0",
  "last_updated": "2026-04-08",
  "bluf": "L402 is a protocol standard enabling HTTP 402 Payment Required responses to be resolved via Bitcoin Lightning Network micropayments using macaroons.",
  "paywall": {
    "status": "LOCKED",
    "unlock_cost_usd": "0.01",
    "skyfire_id": "PLACEHOLDER_SKYFIRE_ID_BIDDA_NODES"
  },
  "verification": {
    "authority": "Lightning Labs API Standard",
    "source_url": "[https://lightning.engineering/api-docs/api/lnd/lightning/add-invoice](https://lightning.engineering/api-docs/api/lnd/lightning/add-invoice)",
    "status": "VERIFIED",
    "timestamp": "2026-04-08T11:55:05.000Z",
    "integrity_hash": "sha256:262bed997bc80a1a4a570025b8b8a658d9cf244805ce9ea1a62b36852d20dd0b"
  },
  "crosswalks": {
    "nist_framework": null,
    "iso_standard": null
  },
  "dependencies": [
    "http-402-client-error-standard",
    "macaroon-auth-handling-01"
  ],
  "actionable_schema": {
    "require_http_402_header": true,
    "macaroon_validation_required": true,
    "max_preimage_timeout_seconds": 60,
    "allow_zero_value_invoices": false
  },
  "deterministic_workflow": [
    {
      "step": 1,
      "condition": "RECEIVE_HTTP_402",
      "action": "Extract invoice string and macaroon from WWW-Authenticate header.",
      "fallback": "TERMINATE_CONNECTION"
    },
    {
      "step": 2,
      "condition": "INVOICE_EXTRACTED",
      "action": "Route payment via Lightning Network using preimage.",
      "fallback": "RETRY_ALTERNATIVE_ROUTE"
    }
  ],
  "primary_citations": [
    "Lightning Labs L402 Protocol Specification v1.0",
    "RFC 7235: HTTP/1.1 Authentication (Status Code 402)"
  ]
}
```
