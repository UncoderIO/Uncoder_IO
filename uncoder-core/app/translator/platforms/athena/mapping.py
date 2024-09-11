from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.athena.const import athena_query_details


class AthenaLogSourceSignature(LogSourceSignature):
    def __init__(self, tables: Optional[list[str]], default_source: dict):
        self.tables = set(tables or [])
        self._default_source = default_source or {}

    def is_suitable(self, table: str) -> bool:
        return table in self.tables

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class AthenaMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> AthenaLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return AthenaLogSourceSignature(tables=tables, default_source=default_log_source)


athena_query_mappings = AthenaMappings(platform_dir="athena", platform_details=athena_query_details)
