
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from database import orders_collection
from models.order import OrderStatusUpdate

router = APIRouter()


# Get All Orders for Staff
@router.get("/orders")
def get_staff_orders():

    orders = []

    for order in orders_collection.find().sort("created_at", -1):

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


# Get Pending Orders
@router.get("/orders/pending")
def get_pending_orders():

    orders = []

    for order in orders_collection.find({
        "status": {"$in": ["pending", "confirmed", "preparing"]}
    }).sort("created_at", 1):

        orders.append({
            "id": str(order["_id"]),
            "items": order["items"],
            "total_amount": order["total_amount"],
            "order_type": order["order_type"],
            "status": order["status"],
            "created_at": order.get("created_at")
        })

    return orders


# Update Order Preparation Status
@router.put("/orders/{order_id}/status")
def update_staff_order_status(
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
