from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


# Customer Registration Model
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None


# User Login Model
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User Response Model
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: Literal["admin", "staff", "customer"]
    created_at: Optional[datetime] = None


# User Role Model
class UserRole(BaseModel):
    role: Literal["admin", "staff", "customer"]