from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping


class LuceneLogSourceSignature(LogSourceSignature):
    def __init__(self, indices: Optional[list[str]], default_source: dict):
        self.indices = set(indices or [])
        self._default_source = default_source or {}

    def is_suitable(self, index: Optional[list[str]] = None, **kwargs) -> bool:  # noqa: ARG002
        return self._check_conditions([set(index).issubset(self.indices) if index else None])

    def is_probably_suitable(self, index: str) -> bool:
        return self.is_suitable([index]) or self.default_source["index"] == index

    def __str__(self) -> str:
        return self._default_source.get("index", "")


class LuceneMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> LuceneLogSourceSignature:
        indices = mapping.get("log_source", {}).get("index")
        default_log_source = mapping.get("default_log_source", {})
        return LuceneLogSourceSignature(indices=indices, default_source=default_log_source)

    def get_source_mappings_by_log_sources(self, log_sources: dict) -> list[SourceMapping]:
        if not log_sources.get("index") and not isinstance(log_sources.get("index"), list):
            return []
        index = log_sources.get("index")[0]
        mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.log_source_signature.is_probably_suitable(index):
                mappings.append(source_mapping)
        return mappings
