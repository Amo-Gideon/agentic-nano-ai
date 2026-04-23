from web3 import Web3
from backend.app.core.config import settings

# Arc Testnet RPC
w3 = Web3(Web3.HTTPProvider("https://rpc.testnet.arc.network"))
USDC_CONTRACT = "0x3600000000000000000000000000000000000000"

ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
    {"anonymous": False, "inputs": [{"indexed": True, "name": "from", "type": "address"}, {"indexed": True, "name": "to", "type": "address"}, {"indexed": False, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"},
]

def verify_payment(tx_hash: str, expected_amount: float, user_wallet: str):
    """
    Verify a USDC payment on Arc Testnet by checking the actual on-chain transaction.
    """
    # Sandbox bypass for demo/development
    if settings.SANDBOX_MODE:
        return {
            "valid": True,
            "tx_details": {"id": tx_hash, "status": "COMPLETE", "sandbox": True},
            "amount_paid": expected_amount,
            "expected": expected_amount,
            "explorer_url": f"https://testnet.arcscan.app/tx/{tx_hash}"
        }

    try:
        # Get transaction receipt
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        if not receipt:
            return {"valid": False, "error": "Transaction not found on-chain", "tx_details": None}

        if receipt['status'] != 1:
            return {"valid": False, "error": "Transaction failed", "tx_details": receipt}

        # Get transaction details
        tx = w3.eth.get_transaction(tx_hash)

        # Verify it interacted with USDC contract
        if tx['to'].lower() != USDC_CONTRACT.lower():
            return {"valid": False, "error": "Not a USDC transaction", "tx_details": tx}

        # Check logs for Transfer event to app wallet
        usdc = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)
        logs = receipt.get('logs', [])

        transfer_found = False
        amount_paid = 0

        for log in logs:
            if log['address'].lower() == USDC_CONTRACT.lower():
                try:
                    decoded = usdc.events.Transfer().process_log(log)
                    if decoded['args']['to'].lower() == settings.WALLET_ADDRESS.lower():
                        transfer_found = True
                        amount_paid = decoded['args']['value'] / 10**6  # USDC has 6 decimals
                except:
                    continue

        if not transfer_found:
            return {"valid": False, "error": "No USDC transfer to app wallet found", "tx_details": receipt}

        if amount_paid < expected_amount:
            return {"valid": False, "error": f"Insufficient amount: {amount_paid} < {expected_amount}", "tx_details": receipt}

        return {
            "valid": True,
            "tx_details": {
                "blockNumber": receipt['blockNumber'],
                "gasUsed": receipt['gasUsed'],
                "transactionHash": tx_hash,
                "explorer_url": f"https://testnet.arcscan.app/tx/{tx_hash}"
            },
            "amount_paid": amount_paid,
            "expected": expected_amount
        }

    except Exception as e:
        return {"valid": False, "error": str(e), "tx_details": None}

def get_payment_requirement(task_id: str):
    return {
        "amount": settings.NANO_FEE_USDC,
        "currency": "USD",
        "destination": settings.WALLET_ADDRESS,
        "chain": settings.ARC_CHAIN,
        "description": f"AI Task Fee #{task_id}",
        "task_id": task_id,
        "settlement": "INSTANT",
        "protocol": "x402"
    }