
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# Create Payment Model
class PaymentCreate(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)
    payment_method: Literal[
        "cash",
        "upi",
        "card"
    ]


# Payment Response Model
class PaymentResponse(BaseModel):
    id: str
    order_id: str
    user_id: str
    amount: float
    payment_method: Literal["cash", "upi", "card"]
    status: Literal[
        "pending",
        "completed",
        "failed",
        "refunded"
    ] = "pending"
    transaction_id: Optional[str] = None
    created_at: Optional[datetime] = None


# Update Payment Status Model
class PaymentStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "completed",
        "failed",
        "refunded"
    ]
