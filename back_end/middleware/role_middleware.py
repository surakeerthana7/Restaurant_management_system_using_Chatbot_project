
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RoleMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path
        role = getattr(request.state, "role", None)

        # Admin-only routes
        if path.startswith("/api/admin"):
            if role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="Admin access required"
                )

        # Staff-only routes
        elif path.startswith("/api/staff"):
            if role not in ["admin", "staff"]:
                raise HTTPException(
                    status_code=403,
                    detail="Staff access required"
                )

        return await call_next(request)
