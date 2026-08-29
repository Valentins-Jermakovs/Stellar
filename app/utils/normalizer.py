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


    def normalize_string(
        self,
        value: str,
    ) -> str:
        
        """Remove leading and trailing whitespace from a string."""
        
        return value.strip()


    def normalize_model(
        self,
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
                values[field] = self.normalize_string(
                    value
                )

        return values