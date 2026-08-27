import jwt


class JWTManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )

    def validate_access_token(
        self,
        token: str,
    ) -> dict:
        payload = self.decode_access_token(token)

        if payload.get("type") != "access":
            raise jwt.InvalidTokenError(
                "Invalid token type"
            )

        if not payload.get("sub"):
            raise jwt.InvalidTokenError(
                "Missing subject"
            )

        return payload