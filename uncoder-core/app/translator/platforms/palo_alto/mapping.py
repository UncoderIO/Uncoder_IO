from typing import Optional, Union

from app.translator.core.mapping import BasePlatformMappings, FieldsMapping, LogSourceSignature, SourceMapping
from app.translator.platforms.palo_alto.const import cortex_xql_query_details


class CortexXQLLogSourceSignature(LogSourceSignature):
    def __init__(self, preset: Optional[list[str]], dataset: Optional[list[str]], default_source: dict):
        self.preset = preset
        self.dataset = dataset
        self._default_source = default_source or {}

    def is_suitable(self, preset: Optional[list[str]] = None, dataset: Optional[list[str]] = None) -> bool:
        conditions = [
            set(preset).issubset(self.preset) if preset else None,
            set(dataset).issubset(self.dataset) if dataset else None,
        ]
        return self._check_conditions(conditions)

    @staticmethod
    def __prepare_log_source_for_render(logsource: Union[str, list[str]], model: str = "datamodel") -> str:
        if isinstance(logsource, list):
            return f"{model} in ({', '.join(source for source in logsource)})"
        return f"{model} = {logsource}"

    @property
    def __datamodel_scheme(self) -> str:
        if datamodel := self._default_source.get("datamodel"):
            return f"{datamodel} "
        return ""

    def __str__(self) -> str:
        if preset_data := self._default_source.get("preset"):
            preset = self.__prepare_log_source_for_render(logsource=preset_data, model="preset")
            return f"{self.__datamodel_scheme}{preset}"
        if dataset_data := self._default_source.get("dataset"):
            dataset = self.__prepare_log_source_for_render(logsource=dataset_data, model="dataset")
            return f"{self.__datamodel_scheme}{dataset}"
        return "datamodel dataset = *"


class CortexXQLMappings(BasePlatformMappings):
    skip_load_default_mappings: bool = False

    def update_default_source_mapping(self, default_mapping: SourceMapping, fields_mapping: FieldsMapping) -> None:
        ...

    def prepare_log_source_signature(self, mapping: dict) -> CortexXQLLogSourceSignature:
        preset = mapping.get("log_source", {}).get("preset")
        dataset = mapping.get("log_source", {}).get("dataset")
        default_log_source = mapping["default_log_source"]
        return CortexXQLLogSourceSignature(preset=preset, dataset=dataset, default_source=default_log_source)


cortex_xql_query_mappings = CortexXQLMappings(
    platform_dir="palo_alto_cortex", platform_details=cortex_xql_query_details
)
