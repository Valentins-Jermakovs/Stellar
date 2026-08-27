from datetime import datetime

import httpx

from stellar.config.settings import settings
from stellar.models.meridian import TokenResponse, User


class MeridianError(Exception):
    """Base exception for Meridian API errors."""


class MeridianClient:
    """Client for communicating with the Meridian authentication service."""

    def __init__(self) -> None:
        self.base_url = settings.MERIDIAN_URL.rstrip("/")


    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        access_token: str | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Send a request to Meridian."""

        headers = kwargs.pop("headers", {})

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
        ) as client:

            response = await client.request(
                method,
                endpoint,
                headers=headers,
                **kwargs,
            )

        if response.is_error:
            raise MeridianError(
                f"Meridian returned HTTP {response.status_code}: "
                f"{response.text}"
            )

        return response


    async def register(
        self,
        username: str,
        full_name: str,
        email: str,
        password: str,
    ) -> User:
        """Register a new user."""

        response = await self._request(
            "POST",
            "/auth/register",
            json={
                "username": username,
                "full_name": full_name,
                "email": email,
                "password": password,
            },
        )

        data = response.json()

        return self._parse_user(data)


    async def login(
        self,
        login: str,
        password: str,
    ) -> TokenResponse:
        """Authenticate a user and return tokens."""

        response = await self._request(
            "POST",
            "/auth/login",
            json={
                "login": login,
                "password": password,
            },
        )

        return self._parse_tokens(response.json())


    async def refresh(
        self,
        refresh_token: str,
    ) -> TokenResponse:
        """Rotate the refresh token."""

        response = await self._request(
            "POST",
            "/auth/refresh",
            json={
                "refresh_token": refresh_token,
            },
        )

        return self._parse_tokens(response.json())


    async def logout(
        self,
        refresh_token: str,
    ) -> None:
        """Logout the current session."""

        await self._request(
            "POST",
            "/auth/logout",
            json={
                "refresh_token": refresh_token,
            },
        )


    async def logout_all(
        self,
        access_token: str,
    ) -> None:
        """Logout all sessions for the current user."""

        await self._request(
            "POST",
            "/auth/logout-all",
            access_token=access_token,
        )


    async def get_current_user(
        self,
        access_token: str,
    ) -> User:
        """Get the currently authenticated user."""

        response = await self._request(
            "GET",
            "/users/me",
            access_token=access_token,
        )

        return self._parse_user(response.json())


    async def update_current_user(
        self,
        access_token: str,
        *,
        username: str | None = None,
        full_name: str | None = None,
        email: str | None = None,
        current_password: str | None = None,
        password: str | None = None,
    ) -> User:
        """Update the current user's information."""

        payload = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "current_password": current_password,
            "password": password,
        }

        # Remove fields that were not provided.
        payload = {
            key: value
            for key, value in payload.items()
            if value is not None
        }

        response = await self._request(
            "PATCH",
            "/users/me",
            access_token=access_token,
            json=payload,
        )

        return self._parse_user(response.json())


    @staticmethod
    def _parse_tokens(data: dict) -> TokenResponse:
        """Convert Meridian token response to TokenResponse."""

        return TokenResponse(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            token_type=data.get("token_type", "bearer"),
        )


    @staticmethod
    def _parse_user(data: dict) -> User:
        """Convert Meridian user response to User."""

        return User(
            id=data["id"],
            username=data["username"],
            full_name=data["full_name"],
            email=data["email"],
            roles=data["roles"],
            is_active=data["is_active"],
            created_at=datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            ),
        )