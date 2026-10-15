# ==============================
# Library imports
# ==============================

from typing import Any

from pydantic import BaseModel


# ==============================
# Data normalization
# ==============================

class DataNormalizer:
    """
    This class provides utilities for normalizing user-provided data.
    """


    @staticmethod
    def normalize_string(
        value: str,
    ) -> str:
        
        """Remove leading and trailing whitespace from a string."""
        
        return value.strip()


    @staticmethod
    def normalize_model(
        model: BaseModel,
        *,
        exclude_unset: bool = False,
    ) -> dict[str, Any]:
        
        """Return normalized values from a Pydantic model."""

        values = model.model_dump(
            exclude_unset=exclude_unset
        )

        # Normalize string values.
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = DataNormalizer.normalize_string(
                    value
                )

        return values