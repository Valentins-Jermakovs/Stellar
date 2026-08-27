from datetime import datetime

import httpx
from flask import session

from stellar.config.settings import settings
from stellar.models.meridian import TokenResponse, User


class MeridianError(Exception):
    """Base exception for Meridian API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)

        self.status_code = status_code


class MeridianClient:
    """Client for communicating with the Meridian authentication service."""

    def __init__(self) -> None:
        self.base_url = settings.MERIDIAN_URL.rstrip("/")


    # ============================================================
    # HTTP
    # ============================================================

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        access_token: str | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Send a request to Meridian."""

        headers = kwargs.pop("headers", {}).copy()

        if access_token:
            headers["Authorization"] = (
                f"Bearer {access_token}"
            )

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
                (
                    f"Meridian returned HTTP "
                    f"{response.status_code}: "
                    f"{response.text}"
                ),
                status_code=response.status_code,
            )

        return response


    async def _authenticated_request(
        self,
        method: str,
        endpoint: str,
        *,
        access_token: str,
        refresh_token: str,
        **kwargs,
    ) -> httpx.Response:
        """
        Send an authenticated request.

        If the access token has expired, automatically refresh
        the token pair and retry the original request once.
        """

        try:

            return await self._request(
                method,
                endpoint,
                access_token=access_token,
                **kwargs,
            )

        except MeridianError as error:

            if error.status_code != 401:
                raise

        # --------------------------------------------------------
        # Access token expired.
        # Refresh the token pair.
        # --------------------------------------------------------

        try:

            tokens = await self.refresh(
                refresh_token
            )

        except MeridianError:

            # Refresh token is also invalid.
            session.clear()

            raise

        # --------------------------------------------------------
        # Save the new tokens.
        # --------------------------------------------------------

        session["access_token"] = (
            tokens.access_token
        )

        session["refresh_token"] = (
            tokens.refresh_token
        )

        # --------------------------------------------------------
        # Retry original request.
        # --------------------------------------------------------

        return await self._request(
            method,
            endpoint,
            access_token=tokens.access_token,
            **kwargs,
        )


    # ============================================================
    # AUTH
    # ============================================================

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

        return self._parse_user(
            response.json()
        )


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

        return self._parse_tokens(
            response.json()
        )


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

        return self._parse_tokens(
            response.json()
        )


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

        refresh_token = session.get(
            "refresh_token"
        )

        if not refresh_token:
            raise MeridianError(
                "Refresh token is missing."
            )

        await self._authenticated_request(
            "POST",
            "/auth/logout-all",
            access_token=access_token,
            refresh_token=refresh_token,
        )


    # ============================================================
    # USERS
    # ============================================================

    async def get_current_user(
        self,
        access_token: str,
    ) -> User:
        """Get the currently authenticated user."""

        refresh_token = session.get(
            "refresh_token"
        )

        if not refresh_token:
            raise MeridianError(
                "Refresh token is missing."
            )

        response = await self._authenticated_request(
            "GET",
            "/users/me",
            access_token=access_token,
            refresh_token=refresh_token,
        )

        return self._parse_user(
            response.json()
        )


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

        payload = {
            key: value
            for key, value in payload.items()
            if value is not None
        }

        refresh_token = session.get(
            "refresh_token"
        )

        if not refresh_token:
            raise MeridianError(
                "Refresh token is missing."
            )

        response = await self._authenticated_request(
            "PATCH",
            "/users/me",
            access_token=access_token,
            refresh_token=refresh_token,
            json=payload,
        )

        return self._parse_user(
            response.json()
        )


    # ============================================================
    # PARSERS
    # ============================================================

    @staticmethod
    def _parse_tokens(
        data: dict,
    ) -> TokenResponse:
        """Convert Meridian token response to TokenResponse."""

        return TokenResponse(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            token_type=data.get(
                "token_type",
                "bearer",
            ),
        )


    @staticmethod
    def _parse_user(
        data: dict,
    ) -> User:
        """Convert Meridian user response to User."""

        return User(
            id=data["id"],
            username=data["username"],
            full_name=data["full_name"],
            email=data["email"],
            roles=data["roles"],
            is_active=data["is_active"],
            created_at=datetime.fromisoformat(
                data["created_at"].replace(
                    "Z",
                    "+00:00",
                )
            ),
        )