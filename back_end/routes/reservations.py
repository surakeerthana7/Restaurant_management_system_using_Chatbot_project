
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import reservations_collection, tables_collection
from models.reservation import (
    ReservationCreate,
    ReservationStatusUpdate
)

router = APIRouter()


# Create New Reservation
@router.post("/")
def create_reservation(reservation: ReservationCreate):

    if not ObjectId.is_valid(reservation.table_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid table ID"
        )

    table = tables_collection.find_one(
        {"_id": ObjectId(reservation.table_id)}
    )

    if not table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    if table.get("status", "available") != "available":
        raise HTTPException(
            status_code=400,
            detail="Table is not available"
        )

    if reservation.reservation_date <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Reservation date must be in the future"
        )

    if reservation.number_of_guests > table["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Number of guests exceeds table capacity"
        )

    reservation_data = {
        "user_id": "customer_id",  # Will be replaced with logged-in user ID
        "table_id": reservation.table_id,
        "reservation_date": reservation.reservation_date,
        "number_of_guests": reservation.number_of_guests,
        "special_request": reservation.special_request,
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = reservations_collection.insert_one(reservation_data)

    return {
        "message": "Reservation created successfully",
        "reservation_id": str(result.inserted_id)
    }


# Get All Reservations
@router.get("/")
def get_reservations():

    reservations = []

    for reservation in reservations_collection.find():
        reservations.append({
            "id": str(reservation["_id"]),
            "user_id": reservation["user_id"],
            "table_id": reservation["table_id"],
            "reservation_date": reservation["reservation_date"],
            "number_of_guests": reservation["number_of_guests"],
            "special_request": reservation.get("special_request"),
            "status": reservation["status"]
        })

    return reservations


# Get Reservation By ID
@router.get("/{reservation_id}")
def get_reservation(reservation_id: str):

    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid reservation ID"
        )

    reservation = reservations_collection.find_one(
        {"_id": ObjectId(reservation_id)}
    )

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    return {
        "id": str(reservation["_id"]),
        "user_id": reservation["user_id"],
        "table_id": reservation["table_id"],
        "reservation_date": reservation["reservation_date"],
        "number_of_guests": reservation["number_of_guests"],
        "special_request": reservation.get("special_request"),
        "status": reservation["status"]
    }


# Update Reservation Status
@router.put("/{reservation_id}/status")
def update_reservation_status(
    reservation_id: str,
    data: ReservationStatusUpdate
):

    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid reservation ID"
        )

    result = reservations_collection.update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": {"status": data.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    return {
        "message": "Reservation status updated successfully",
        "status": data.status
    }


# Cancel Reservation
@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: str):

    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid reservation ID"
        )

    result = reservations_collection.update_one(
        {
            "_id": ObjectId(reservation_id),
            "status": {"$in": ["pending", "confirmed"]}
        },
        {"$set": {"status": "cancelled"}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Reservation not found or cannot be cancelled"
        )

    return {
        "message": "Reservation cancelled successfully"
    }
