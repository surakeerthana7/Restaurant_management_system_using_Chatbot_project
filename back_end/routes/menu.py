
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import menu_collection
from models.menu import MenuCreate, MenuUpdate

router = APIRouter()


# Add New Food Item
@router.post("/")
def add_menu_item(item: MenuCreate):

    item_data = item.model_dump()
    item_data["created_at"] = datetime.utcnow()

    result = menu_collection.insert_one(item_data)

    return {
        "message": "Food item added successfully",
        "item_id": str(result.inserted_id)
    }


# Get All Available Food Items
@router.get("/")
def get_menu():

    menu_items = []

    for item in menu_collection.find():
        menu_items.append({
            "id": str(item["_id"]),
            "name": item["name"],
            "description": item.get("description"),
            "price": item["price"],
            "category_id": item["category_id"],
            "image": item.get("image"),
            "is_available": item.get("is_available", True)
        })

    return menu_items


# Get Food Item By ID
@router.get("/{item_id}")
def get_menu_item(item_id: str):

    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid food item ID"
        )

    item = menu_collection.find_one(
        {"_id": ObjectId(item_id)}
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "category_id": item["category_id"],
        "image": item.get("image"),
        "is_available": item.get("is_available", True)
    }


# Update Food Item
@router.put("/{item_id}")
def update_menu_item(item_id: str, item: MenuUpdate):

    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid food item ID"
        )

    update_data = item.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update details provided"
        )

    result = menu_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    return {
        "message": "Food item updated successfully"
    }


# Delete Food Item
@router.delete("/{item_id}")
def delete_menu_item(item_id: str):

    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid food item ID"
        )

    result = menu_collection.delete_one(
        {"_id": ObjectId(item_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    return {
        "message": "Food item deleted successfully"
    }
