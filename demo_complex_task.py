import requests
import time

API_URL = "http://localhost:5000"
WALLET = "0xcF1DD1B3B2A682F7d7935bbbcFe9C5514b19E9f0"

print("=" * 70)
print("🤖 AGENT PRIME — MULTI-AGENT ORCHESTRATION")
print("=" * 70)
print()
print("User Request: 'Write a blog post about AI agents'")
print()
print("Agent Prime breaks this into 3 subtasks:")
print("  1. Research Agent  ($0.001)")
print("  2. Writer Agent    ($0.001)")
print("  3. Editor Agent    ($0.001)")
print()
print("Total Cost: $0.003 USDC")
print("=" * 70)
print()

print("📋 Step 1: Getting payment requirement...")
req_res = requests.get(
    f"{API_URL}/api/complex-task-requirement",
    params={"user_wallet": WALLET, "task": "Write a blog post about AI agents"}
)
req_data = req_res.json()
job_id = req_data["job_id"]

print(f"   Job ID: {job_id}")
print(f"   Total Fee: ${req_data['total_fee']} USDC")
print()

simulated_tx = f"complex_tx_{job_id}_{int(time.time() * 1000)}"

print("💰 Step 2: Payment sent — hiring 3 agents...")
print()

print("⚙️  Step 3: Agent Prime orchestrating subtasks...")
print("   (Takes ~15 seconds — 3 AI calls)")
print()

start = time.time()

exec_res = requests.post(
    f"{API_URL}/api/complex-task",
    json={
        "user_wallet": WALLET,
        "task": "Write a blog post about AI agents",
        "tx_hash": simulated_tx
    }
)

elapsed = time.time() - start
data = exec_res.json()

if exec_res.status_code == 200:
    print("=" * 70)
    print("✅ ALL 3 AGENTS COMPLETED")
    print("=" * 70)
    print()

    for i, sub in enumerate(data["subtasks"], 1):
        print(f"🤖 Agent {i}: {sub['agent']}")
        print(f"   Fee: ${sub['fee']} USDC")
        print(f"   Output: {sub['output'][:80]}...")
        print()

    print("=" * 70)
    print("📄 FINAL OUTPUT")
    print("=" * 70)
    print(data["final_output"])
    print()
    print("=" * 70)
    print("💰 ECONOMIC SUMMARY")
    print("=" * 70)
    econ = data["economics"]
    print(f"   Total Tasks:   {econ['total_tasks']}")
    print(f"   Total Fee:     ${econ['total_fee_usd']} USDC")
    print(f"   Arc Gas:       ${econ['arc_gas_estimate']}")
    print(f"   L1 Gas:        ${econ['l1_gas_estimate']}")
    print(f"   Arc Margin:    {econ['arc_margin']}")
    print(f"   L1 Margin:     {econ['l1_margin']}")
    print(f"   Time:          {elapsed:.1f}s")
    print()
    print("   Agent-to-agent commerce on Arc.")
else:
    print(f"❌ Error: {exec_res.json()}")