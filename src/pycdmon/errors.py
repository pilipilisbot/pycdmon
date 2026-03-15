from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class CdmonError(Exception):
    """Base exception for all cdmon client errors."""


@dataclass(slots=True)
class CdmonApiError(CdmonError):
    """Raised when cdmon returns status=ko or HTTP error with parseable body."""

    message: str
    status_code: int
    payload: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"cdmon API error ({self.status_code}): {self.message}"


class CdmonTransportError(CdmonError):
    """Raised when network or low-level transport operations fail."""
