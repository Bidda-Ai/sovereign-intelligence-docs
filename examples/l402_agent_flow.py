"""
Example: Autonomous Agent L402 Payment Flow
This script demonstrates how an AI agent interacts with the Bidda Sovereign Intelligence Forest,
handles an HTTP 402 Payment Required challenge, and retrieves a compliance node.

Reference API: https://bidda.com/api/v1/vault/
"""

import requests
import time

# The target regulatory node (from the Bidda Web UI example)
TARGET_NODE_URL = "https://bidda.com/api/v1/vault/as9100-rev-d-qms"

def fetch_bidda_node():
    print("[Agent] Initiating request to Sovereign Intelligence Forest...")
    
    # STEP 1 — HIT THE VAULT ENDPOINT
    initial_response = requests.get(TARGET_NODE_URL)
    
    if initial_response.status_code == 402:
        challenge_data = initial_response.json()
        invoice_string = challenge_data.get("invoice")
        print(f"[Agent] HTTP 402 Payment Required. Received Invoice: {invoice_string[:15]}...")
        
        # STEP 2 — SETTLE $0.01 USDC ON BASE
        print("[Agent] Routing invoice to agentic wallet (e.g., Skyfire) for $0.01 USDC settlement on Base...")
        time.sleep(2) # Simulating network confirmation time
        
        # Once settled, the payment provider returns the cryptographic receipt
        signed_receipt_token = "mock_receipt_token_xyz123"
        print("[Agent] Payment confirmed. Receipt token generated.")
        
        # STEP 3 — RETRY WITH BEARER TOKEN
        print("[Agent] Retrying vault endpoint with L402 Authorization header...")
        headers = {
            "Authorization": f"L402 {signed_receipt_token}"
        }
        
        final_response = requests.get(TARGET_NODE_URL, headers=headers)
        
        if final_response.status_code == 200:
            print("[Agent] HTTP 200 OK. Vault Unlocked.")
            node_payload = final_response.json()
            
            # The agent now has the 13-key Golden Schema to govern its actions
            print("\n--- NODE DATA RETRIEVED ---")
            print(f"Title: {node_payload.get('title', 'AS9100 Rev D QMS')}")
            print("Actionable Schema loaded into agent memory.")
            return node_payload
        else:
            print(f"[Agent] Error unlocking node: {final_response.status_code}")
            return None
            
    elif initial_response.status_code == 200:
        print("[Agent] Node is currently free/unlocked.")
        return initial_response.json()

if __name__ == "__main__":
    fetch_bidda_node()
