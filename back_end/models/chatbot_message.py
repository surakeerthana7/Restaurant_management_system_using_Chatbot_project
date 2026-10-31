
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


# Create Chatbot Message Model
class ChatbotMessageCreate(BaseModel):
    message: str
    session_id: Optional[str] = None


# Chatbot Response Model
class ChatbotMessageResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    message: str
    response: str
    sender: Literal["customer", "bot"]
    created_at: Optional[datetime] = None
