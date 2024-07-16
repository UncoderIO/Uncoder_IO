from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.platforms.hunters.const import hunters_query_details


class HuntersLogSourceSignature(LogSourceSignature):
    def __init__(self, default_source: dict):
        self._default_source = default_source or {}

    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class HuntersMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> HuntersLogSourceSignature:
        default_log_source = mapping["default_log_source"]
        return HuntersLogSourceSignature(default_source=default_log_source)

    def get_suitable_source_mappings(self, field_names: list[str]) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            if source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


hunters_query_mappings = HuntersMappings(platform_dir="hunters", platform_details=hunters_query_details)
