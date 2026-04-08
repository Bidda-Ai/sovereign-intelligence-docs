# API Access & L402 Integration (Beta Protocol)

The Bidda Sovereign Intelligence Forest is currently transitioning to fully autonomous L402 (HTTP 402 Payment Required) node resolution via the Skyfire network. 

During this Beta phase, while our automated agent-to-agent settlement layer is finalized, we provide manual API provisioning for enterprise testing and sandbox environments.

## How to Access the Nodes

### 1. The Web Interface (Single Node Retrieval)
Developers can manually query and unlock individual compliance nodes via the Bidda web portal. 
* A web-based wallet interface is provided to settle the $0.01 USDC unlock fee per node.
* Upon settlement, the payload is immediately returned adhering strictly to the 13-key Golden Schema.

### 2. Programmatic API Access (Sandbox)
If you are building an agentic workflow that requires batch querying or programmatic access to the full 501-node registry, you can request a temporary bypass token.

**To request sandbox access:**
1. Execute your test L402 web payment to verify your wallet architecture.
2. Email the transaction hash and your agent's intended `User-Agent` string to `api@bidda.com`.
3. Our engineering team will provision a temporary bearer token allowing direct `GET` requests to the `/nodes` endpoints while our autonomous payment gateway is finalized.
