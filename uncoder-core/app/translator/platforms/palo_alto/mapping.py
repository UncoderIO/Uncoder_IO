from typing import Optional, Union

from app.translator.core.mapping import (
    BasePlatformMappings,
    BaseStrictLogSourcesPlatformMappings,
    FieldsMapping,
    LogSourceSignature,
    SourceMapping,
)
from app.translator.platforms.palo_alto.const import cortex_xdr_xql_query_details, cortex_xsiam_xql_query_details


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
    def __data_model_scheme(self) -> str:
        if data_model := self._default_source.get("datamodel"):
            return f"{data_model} "
        return ""

    def __str__(self) -> str:
        if preset_data := self._default_source.get("preset"):
            preset = self.__prepare_log_source_for_render(logsource=preset_data, model="preset")
            return f"{self.__data_model_scheme}{preset}"
        if dataset_data := self._default_source.get("dataset"):
            dataset = self.__prepare_log_source_for_render(logsource=dataset_data, model="dataset")
            return f"{self.__data_model_scheme}{dataset}"
        return "datamodel dataset = *"


class CortexXQLLogSourceSignaturePreparer:
    @staticmethod
    def prepare_log_source_signature(mapping: dict) -> CortexXQLLogSourceSignature:
        preset = mapping.get("log_source", {}).get("preset")
        dataset = mapping.get("log_source", {}).get("dataset")
        default_log_source = mapping["default_log_source"]
        return CortexXQLLogSourceSignature(preset=preset, dataset=dataset, default_source=default_log_source)


class CortexXSIAMXQLMappings(CortexXQLLogSourceSignaturePreparer, BasePlatformMappings):
    skip_load_default_mappings: bool = False

    def update_default_source_mapping(self, default_mapping: SourceMapping, fields_mapping: FieldsMapping) -> None:
        ...


class CortexXDRXQLMappings(CortexXQLLogSourceSignaturePreparer, BaseStrictLogSourcesPlatformMappings):
    ...


cortex_xsiam_xql_query_mappings = CortexXSIAMXQLMappings(
    platform_dir="palo_alto_cortex_xsiam", platform_details=cortex_xsiam_xql_query_details
)
cortex_xdr_xql_query_mappings = CortexXDRXQLMappings(
    platform_dir="palo_alto_cortex_xdr", platform_details=cortex_xdr_xql_query_details
)
