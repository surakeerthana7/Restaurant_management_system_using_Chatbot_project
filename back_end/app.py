from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routes import (
    auth, users, menu, categories, orders, tables,
    reservations, payments, feedback, chatbot, admin, staff
)

app = FastAPI(
    title="Restaurant Management System",
    description="Restaurant Management System with Chatbot",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(menu.router, prefix="/api/menu", tags=["Menu"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(tables.router, prefix="/api/tables", tags=["Tables"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["Reservations"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(staff.router, prefix="/api/staff", tags=["Staff"])