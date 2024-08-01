from typing import Optional

from app.translator.core.mapping import BaseCommonPlatformMappings, LogSourceSignature
from app.translator.platforms.forti_siem.const import forti_siem_rule_details


class FortiSiemLogSourceSignature(LogSourceSignature):
    def __init__(self, event_types: Optional[list[str]], default_source: dict):
        self.event_types = set(event_types or [])
        self._default_source = default_source or {}

    def is_suitable(self, event_type: Optional[list[str]] = None) -> bool:
        return self._check_conditions([set(event_type).issubset(self.event_types) if event_type else None])

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


forti_siem_rule_mappings = FortiSiemMappings(platform_dir="forti_siem", platform_details=forti_siem_rule_details)
