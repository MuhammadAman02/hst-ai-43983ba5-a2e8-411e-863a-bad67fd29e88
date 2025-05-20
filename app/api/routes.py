from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from ..services.fraud_detection import FraudDetectionSystem

router = APIRouter()

# Initialize the fraud detection system
fds = FraudDetectionSystem()

class Transaction(BaseModel):
    user_id: str
    amount: float
    timestamp: datetime
    merchant: str

@router.post('/check-transaction')
async def check_transaction(transaction: Transaction):
    """Check if a transaction is potentially fraudulent."""
    is_fraudulent, reason = fds.check_transaction(
        transaction.user_id,
        transaction.amount,
        transaction.timestamp,
        transaction.merchant
    )

    if is_fraudulent:
        raise HTTPException(status_code=400, detail=f"Potential fraud detected: {reason}")

    # If not fraudulent, add the transaction to the history
    fds.add_transaction(
        transaction.user_id,
        transaction.amount,
        transaction.timestamp,
        transaction.merchant
    )

    return {"message": "Transaction approved"}

@router.get('/flagged-transactions')
async def get_flagged_transactions():
    """Get all flagged transactions."""
    return fds.get_flagged_transactions()

@router.get('/ping')
async def ping_pong():
    """A simple ping endpoint."""
    return {"message": "pong!"}