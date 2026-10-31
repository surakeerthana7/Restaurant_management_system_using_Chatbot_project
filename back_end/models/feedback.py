
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Create Feedback Model
class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    order_id: Optional[str] = None


# Feedback Response Model
class FeedbackResponse(BaseModel):
    id: str
    user_id: str
    rating: int
    comment: Optional[str] = None
    order_id: Optional[str] = None
    created_at: Optional[datetime] = None


# Update Feedback Model
class FeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
