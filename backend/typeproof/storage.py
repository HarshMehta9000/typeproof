from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .models import FailureRecord, NewsEntity


class FailureStore:
    """SQLite by default; pass ':memory:' for a local/test-only fallback."""

    def __init__(self, path: str = "typeproof.db", retention_days: int = 30):
        self.path = path
        self.retention_days = retention_days
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXISTS failures (
            id INTEGER PRIMARY KEY AUTOINCREMENT, raw_output TEXT NOT NULL,
            error_path TEXT NOT NULL, error_type TEXT NOT NULL, retry_number INTEGER NOT NULL,
            provider_mode TEXT NOT NULL, model TEXT NOT NULL, input_hash TEXT NOT NULL,
            schema_version TEXT NOT NULL, created_at TEXT NOT NULL)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS extractions (
            cache_key TEXT PRIMARY KEY, payload TEXT NOT NULL, schema_version TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        self.db.commit()

    def save_failure(self, record: FailureRecord) -> int:
        values = record.model_dump(exclude={"id"})
        cur = self.db.execute("INSERT INTO failures(raw_output,error_path,error_type,retry_number,provider_mode,model,input_hash,schema_version,created_at) VALUES (:raw_output,:error_path,:error_type,:retry_number,:provider_mode,:model,:input_hash,:schema_version,:created_at)", values)
        self.db.commit()
        return int(cur.lastrowid)

    def list_failures(self, offset: int = 0, limit: int = 25, error_type: Optional[str] = None) -> list[FailureRecord]:
        query = "SELECT * FROM failures"
        params: list[object] = []
        if error_type:
            query += " WHERE error_type = ?"
            params.append(error_type)
        rows = self.db.execute(query + " ORDER BY id DESC LIMIT ? OFFSET ?", [*params, limit, offset]).fetchall()
        return [FailureRecord(**dict(row)) for row in rows]

    def get_cached(self, cache_key: str, schema_version: str) -> Optional[NewsEntity]:
        row = self.db.execute("SELECT payload FROM extractions WHERE cache_key = ? AND schema_version = ?", (cache_key, schema_version)).fetchone()
        return NewsEntity.model_validate(json.loads(row["payload"])) if row else None

    def cache(self, cache_key: str, entity: NewsEntity) -> None:
        self.db.execute("INSERT OR REPLACE INTO extractions VALUES (?, ?, ?, ?)", (cache_key, entity.model_dump_json(), entity.schema_version, datetime.now(timezone.utc).isoformat()))
        self.db.commit()

    def prune(self) -> None:
        self.db.execute("DELETE FROM failures WHERE created_at < datetime('now', ?)", (f"-{self.retention_days} days",))
        self.db.commit()
