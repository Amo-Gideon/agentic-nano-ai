import requests

API_URL = "http://localhost:5000"
WALLET = "0xcF1DD1B3B2A682F7d7935bbbcFe9C5514b19E9f0"

with open("tx_hashes.txt", "r") as f:
    tx_hashes = [line.strip() for line in f if line.strip()]

print(f"Running {len(tx_hashes)} REAL Arc Testnet transactions...")
print("Each hash is verified on-chain via web3.py")
print()

for i, tx_hash in enumerate(tx_hashes):
    task = f"Real AI task {i+1}"
    res = requests.post(
        f"{API_URL}/api/execute-task",
        json={"user_wallet": WALLET, "task": task, "tx_hash": tx_hash}
    )
    if res.status_code == 200:
        data = res.json()
        print(f"✅ Tx {i+1}: {data['ai_result'][:50]}...")
        print(f"   Explorer: {data.get('explorer_url', 'N/A')}")
    else:
        print(f"❌ Tx {i+1}: {res.json().get('detail', {}).get('error', 'Failed')}")