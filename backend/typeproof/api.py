from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Query

from .engine import ExtractionEngine
from .models import ExtractRequest
from .providers import FakeProvider
from .storage import FailureStore

app = FastAPI(title="Typeproof API", version="0.3.0")
store = FailureStore("typeproof.db")
engine = ExtractionEngine(FakeProvider(), store)


@app.post("/extract")
def extract(request: ExtractRequest):
    return engine.extract(request.text, request.mode, request.max_retries, request.idempotency_key)


@app.get("/failures")
def failures(offset: int = Query(0, ge=0), limit: int = Query(25, ge=1, le=100), error_type: Optional[str] = None):
    return {"items": store.list_failures(offset=offset, limit=limit, error_type=error_type), "offset": offset, "limit": limit}


@app.get("/schemas")
def schemas():
    return {"active": "0.3.0", "versions": [{"version": "0.3.0", "compatibility": "backward-compatible", "active": True}]}


@app.get("/schemas/{version}")
def schema(version: str):
    if version != "0.3.0":
        return {"version": version, "status": "immutable historical version"}
    from .models import NewsEntity
    return {"version": version, "json_schema": NewsEntity.model_json_schema()}
