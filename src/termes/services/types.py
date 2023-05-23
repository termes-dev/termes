from typing import Any

from pydantic import BaseModel

from termes.types.responses import ErrorResponse


class ServiceRequest(BaseModel):
    headers: dict[str, Any] | None = None
    data: Any | None = None


class ServiceResponse(BaseModel):
    status: int
    headers: dict[str, Any] | None = None
    data: Any | None = None
    error: ErrorResponse | None = None
