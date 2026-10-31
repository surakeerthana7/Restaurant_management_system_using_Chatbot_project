
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import payments_collection, orders_collection
from models.payment import PaymentCreate, PaymentStatusUpdate

router = APIRouter()


# Create Payment
@router.post("/")
def create_payment(payment: PaymentCreate):

    if not ObjectId.is_valid(payment.order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    order = orders_collection.find_one(
        {"_id": ObjectId(payment.order_id)}
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if payment.amount != order["total_amount"]:
        raise HTTPException(
            status_code=400,
            detail="Payment amount does not match order total"
        )

    existing_payment = payments_collection.find_one(
        {"order_id": payment.order_id}
    )

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this order"
        )

    payment_data = {
        "order_id": payment.order_id,
        "user_id": order["user_id"],
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "status": "pending",
        "transaction_id": None,
        "created_at": datetime.utcnow()
    }

    result = payments_collection.insert_one(payment_data)

    return {
        "message": "Payment record created successfully",
        "payment_id": str(result.inserted_id)
    }


# Get All Payments
@router.get("/")
def get_payments():

    payments = []

    for payment in payments_collection.find():
        payments.append({
            "id": str(payment["_id"]),
            "order_id": payment["order_id"],
            "user_id": payment["user_id"],
            "amount": payment["amount"],
            "payment_method": payment["payment_method"],
            "status": payment["status"],
            "transaction_id": payment.get("transaction_id")
        })

    return payments


# Get Payment By ID
@router.get("/{payment_id}")
def get_payment(payment_id: str):

    if not ObjectId.is_valid(payment_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid payment ID"
        )

    payment = payments_collection.find_one(
        {"_id": ObjectId(payment_id)}
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "id": str(payment["_id"]),
        "order_id": payment["order_id"],
        "user_id": payment["user_id"],
        "amount": payment["amount"],
        "payment_method": payment["payment_method"],
        "status": payment["status"],
        "transaction_id": payment.get("transaction_id")
    }


# Update Payment Status
@router.put("/{payment_id}/status")
def update_payment_status(
    payment_id: str,
    data: PaymentStatusUpdate
):

    if not ObjectId.is_valid(payment_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid payment ID"
        )

    result = payments_collection.update_one(
        {"_id": ObjectId(payment_id)},
        {"$set": {"status": data.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "message": "Payment status updated successfully",
        "status": data.status
    }
