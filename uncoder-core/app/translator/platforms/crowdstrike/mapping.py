from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.crowdstrike.const import crowdstrike_query_details


class CrowdStrikeLogSourceSignature(LogSourceSignature):
    def __init__(self, event_simple_name: Optional[list[str]], default_source: dict):
        self.event_simple_names = set(event_simple_name or [])
        self._default_source = default_source or {}

    def is_suitable(self, event_simpleName: Optional[list[str]] = None) -> bool:  # noqa: N803
        conditions = [set(event_simpleName).issubset(self.event_simple_names) if event_simpleName else None]
        return self._check_conditions(conditions)

    def __str__(self) -> str:
        return f"event_simpleName={self._default_source['event_simpleName']}"


class CrowdstrikeMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> CrowdStrikeLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping["default_log_source"]
        return CrowdStrikeLogSourceSignature(
            event_simple_name=log_source.get("event_simpleName"), default_source=default_log_source
        )


crowdstrike_query_mappings = CrowdstrikeMappings(platform_dir="crowdstrike", platform_details=crowdstrike_query_details)
