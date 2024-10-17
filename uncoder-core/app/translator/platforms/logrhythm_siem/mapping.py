from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class LogRhythmSiemLogSourceSignature(LogSourceSignature):
    def __init__(self, default_source: Optional[dict] = None):
        self._default_source = default_source or {}

    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return "general_information.log_source.type_name"


class LogRhythmSiemMappings(BasePlatformMappings):
    def prepare_mapping(self) -> dict[str, SourceMapping]:
        source_mappings = {}
        for mapping_dict in self._loader.load_platform_mappings(self._platform_dir):
            log_source_signature = self.prepare_log_source_signature(mapping=mapping_dict)
            fields_mapping = self.prepare_fields_mapping(field_mapping=mapping_dict.get("field_mapping", {}))
            source_mappings[DEFAULT_MAPPING_NAME] = SourceMapping(
                source_id=DEFAULT_MAPPING_NAME, log_source_signature=log_source_signature, fields_mapping=fields_mapping
            )
            return source_mappings

    def prepare_log_source_signature(self, mapping: dict) -> LogRhythmSiemLogSourceSignature:
        default_log_source = mapping.get("default_log_source")
        return LogRhythmSiemLogSourceSignature(default_source=default_log_source)

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


logrhythm_siem_mappings = LogRhythmSiemMappings(platform_dir="logrhythm_siem")
