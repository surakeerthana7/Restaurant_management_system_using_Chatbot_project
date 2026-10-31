
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Create Menu Item Model
class MenuCreate(BaseModel):
    name: str = Field(..., min_length=2)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: str
    image: Optional[str] = None
    is_available: bool = True


# Menu Item Response Model
class MenuResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    category_id: str
    image: Optional[str] = None
    is_available: bool = True
    created_at: Optional[datetime] = None


# Update Menu Item Model
class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[str] = None
    image: Optional[str] = None
    is_available: Optional[bool] = None
