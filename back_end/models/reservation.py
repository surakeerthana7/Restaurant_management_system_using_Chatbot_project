
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# Create Reservation Model
class ReservationCreate(BaseModel):
    table_id: str
    reservation_date: datetime
    number_of_guests: int = Field(..., gt=0)
    special_request: Optional[str] = None


# Reservation Response Model
class ReservationResponse(BaseModel):
    id: str
    user_id: str
    table_id: str
    reservation_date: datetime
    number_of_guests: int
    status: Literal[
        "pending",
        "confirmed",
        "cancelled",
        "completed"
    ] = "pending"
    special_request: Optional[str] = None
    created_at: Optional[datetime] = None


# Update Reservation Status Model
class ReservationStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "confirmed",
        "cancelled",
        "completed"
    ]
