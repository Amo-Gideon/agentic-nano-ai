from pydantic import BaseModel

class TaskRequest(BaseModel):
    user_wallet: str
    task: str

class PaymentProof(BaseModel):
    user_wallet: str
    task: str
    tx_hash: str