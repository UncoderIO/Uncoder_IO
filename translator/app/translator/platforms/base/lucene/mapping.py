from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class LuceneLogSourceSignature(LogSourceSignature):
    def __init__(self, indices: Optional[list[str]], default_source: dict):
        self.indices = set(indices or [])
        self._default_source = default_source or {}

    def is_suitable(self, index: Optional[list[str]]) -> bool:
        return set(index or []).issubset(self.indices)

    def __str__(self) -> str:
        return self._default_source.get("index", "")


class LuceneMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> LuceneLogSourceSignature:
        indices = mapping.get("log_source", {}).get("index")
        default_log_source = mapping.get("default_log_source", {})
        return LuceneLogSourceSignature(indices=indices, default_source=default_log_source)

    def get_suitable_source_mappings(
        self, field_names: list[str], index: Optional[list[str]] = None
    ) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: LuceneLogSourceSignature = source_mapping.log_source_signature
            if index and log_source_signature.is_suitable(index=index):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)
            elif source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings
