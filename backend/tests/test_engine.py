import pytest

from typeproof.engine import ExtractionEngine
from typeproof.providers import FakeProvider
from typeproof.storage import FailureStore


def test_invalid_first_attempt_is_persisted_and_never_returned():
    store = FailureStore(":memory:")
    result = ExtractionEngine(FakeProvider(), store).extract("Aster Labs appointed Maya Chen on 2024-02-14.", "function", 3)
    assert result.data.date.isoformat() == "2024-02-14"
    assert len(result.attempts) == 2
    assert len(store.list_failures()) == 1


def test_cache_hit_keeps_schema_version_in_key():
    store = FailureStore(":memory:")
    engine = ExtractionEngine(FakeProvider(), store, schema_version="0.3.0")
    first = engine.extract("same input", "json", 3)
    second = engine.extract("same input", "json", 3)
    assert first.cached is False
    assert second.cached is True


def test_exhaustion_does_not_return_invalid_data(monkeypatch):
    class AlwaysBad(FakeProvider):
        def complete(self, text, mode, attempt, repair_prompt=None):
            response = super().complete(text, mode, 1, repair_prompt)
            return response
    with pytest.raises(RuntimeError):
        ExtractionEngine(AlwaysBad(), FailureStore(":memory:")).extract("text", "function", 0)
