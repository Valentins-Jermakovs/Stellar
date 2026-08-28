from typing import Any

from pydantic import BaseModel


class DataNormalizer:
    """Normalize user-provided data before processing."""

    @staticmethod
    def normalize_string(value: str) -> str:
        """Remove leading and trailing whitespace."""
        return value.strip()

    @classmethod
    def normalize_model(
        cls,
        model: BaseModel,
        *,
        exclude_unset: bool = False,
    ) -> dict[str, Any]:
        """Return normalized values from a Pydantic model."""
        values = model.model_dump(
            exclude_unset=exclude_unset
        )

        for field, value in values.items():
            if isinstance(value, str):
                values[field] = cls.normalize_string(
                    value
                )

        return values