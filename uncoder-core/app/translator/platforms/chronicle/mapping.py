from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class ChronicleLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        return ""


class ChronicleMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> ChronicleLogSourceSignature: ...

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


chronicle_mappings = ChronicleMappings(platform_dir="chronicle")
