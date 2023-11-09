from typing import List, Optional

from app.converter.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class CrowdStrikeLogSourceSignature(LogSourceSignature):
    def __init__(self, event_simple_name: Optional[List[str]], default_source: dict):
        self.event_simple_names = set(event_simple_name or [])
        self._default_source = default_source or {}

    def is_suitable(self, event_simple_name: List[str]) -> bool:
        return set(event_simple_name).issubset(self.event_simple_names)

    def __str__(self) -> str:
        return f"event_simpleName={self._default_source['event_simpleName']}"


class CrowdstrikeMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> CrowdStrikeLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping["default_log_source"]
        return CrowdStrikeLogSourceSignature(
            event_simple_name=log_source.get("event_simpleName"),
            default_source=default_log_source
        )

    def get_suitable_source_mappings(self, field_names: List[str], event_simpleName: List[str]) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            source_signature: CrowdStrikeLogSourceSignature = source_mapping.log_source_signature
            if source_signature.is_suitable(event_simple_name=event_simpleName):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        return suitable_source_mappings or [self._source_mappings[DEFAULT_MAPPING_NAME]]


crowdstrike_mappings = CrowdstrikeMappings(platform_dir="crowdstrike")
