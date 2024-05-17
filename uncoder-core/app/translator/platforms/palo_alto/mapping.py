from typing import Optional, Union

from app.translator.core.mapping import (
    DEFAULT_MAPPING_NAME,
    BasePlatformMappings,
    FieldsMapping,
    LogSourceSignature,
    SourceMapping,
)


class CortexXSIAMLogSourceSignature(LogSourceSignature):
    def __init__(self, preset: Optional[list[str]], dataset: Optional[list[str]], default_source: dict):
        self.preset = preset
        self.dataset = dataset
        self._default_source = default_source or {}

    def is_suitable(self, preset: str, dataset: str) -> bool:
        return preset == self.preset or dataset == self.dataset

    def __prepare_log_source_for_render(self, logsource: Union[str, list[str]], model: str = "datamodel") -> str:
        if isinstance(logsource, list):
            return f"{model} in ({', '.join(source for source in logsource)})"
        return f"{model} = {logsource}"

    def __str__(self) -> str:
        if preset_data := self._default_source.get("preset"):
            return self.__prepare_log_source_for_render(logsource=preset_data, model="preset")
        if dataset_data := self._default_source.get("dataset"):
            return self.__prepare_log_source_for_render(logsource=dataset_data, model="preset")
        return "datamodel"


class CortexXSIAMMappings(BasePlatformMappings):
    skip_load_default_mappings: bool = False

    def update_default_source_mapping(self, default_mapping: SourceMapping, fields_mapping: FieldsMapping) -> None:
        ...

    def prepare_log_source_signature(self, mapping: dict) -> CortexXSIAMLogSourceSignature:
        preset = mapping.get("log_source", {}).get("preset")
        dataset = mapping.get("log_source", {}).get("dataset")
        default_log_source = mapping["default_log_source"]
        return CortexXSIAMLogSourceSignature(preset=preset, dataset=dataset, default_source=default_log_source)

    def get_suitable_source_mappings(
        self, field_names: list[str], preset: Optional[str], dataset: Optional[str]
    ) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: CortexXSIAMLogSourceSignature = source_mapping.log_source_signature
            if (preset or dataset) and log_source_signature.is_suitable(preset=preset, dataset=dataset):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)
            elif source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


cortex_xsiam_mappings = CortexXSIAMMappings(platform_dir="palo_alto_cortex")
