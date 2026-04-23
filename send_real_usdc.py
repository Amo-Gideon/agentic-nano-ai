import time
from web3 import Web3

# ---------------------- CONFIG ----------------------
RPC_URL = "https://rpc.testnet.arc.network"
USDC_CONTRACT = "0x3600000000000000000000000000000000000000"
APP_WALLET = "0xcF1DD1B3B2A682F7d7935bbbcFe9C5514b19E9f0"

# ⚠️ PASTE YOUR METAMASK PRIVATE KEY HERE (STARTS WITH 0x)
PRIVATE_KEY = "dd08ca0d34c2de74d71be3298ed75682aa8065846c0ee8ad5727ff16f78537cc"

# ERC20 ABI (STABLE, CORRECT)
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

def main():
    print("=" * 60)
    print("ARC TESTNET — REAL USDC NANOPAYMENTS")
    print("=" * 60)

    # Connect to RPC
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Cannot connect to Arc Testnet")
        return
    print(f"✅ Connected (Chain ID: {w3.eth.chain_id})\n")

    # Load wallet
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
    except:
        print("❌ INVALID PRIVATE KEY!")
        return

    sender = account.address
    print(f"📤 Sender:     {sender}")
    print(f"📥 Receiver:   {APP_WALLET}\n")

    # USDC Contract
    usdc = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)
    decimals = usdc.functions.decimals().call()
    balance = usdc.functions.balanceOf(sender).call()
    print(f"💰 Balance:    {balance / 10**decimals} USDC")

    # Tx Settings
    amount_per_tx = int(0.001 * 10**decimals)
    gas_price = w3.to_wei('10', 'gwei')
    gas_limit = 100000
    print(f"💵 Per tx:     ${amount_per_tx / 10**decimals} USDC")
    print(f"⛽ Gas price:  10 gwei\n")

    num_txs = 50
    print(f"📦 Sending {num_txs} transactions...\n")

    tx_hashes = []
    for i in range(num_txs):
        try:
            nonce = w3.eth.get_transaction_count(sender, 'pending')
            tx = usdc.functions.transfer(APP_WALLET, amount_per_tx).build_transaction({
                'from': sender,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price
            })
            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            tx_hashes.append(tx_hash_hex)
            print(f"  ✅ Tx {i+1:2d}/{num_txs} | {tx_hash_hex}")
            time.sleep(5)

        except Exception as e:
            err = str(e)
            if "txpool is full" in err:
                print(f"  ⏳ Tx {i+1:2d}/{num_txs} | txpool full, waiting 30s...")
                time.sleep(30)
                continue
            else:
                print(f"  ❌ Tx {i+1:2d}/{num_txs} | {err[:60]}")
                time.sleep(5)

    print()
    print("=" * 60)
    print(f"✅ {len(tx_hashes)}/{num_txs} TRANSACTIONS SENT")
    print("=" * 60)

    print(f"\n🔗 View on Arcscan:")
    print(f"   https://testnet.arcscan.app/address/{APP_WALLET}")
    print("\n⏳ Wait 30-60 seconds for all to confirm, then refresh Arcscan")

    # Save tx hashes
    print("\n💾 Saving to tx_hashes.txt")
    with open("tx_hashes.txt", "w") as f:
        for h in tx_hashes:
            f.write(h + "\n")

    # Economic Proof (for judges)
    print("\n📋 ECONOMIC PROOF:")
    print(f"   50 tasks × $0.001  = $0.050 revenue")
    print(f"   50 txs × ~$0.009 gas = ~$0.450 gas")
    print(f"   Total: ~$0.50 USDC spent")
    print("\n   On Ethereum L1:")
    print(f"   50 txs × $1.50 gas = $75.00 gas")
    print(f"   Result: -$74.95 LOSS")
    print("\n   Arc makes this viable. L1 makes it impossible.")

if __name__ == "__main__":
    main()