from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class MicrosoftSentinelLogSourceSignature(LogSourceSignature):
    def __init__(self, tables: Optional[list[str]], default_source: dict):
        self.tables = set(tables or [])
        self._default_source = default_source or {}

    def is_suitable(self, table: list[str]) -> bool:
        return set(table).issubset(self.tables)

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class MicrosoftSentinelMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> MicrosoftSentinelLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return MicrosoftSentinelLogSourceSignature(tables=tables, default_source=default_log_source)

    def get_suitable_source_mappings(self, field_names: list[str], table: list[str]) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: MicrosoftSentinelLogSourceSignature = source_mapping.log_source_signature
            if log_source_signature.is_suitable(table=table) and source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


microsoft_sentinel_mappings = MicrosoftSentinelMappings(platform_dir="microsoft_sentinel")


class MicrosoftDefenderLogSourceSignature(MicrosoftSentinelLogSourceSignature):
    pass


class MicrosoftDefenderMappings(MicrosoftSentinelMappings):
    def prepare_log_source_signature(self, mapping: dict) -> MicrosoftDefenderLogSourceSignature:
        tables = mapping.get("log_source", {}).get("table")
        default_log_source = mapping["default_log_source"]
        return MicrosoftDefenderLogSourceSignature(tables=tables, default_source=default_log_source)


microsoft_defender_mappings = MicrosoftDefenderMappings(platform_dir="microsoft_defender")
