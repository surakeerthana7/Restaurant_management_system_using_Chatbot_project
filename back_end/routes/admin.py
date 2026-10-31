
from fastapi import APIRouter
from database import (
    users_collection,
    menu_collection,
    orders_collection,
    reservations_collection,
    payments_collection,
    feedback_collection,
    tables_collection
)

router = APIRouter()


# Admin Dashboard Summary
@router.get("/dashboard")
def admin_dashboard():

    total_users = users_collection.count_documents({
        "role": "customer"
    })

    total_menu_items = menu_collection.count_documents({})

    total_orders = orders_collection.count_documents({})

    pending_orders = orders_collection.count_documents({
        "status": "pending"
    })

    completed_orders = orders_collection.count_documents({
        "status": "completed"
    })

    total_reservations = reservations_collection.count_documents({})

    total_tables = tables_collection.count_documents({})

    available_tables = tables_collection.count_documents({
        "status": "available"
    })

    total_payments = payments_collection.count_documents({})

    completed_payments = payments_collection.count_documents({
        "status": "completed"
    })

    total_feedback = feedback_collection.count_documents({})

    return {
        "total_customers": total_users,
        "total_menu_items": total_menu_items,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_reservations": total_reservations,
        "total_tables": total_tables,
        "available_tables": available_tables,
        "total_payments": total_payments,
        "completed_payments": completed_payments,
        "total_feedback": total_feedback
    }


# Get All Registered Staff
@router.get("/staff")
def get_staff():

    staff_members = []

    for staff in users_collection.find({
        "role": {"$in": ["admin", "staff"]}
    }):

        staff_members.append({
            "id": str(staff["_id"]),
            "name": staff["name"],
            "email": staff["email"],
            "phone": staff.get("phone"),
            "role": staff["role"]
        })

    return staff_members
