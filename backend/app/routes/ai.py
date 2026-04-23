from fastapi import APIRouter, HTTPException
from backend.app.models.schema import PaymentProof
from backend.app.services.payment_service import verify_payment, get_payment_requirement
from backend.app.services.ai_service import run_ai_task
from backend.app.core.config import settings
import uuid

router = APIRouter()

@router.get("/api/payment-requirement")
def request_payment_requirement(user_wallet: str, task: str):
    task_id = str(uuid.uuid4())[:8]
    requirement = get_payment_requirement(task_id)
    return {
        "task_id": task_id,
        "payment_required": True,
        "requirement": requirement,
        "instructions": f"Send {settings.NANO_FEE_USDC} USDC to {settings.WALLET_ADDRESS} on {settings.ARC_CHAIN}, then POST /api/execute-task with tx_hash"
    }

@router.post("/api/execute-task")
def execute_task(req: PaymentProof):
    verification = verify_payment(
        tx_hash=req.tx_hash,
        expected_amount=settings.NANO_FEE_USDC,
        user_wallet=req.user_wallet
    )
    if not verification["valid"]:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment verification failed",
                "verification": verification,
                "message": "Please complete payment first via /api/payment-requirement"
            }
        )
    ai_result = run_ai_task(req.task)
    return {
        "task_id": verification.get("tx_details", {}).get("id", "unknown"),
        "fee_usd": settings.NANO_FEE_USDC,
        "chain": settings.ARC_CHAIN,
        "payment_verified": True,
        "amount_paid": verification["amount_paid"],
        "ai_result": ai_result
    }

@router.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "wallet": settings.WALLET_ADDRESS,
        "fee_per_task": settings.NANO_FEE_USDC,
        "chain": settings.ARC_CHAIN
    }