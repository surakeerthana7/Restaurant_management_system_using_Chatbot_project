
from fastapi import APIRouter, HTTPException
from datetime import datetime
from passlib.context import CryptContext
from jose import jwt
import os

from database import users_collection
from models.user import UserCreate, UserLogin

router = APIRouter()

# Password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "restaurant_secret_key_change_later")
ALGORITHM = "HS256"


# Customer Registration
@router.post("/register")
def register(user: UserCreate):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phone": user.phone,
        "role": "customer",
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_data)

    return {
        "message": "Registration successful",
        "user_id": str(result.inserted_id)
    }


# Customer Login
@router.post("/login")
def login(user: UserLogin):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = jwt.encode(
        {
            "user_id": str(existing_user["_id"]),
            "role": existing_user["role"]
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(existing_user["_id"]),
            "name": existing_user["name"],
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    }
