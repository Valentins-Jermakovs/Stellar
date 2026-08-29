# ==============================
# Library imports
# ==============================

from collections.abc import Callable

import jwt

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from .jwt import JWTManager


# ==============================
# JWT authentication
# ==============================

class JWTAuth:
    """
    This class provides JWT authentication and role-based
    authorization dependencies for FastAPI endpoints.
    """

    def __init__(
        self,
        jwt_manager: JWTManager,
    ):
        """Initialize the JWT authentication dependencies."""
        self.jwt_manager = jwt_manager
        self.bearer = HTTPBearer()

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(
            HTTPBearer()
        ),
    ) -> dict:
        """Validate the access token and return its payload."""
        token = credentials.credentials

        try:
            return self.jwt_manager.validate_access_token(
                token
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

    def require_roles(
        self,
        roles: list[str],
    ) -> Callable:
        """Create a dependency that requires specific user roles."""

        async def dependency(
            payload: dict = Depends(
                self.get_current_user
            ),
        ) -> dict:
            """Check whether the authenticated user has a required role."""
            user_roles = payload.get(
                "roles",
                [],
            )

            if not any(
                role in user_roles
                for role in roles
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden",
                )

            return payload

        return dependency