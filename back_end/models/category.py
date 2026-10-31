
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Create Category Model
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2)
    description: Optional[str] = None


# Category Response Model
class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


# Update Category Model
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
