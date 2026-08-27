from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal, Optional, Protocol


@dataclass(frozen=True)
class ProviderResponse:
    raw: str
    model: str
    mode: Literal["function", "json"]


class Provider(Protocol):
    def complete(self, text: str, mode: Literal["function", "json"], attempt: int, repair_prompt: Optional[str] = None) -> ProviderResponse: ...


class FakeProvider:
    """Deterministic demo provider: first response is deliberately invalid."""

    model = "fake-typeproof-001"

    def complete(self, text: str, mode: Literal["function", "json"], attempt: int, repair_prompt: Optional[str] = None) -> ProviderResponse:
        payload = {"person": "Maya Chen", "organization": "Aster Labs", "date": "2024-13-40" if attempt == 1 else "2024-02-14", "action": "appointed", "source_span": text[:120], "confidence": 0.97}
        raw = json.dumps(payload) if mode == "json" else json.dumps({"arguments": payload})
        return ProviderResponse(raw=raw, model=self.model, mode=mode)
