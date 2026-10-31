
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import orders_collection
from models.order import OrderCreate, OrderStatusUpdate

router = APIRouter()


# Place New Order
@router.post("/")
def create_order(order: OrderCreate):

    if not order.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one food item"
        )

    total_amount = sum(
        item.price * item.quantity
        for item in order.items
    )

    order_data = {
        "user_id": "customer_id",  # Will be replaced with logged-in user ID
        "items": [
            item.model_dump()
            for item in order.items
        ],
        "total_amount": total_amount,
        "order_type": order.order_type,
        "table_id": order.table_id,
        "delivery_address": order.delivery_address,
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = orders_collection.insert_one(order_data)

    return {
        "message": "Order placed successfully",
        "order_id": str(result.inserted_id),
        "total_amount": total_amount
    }


# Get All Orders
@router.get("/")
def get_orders():

    orders = []

    for order in orders_collection.find():
        orders.append({
            "id": str(order["_id"]),
            "user_id": order["user_id"],
            "items": order["items"],
            "total_amount": order["total_amount"],
            "order_type": order["order_type"],
            "status": order["status"],
            "table_id": order.get("table_id"),
            "delivery_address": order.get("delivery_address"),
            "created_at": order.get("created_at")
        })

    return orders


# Get Order By ID
@router.get("/{order_id}")
def get_order(order_id: str):

    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    order = orders_collection.find_one(
        {"_id": ObjectId(order_id)}
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": str(order["_id"]),
        "user_id": order["user_id"],
        "items": order["items"],
        "total_amount": order["total_amount"],
        "order_type": order["order_type"],
        "status": order["status"],
        "table_id": order.get("table_id"),
        "delivery_address": order.get("delivery_address"),
        "created_at": order.get("created_at")
    }


# Update Order Status
@router.put("/{order_id}/status")
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate
):

    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    result = orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": data.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "message": "Order status updated successfully",
        "status": data.status
    }


# Cancel Order
@router.delete("/{order_id}")
def cancel_order(order_id: str):

    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    result = orders_collection.update_one(
        {
            "_id": ObjectId(order_id),
            "status": {"$in": ["pending", "confirmed"]}
        },
        {"$set": {"status": "cancelled"}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Order not found or cannot be cancelled"
        )

    return {
        "message": "Order cancelled successfully"
    }
