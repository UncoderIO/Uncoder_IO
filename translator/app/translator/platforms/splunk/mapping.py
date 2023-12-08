from typing import List, Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class SplunkLogSourceSignature(LogSourceSignature):
    def __init__(self,
                 sources: Optional[List[str]],
                 source_types: Optional[List[str]],
                 source_categories: Optional[List[str]],
                 indices: Optional[List[str]],
                 default_source: dict = None):
        self.sources = set(sources or [])
        self.source_types = set(source_types or [])
        self.source_categories = set(source_categories or [])
        self.indices = set(indices or [])
        self._default_source = default_source or {}

    def is_suitable(self,
                    source: Optional[List[str]],
                    source_type: Optional[List[str]],
                    source_category: Optional[List[str]],
                    index: Optional[List[str]]) -> bool:
        source_match = set(source or []).issubset(self.sources)
        source_type_match = set(source_type or []).issubset(self.source_types)
        source_category_match = set(source_category or []).issubset(self.source_categories)
        index_match = set(index or []).issubset(self.indices)

        return source_match and source_type_match and source_category_match and index_match

    def __str__(self) -> str:
        return " AND ".join((f"{key}={value}" for key, value in self._default_source.items() if value))


class SplunkMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> SplunkLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping["default_log_source"]
        return SplunkLogSourceSignature(
            sources=log_source.get("source"),
            source_types=log_source.get("source_type"),
            source_categories=log_source.get("source_category"),
            indices=log_source.get("index"),
            default_source=default_log_source
        )

    def get_suitable_source_mappings(self,
                                     field_names: List[str],
                                     source: List[str] = None,
                                     sourcetype: List[str] = None,
                                     sourcecategory: List[str] = None,
                                     index: List[str] = None) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            source_signature: SplunkLogSourceSignature = source_mapping.log_source_signature
            if source_signature.is_suitable(source, sourcetype, sourcecategory, index):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        return suitable_source_mappings or [self._source_mappings[DEFAULT_MAPPING_NAME]]


splunk_mappings = SplunkMappings(platform_dir="splunk")
