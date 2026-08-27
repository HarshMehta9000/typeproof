from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NewsEntity(BaseModel):
    """The only shape allowed to leave the extraction engine."""

    model_config = ConfigDict(extra="forbid", strict=False)

    person: str = Field(min_length=2, max_length=160)
    organization: str = Field(min_length=2, max_length=240)
    date: date
    action: str = Field(min_length=4, max_length=160)
    source_span: str = Field(min_length=1, max_length=240)
    confidence: float = Field(ge=0, le=1)
    schema_version: Literal["0.3.0"] = "0.3.0"

    @field_validator("date", mode="before")
    @classmethod
    def normalize_date(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().replace("/", "-")
        return value


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)
    mode: Literal["function", "json"] = "function"
    provider: str = "fake-local"
    max_retries: int = Field(default=3, ge=0, le=5)
    idempotency_key: Optional[str] = None


class AttemptMeta(BaseModel):
    attempt: int
    provider_mode: str
    model: str
    input_hash: str
    schema_version: str
    duration_ms: int


class ExtractResponse(BaseModel):
    data: NewsEntity
    attempts: list[AttemptMeta]
    cached: bool = False


class FailureRecord(BaseModel):
    id: Optional[int] = None
    raw_output: str
    error_path: str
    error_type: str
    retry_number: int
    provider_mode: str
    model: str
    input_hash: str
    schema_version: str
    created_at: str
