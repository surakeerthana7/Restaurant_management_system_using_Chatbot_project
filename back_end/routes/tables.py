
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import tables_collection
from models.table import TableCreate, TableUpdate

router = APIRouter()


# Add New Table
@router.post("/")
def add_table(table: TableCreate):

    existing = tables_collection.find_one(
        {"table_number": table.table_number}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Table number already exists"
        )

    table_data = table.model_dump()
    table_data["status"] = "available"
    table_data["created_at"] = datetime.utcnow()

    result = tables_collection.insert_one(table_data)

    return {
        "message": "Table added successfully",
        "table_id": str(result.inserted_id)
    }


# Get All Tables
@router.get("/")
def get_tables():

    tables = []

    for table in tables_collection.find():
        tables.append({
            "id": str(table["_id"]),
            "table_number": table["table_number"],
            "capacity": table["capacity"],
            "location": table.get("location"),
            "status": table.get("status", "available")
        })

    return tables


# Get Table By ID
@router.get("/{table_id}")
def get_table(table_id: str):

    if not ObjectId.is_valid(table_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid table ID"
        )

    table = tables_collection.find_one(
        {"_id": ObjectId(table_id)}
    )

    if not table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    return {
        "id": str(table["_id"]),
        "table_number": table["table_number"],
        "capacity": table["capacity"],
        "location": table.get("location"),
        "status": table.get("status", "available")
    }


# Update Table
@router.put("/{table_id}")
def update_table(table_id: str, table: TableUpdate):

    if not ObjectId.is_valid(table_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid table ID"
        )

    update_data = table.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update details provided"
        )

    result = tables_collection.update_one(
        {"_id": ObjectId(table_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    return {
        "message": "Table updated successfully"
    }


# Delete Table
@router.delete("/{table_id}")
def delete_table(table_id: str):

    if not ObjectId.is_valid(table_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid table ID"
        )

    result = tables_collection.delete_one(
        {"_id": ObjectId(table_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    return {
        "message": "Table deleted successfully"
    }
