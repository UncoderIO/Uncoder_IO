from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.platforms.microsoft.const import (
    microsoft_defender_query_details,
    microsoft_sentinel_query_details,
    microsoft_sentinel_rule_details,
)


class MicrosoftSentinelLogSourceSignature(LogSourceSignature):
    def __init__(self, tables: Optional[list[str]], default_source: dict):
        self.tables = set(tables or [])
        self._default_source = default_source or {}

    def is_suitable(self, table: Optional[list[str]] = None) -> bool:
        return self._check_conditions([set(table).issubset(self.tables) if table else None])

    def is_probably_suitable(self, table: str) -> bool:
        return self.is_suitable([table]) or self.default_source["table"] == table

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class MicrosoftSentinelMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> MicrosoftSentinelLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return MicrosoftSentinelLogSourceSignature(tables=tables, default_source=default_log_source)

    def get_source_mappings_by_log_sources(self, log_sources: dict) -> list[SourceMapping]:
        if not log_sources.get("table") and not isinstance(log_sources.get("table"), list):
            return []
        table = log_sources.get("table")[0]
        mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.log_source_signature.is_probably_suitable(table):
                mappings.append(source_mapping)
        return mappings


microsoft_sentinel_query_mappings = MicrosoftSentinelMappings(
    platform_dir="microsoft_sentinel", platform_details=microsoft_sentinel_query_details
)
microsoft_sentinel_rule_mappings = MicrosoftSentinelMappings(
    platform_dir="microsoft_sentinel", platform_details=microsoft_sentinel_rule_details
)


class MicrosoftDefenderLogSourceSignature(MicrosoftSentinelLogSourceSignature):
    pass


class MicrosoftDefenderMappings(MicrosoftSentinelMappings):
    is_strict_mapping = True

    def prepare_log_source_signature(self, mapping: dict) -> MicrosoftDefenderLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return MicrosoftDefenderLogSourceSignature(tables=tables, default_source=default_log_source)


microsoft_defender_query_mappings = MicrosoftDefenderMappings(
    platform_dir="microsoft_defender", platform_details=microsoft_defender_query_details
)
