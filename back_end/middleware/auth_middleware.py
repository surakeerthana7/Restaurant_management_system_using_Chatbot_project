
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
import os


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "restaurant_secret_key_change_later"
)

ALGORITHM = "HS256"


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Public routes that do not require login
        public_paths = [
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/api/auth/register",
            "/api/auth/login",
            "/api/menu",
            "/api/categories"
        ]

        if (
            request.method == "OPTIONS"
            or request.url.path in public_paths
            or request.url.path.startswith("/docs/")
        ):
            return await call_next(request)

        # Get token from request header
        authorization = request.headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Please login first"
            )

        token = authorization.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            request.state.user_id = payload.get("user_id")
            request.state.role = payload.get("role")

            if not request.state.user_id or not request.state.role:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid login token"
                )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return await call_next(request)
