import requests
import time

API_URL = "http://localhost:5000"
YOUR_ARC_WALLET = "0xcF1DD1B3B2A682F7d7935bbbcFe9C5514b19E9f0"

print("=" * 60)
print("AGENTIC NANO AI — 100 Transaction Demo")
print("=" * 60)
print(f"Wallet: {YOUR_ARC_WALLET}")
print(f"Fee per task: $0.001 USDC")
print()

successful = 0
failed = 0
total_fees = 0.0

for i in range(100):
    task = f"Demo AI task {i+1}"
    try:
        req_res = requests.get(
            f"{API_URL}/api/payment-requirement",
            params={"user_wallet": YOUR_ARC_WALLET, "task": task}
        )
        req_data = req_res.json()
        task_id = req_data["task_id"]
        simulated_tx_hash = f"sim_tx_{task_id}_{int(time.time() * 1000)}"
        exec_res = requests.post(
            f"{API_URL}/api/execute-task",
            json={
                "user_wallet": YOUR_ARC_WALLET,
                "task": task,
                "tx_hash": simulated_tx_hash
            }
        )
        if exec_res.status_code == 200:
            exec_data = exec_res.json()
            successful += 1
            total_fees += 0.001
            print(f"Tx {i+1:3d} | Task: {task_id} | AI: {exec_data['ai_result'][:50]}...")
        else:
            failed += 1
            print(f"Tx {i+1:3d} | Payment verification failed")
    except Exception as e:
        failed += 1
        print(f"Tx {i+1:3d} | Error: {str(e)[:60]}")
    time.sleep(0.1)

print()
print("=" * 60)
print("DEMO COMPLETE")
print("=" * 60)
print(f"Successful: {successful}/100")
print(f"Failed:     {failed}/100")
print(f"Total fees: ${total_fees:.3f} USDC")
print()
print("Traditional L1 comparison:")
print(f"  100 txs @ $1.50 gas = $150.00 cost")
print(f"  Revenue = $0.10")
print(f"  LOSS = $149.90")
print()
print("Arc nanopayment model:")
print(f"  100 txs @ $0.0001 gas = $0.01 cost")
print(f"  Revenue = $0.10")
print(f"  PROFIT = $0.09")