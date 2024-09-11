from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature


class LuceneLogSourceSignature(LogSourceSignature):
    def __init__(self, indices: Optional[list[str]], default_source: dict):
        self.indices = set(indices or [])
        self._default_source = default_source or {}

    def is_suitable(self, index: Optional[list[str]] = None, **kwargs) -> bool:  # noqa: ARG002
        return self._check_conditions([set(index).issubset(self.indices) if index else None])

    def __str__(self) -> str:
        return self._default_source.get("index", "")


class LuceneMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> LuceneLogSourceSignature:
        indices = mapping.get("log_source", {}).get("index")
        default_log_source = mapping.get("default_log_source", {})
        return LuceneLogSourceSignature(indices=indices, default_source=default_log_source)
