from typing import Optional

from app.translator.core.mapping import (
    DEFAULT_MAPPING_NAME,
    BaseCommonPlatformMappings,
    LogSourceSignature,
    SourceMapping,
)
from app.translator.platforms.forti_siem.const import forti_siem_rule_details


class FortiSiemLogSourceSignature(LogSourceSignature):
    def __init__(self, event_types: Optional[list[str]], default_source: dict):
        self.event_types = set(event_types or [])
        self._default_source = default_source or {}

    def is_suitable(self, event_type: str) -> bool:
        return event_type in self.event_types

    def __str__(self) -> str:
        event_type = self._default_source.get("eventType", "")
        if event_type:
            if event_type.startswith(self.wildcard_symbol) and not event_type.endswith(self.wildcard_symbol):
                return f'eventType REGEXP "{event_type.lstrip(self.wildcard_symbol)}$"'
            if event_type.endswith(self.wildcard_symbol) and not event_type.startswith(self.wildcard_symbol):
                return f'eventType REGEXP "^{event_type.rstrip(self.wildcard_symbol)}"'

            if self.wildcard_symbol in event_type:
                return f'eventType REGEXP "{event_type}"'

            return f'eventType = "{event_type}"'

        return ""


class FortiSiemMappings(BaseCommonPlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> FortiSiemLogSourceSignature:
        event_types = mapping.get("log_source", {}).get("eventType")
        default_log_source = mapping["default_log_source"]
        return FortiSiemLogSourceSignature(event_types=event_types, default_source=default_log_source)

    def get_suitable_source_mappings(self, field_names: list[str], event_type: Optional[str]) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: FortiSiemLogSourceSignature = source_mapping.log_source_signature
            if event_type and log_source_signature.is_suitable(event_type=event_type):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)
            elif source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


forti_siem_rule_mappings = FortiSiemMappings(platform_dir="forti_siem", platform_details=forti_siem_rule_details)
