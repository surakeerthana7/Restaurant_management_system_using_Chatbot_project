
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# Individual Food Item in an Order
class OrderItem(BaseModel):
    menu_item_id: str
    name: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


# Create Order Model
class OrderCreate(BaseModel):
    items: List[OrderItem]
    order_type: Literal["dine_in", "takeaway", "delivery"]
    table_id: Optional[str] = None
    delivery_address: Optional[str] = None


# Order Response Model
class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    order_type: Literal["dine_in", "takeaway", "delivery"]
    status: Literal[
        "pending",
        "confirmed",
        "preparing",
        "ready",
        "completed",
        "cancelled"
    ]
    table_id: Optional[str] = None
    delivery_address: Optional[str] = None
    created_at: Optional[datetime] = None


# Update Order Status Model
class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "confirmed",
        "preparing",
        "ready",
        "completed",
        "cancelled"
    ]
