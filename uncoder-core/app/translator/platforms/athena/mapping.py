from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.platforms.athena.const import athena_query_details


class AthenaLogSourceSignature(LogSourceSignature):
    def __init__(self, tables: Optional[list[str]], default_source: dict):
        self.tables = set(tables or [])
        self._default_source = default_source or {}

    def is_suitable(self, table: list[str]) -> bool:
        return set(table).issubset(self.tables)

    def is_probably_suitable(self, table: str) -> bool:
        return self.is_suitable([table]) or self.default_source["table"] == table

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class AthenaMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> AthenaLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return AthenaLogSourceSignature(tables=tables, default_source=default_log_source)

    def get_source_mappings_by_log_sources(self, log_sources: dict) -> list[SourceMapping]:
        if not log_sources.get("table") and not isinstance(log_sources.get("table"), list):
            return []
        table = log_sources.get("table")[0]
        mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.log_source_signature.is_probably_suitable(table):
                mappings.append(source_mapping)
        return mappings


athena_query_mappings = AthenaMappings(platform_dir="athena", platform_details=athena_query_details)
