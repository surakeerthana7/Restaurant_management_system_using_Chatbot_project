
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import feedback_collection, orders_collection
from models.feedback import FeedbackCreate, FeedbackUpdate

router = APIRouter()


# Submit Customer Feedback
@router.post("/")
def add_feedback(feedback: FeedbackCreate):

    if feedback.order_id:
        if not ObjectId.is_valid(feedback.order_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid order ID"
            )

        order = orders_collection.find_one(
            {"_id": ObjectId(feedback.order_id)}
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

    feedback_data = {
        "user_id": "customer_id",  # Will be replaced with logged-in user ID
        "rating": feedback.rating,
        "comment": feedback.comment,
        "order_id": feedback.order_id,
        "created_at": datetime.utcnow()
    }

    result = feedback_collection.insert_one(feedback_data)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": str(result.inserted_id)
    }


# Get All Feedback
@router.get("/")
def get_feedback():

    feedback_list = []

    for feedback in feedback_collection.find():
        feedback_list.append({
            "id": str(feedback["_id"]),
            "user_id": feedback["user_id"],
            "rating": feedback["rating"],
            "comment": feedback.get("comment"),
            "order_id": feedback.get("order_id"),
            "created_at": feedback.get("created_at")
        })

    return feedback_list


# Get Feedback By ID
@router.get("/{feedback_id}")
def get_feedback_by_id(feedback_id: str):

    if not ObjectId.is_valid(feedback_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid feedback ID"
        )

    feedback = feedback_collection.find_one(
        {"_id": ObjectId(feedback_id)}
    )

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found"
        )

    return {
        "id": str(feedback["_id"]),
        "user_id": feedback["user_id"],
        "rating": feedback["rating"],
        "comment": feedback.get("comment"),
        "order_id": feedback.get("order_id"),
        "created_at": feedback.get("created_at")
    }


# Update Feedback
@router.put("/{feedback_id}")
def update_feedback(feedback_id: str, data: FeedbackUpdate):

    if not ObjectId.is_valid(feedback_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid feedback ID"
        )

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update details provided"
        )

    result = feedback_collection.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found"
        )

    return {
        "message": "Feedback updated successfully"
    }


# Delete Feedback
@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: str):

    if not ObjectId.is_valid(feedback_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid feedback ID"
        )

    result = feedback_collection.delete_one(
        {"_id": ObjectId(feedback_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found"
        )

    return {
        "message": "Feedback deleted successfully"
    }
