
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import categories_collection
from models.category import CategoryCreate, CategoryUpdate

router = APIRouter()


# Add New Category
@router.post("/")
def add_category(category: CategoryCreate):

    existing = categories_collection.find_one(
        {"name": category.name}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category_data = category.model_dump()
    category_data["created_at"] = datetime.utcnow()

    result = categories_collection.insert_one(category_data)

    return {
        "message": "Category added successfully",
        "category_id": str(result.inserted_id)
    }


# Get All Categories
@router.get("/")
def get_categories():

    categories = []

    for category in categories_collection.find():
        categories.append({
            "id": str(category["_id"]),
            "name": category["name"],
            "description": category.get("description")
        })

    return categories


# Get Category By ID
@router.get("/{category_id}")
def get_category(category_id: str):

    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid category ID"
        )

    category = categories_collection.find_one(
        {"_id": ObjectId(category_id)}
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category.get("description")
    }


# Update Category
@router.put("/{category_id}")
def update_category(category_id: str, category: CategoryUpdate):

    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid category ID"
        )

    update_data = category.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update details provided"
        )

    result = categories_collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message": "Category updated successfully"
    }


# Delete Category
@router.delete("/{category_id}")
def delete_category(category_id: str):

    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid category ID"
        )

    result = categories_collection.delete_one(
        {"_id": ObjectId(category_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message": "Category deleted successfully"
    }
