
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# Create Table Model
class TableCreate(BaseModel):
    table_number: int = Field(..., gt=0)
    capacity: int = Field(..., gt=0)
    location: Optional[str] = None


# Table Response Model
class TableResponse(BaseModel):
    id: str
    table_number: int
    capacity: int
    location: Optional[str] = None
    status: Literal["available", "occupied", "reserved"] = "available"
    created_at: Optional[datetime] = None


# Update Table Model
class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    status: Optional[Literal["available", "occupied", "reserved"]] = None
