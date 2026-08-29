# ==============================
# Library imports
# ==============================

import jwt


# ==============================
# JWT management
# ==============================

class JWTManager:
    """
    This class provides JWT access token decoding and validation.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
    ):
        """Initialize the JWT manager configuration."""
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """Decode an access token and return its payload."""
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )

    def validate_access_token(
        self,
        token: str,
    ) -> dict:
        """Validate an access token and return its payload."""
        payload = self.decode_access_token(token)

        # Verify that the token is an access token.
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError(
                "Invalid token type"
            )

        # Verify that the token contains a subject.
        if not payload.get("sub"):
            raise jwt.InvalidTokenError(
                "Missing subject"
            )

        return payload