from fastapi import APIRouter, HTTPException
from backend.app.models.schema import PaymentProof
from backend.app.services.payment_service import verify_payment
from backend.app.services.ai_service import run_ai_task
from backend.app.core.config import settings
import uuid

router = APIRouter()

SUBTASK_PROMPTS = {
    "research": "Research and list 5 key facts about: {topic}. Return only bullet points.",
    "draft": "Write a 3-paragraph blog post about: {topic}. Use these facts: {facts}",
    "edit": "Edit and polish this blog post. Make it engaging and professional. Return only the final text.\n\nDraft:\n{draft}"
}

@router.post("/api/complex-task")
def execute_complex_task(req: PaymentProof):
    verification = verify_payment(
        tx_hash=req.tx_hash,
        expected_amount=settings.NANO_FEE_USDC * 3,
        user_wallet=req.user_wallet
    )
    if not verification["valid"]:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment verification failed",
                "required": settings.NANO_FEE_USDC * 3,
                "message": "Complex tasks require $0.003 USDC (3 sub-agents)"
            }
        )
    topic = req.task
    job_id = str(uuid.uuid4())[:8]
    research_task = SUBTASK_PROMPTS["research"].format(topic=topic)
    research_result = run_ai_task(research_task)
    draft_task = SUBTASK_PROMPTS["draft"].format(topic=topic, facts=research_result)
    draft_result = run_ai_task(draft_task)
    edit_task = SUBTASK_PROMPTS["edit"].format(draft=draft_result)
    final_result = run_ai_task(edit_task)
    return {
        "job_id": job_id,
        "topic": topic,
        "total_fee": settings.NANO_FEE_USDC * 3,
        "chain": settings.ARC_CHAIN,
        "payment_verified": True,
        "amount_paid": verification["amount_paid"],
        "subtasks": [
            {"agent": "Research Agent", "fee": settings.NANO_FEE_USDC, "task": "Research facts", "output": research_result},
            {"agent": "Writer Agent", "fee": settings.NANO_FEE_USDC, "task": "Draft blog post", "output": draft_result},
            {"agent": "Editor Agent", "fee": settings.NANO_FEE_USDC, "task": "Polish final text", "output": final_result}
        ],
        "final_output": final_result,
        "economics": {
            "total_tasks": 3,
            "total_fee_usd": settings.NANO_FEE_USDC * 3,
            "per_agent_fee": settings.NANO_FEE_USDC,
            "arc_gas_estimate": round(0.009 * 3, 3),
            "l1_gas_estimate": round(1.50 * 3, 2),
            "arc_margin": "~90%",
            "l1_margin": "-49,900%"
        }
    }

@router.get("/api/complex-task-requirement")
def get_complex_task_requirement(user_wallet: str, task: str):
    job_id = str(uuid.uuid4())[:8]
    total_fee = settings.NANO_FEE_USDC * 3
    return {
        "job_id": job_id,
        "task": task,
        "payment_required": True,
        "total_fee": total_fee,
        "breakdown": [
            {"agent": "Research Agent", "fee": settings.NANO_FEE_USDC, "role": "Gather facts"},
            {"agent": "Writer Agent", "fee": settings.NANO_FEE_USDC, "role": "Draft content"},
            {"agent": "Editor Agent", "fee": settings.NANO_FEE_USDC, "role": "Polish final"}
        ],
        "currency": "USD",
        "destination": settings.WALLET_ADDRESS,
        "chain": settings.ARC_CHAIN,
        "protocol": "x402",
        "instructions": f"Send {total_fee} USDC to {settings.WALLET_ADDRESS} on {settings.ARC_CHAIN}. This hires 3 AI agents to complete your task."
    }