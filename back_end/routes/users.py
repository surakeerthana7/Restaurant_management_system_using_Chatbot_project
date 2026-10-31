
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from database import users_collection

router = APIRouter()


# Get All Customers
@router.get("/")
def get_users():

    users = []

    for user in users_collection.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "role": user["role"]
        })

    return users


# Get User By ID
@router.get("/{user_id}")
def get_user(user_id: str):

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    user = users_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user.get("phone"),
        "role": user["role"]
    }


# Update User Profile
@router.put("/{user_id}")
def update_user(user_id: str, data: dict):

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    allowed_fields = ["name", "phone"]

    update_data = {
        key: value
        for key, value in data.items()
        if key in allowed_fields
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided"
        )

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User profile updated successfully"
    }
