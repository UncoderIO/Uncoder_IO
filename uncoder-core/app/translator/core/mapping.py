from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, TypeVar, Union

from app.translator.core.exceptions.core import StrictPlatformException
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.mappings.utils.load_from_files import LoaderFileMappings

if TYPE_CHECKING:
    from app.translator.core.models.query_tokens.field import Field


DEFAULT_MAPPING_NAME = "default"


class LogSourceSignature(ABC):
    _default_source: dict
    wildcard_symbol = "*"

    @abstractmethod
    def is_suitable(self, **kwargs) -> bool:
        raise NotImplementedError("Abstract method")

    @staticmethod
    def _check_conditions(conditions: list[Union[bool, None]]) -> bool:
        conditions = [condition for condition in conditions if condition is not None]
        return bool(conditions) and all(conditions)

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Abstract method")

    @property
    def default_source(self) -> dict:
        return self._default_source


class FieldMapping:
    def __init__(self, generic_field_name: str, platform_field_name: str):
        self.generic_field_name = generic_field_name
        self.platform_field_name = platform_field_name


class FieldsMapping:
    def __init__(self, fields_mapping: list):
        self.__parser_mapping = self.__build_parser_mapping(fields_mapping)
        self.__render_mapping = self.__build_render_mapping(fields_mapping)

    @staticmethod
    def __build_parser_mapping(fields: list[FieldMapping]) -> dict[str, FieldMapping]:
        result = {}
        for field in fields:
            if isinstance(field.platform_field_name, list):
                for f in field.platform_field_name:
                    result.update({f: field})
            else:
                result.update({field.platform_field_name: field})
        return result

    @staticmethod
    def __build_render_mapping(fields: list[FieldMapping]) -> dict[str, FieldMapping]:
        return {field.generic_field_name: field for field in fields}

    def get_generic_field_name(self, platform_field_name: str) -> Optional[str]:
        field = self.__parser_mapping.get(platform_field_name)
        return field and field.generic_field_name

    def get_platform_field_name(self, generic_field_name: str) -> Optional[str]:
        field = self.__render_mapping.get(generic_field_name)
        return field and field.platform_field_name

    def update(self, fields_mapping: FieldsMapping) -> None:
        self.__parser_mapping.update(fields_mapping.__parser_mapping)
        self.__render_mapping.update(fields_mapping.__render_mapping)

    def is_suitable(self, field_names: list[str]) -> bool:
        return bool(field_names) and set(field_names).issubset(set(self.__parser_mapping.keys()))


_LogSourceSignatureType = TypeVar("_LogSourceSignatureType", bound=LogSourceSignature)


class SourceMapping:
    def __init__(
        self,
        source_id: str,
        log_source_signature: _LogSourceSignatureType = None,
        fields_mapping: Optional[FieldsMapping] = None,
        raw_log_fields: Optional[dict] = None,
    ):
        self.source_id = source_id
        self.log_source_signature = log_source_signature
        self.fields_mapping = fields_mapping or FieldsMapping([])
        self.raw_log_fields = raw_log_fields


class BasePlatformMappings:
    details: PlatformDetails = None

    is_strict_mapping: bool = False
    skip_load_default_mappings: bool = True
    extend_default_mapping_with_all_fields: bool = False

    def __init__(self, platform_dir: str, platform_details: PlatformDetails):
        self._loader = LoaderFileMappings()
        self._platform_dir = platform_dir
        self.details = platform_details
        self._source_mappings = self.prepare_mapping()

    def update_default_source_mapping(self, default_mapping: SourceMapping, fields_mapping: FieldsMapping) -> None:
        default_mapping.fields_mapping.update(fields_mapping)

    def prepare_mapping(self) -> dict[str, SourceMapping]:
        source_mappings = {}
        default_mapping = SourceMapping(source_id=DEFAULT_MAPPING_NAME)
        for mapping_dict in self._loader.load_platform_mappings(self._platform_dir):
            log_source_signature = self.prepare_log_source_signature(mapping=mapping_dict)
            if (source_id := mapping_dict["source"]) == DEFAULT_MAPPING_NAME:
                default_mapping.log_source_signature = log_source_signature
                if self.skip_load_default_mappings:
                    continue

            field_mappings_dict = mapping_dict.get("field_mapping", {})
            raw_log_fields = mapping_dict.get("raw_log_fields", {})
            field_mappings_dict.update({field: field for field in raw_log_fields})
            fields_mapping = self.prepare_fields_mapping(field_mapping=field_mappings_dict)
            self.update_default_source_mapping(default_mapping=default_mapping, fields_mapping=fields_mapping)
            source_mappings[source_id] = SourceMapping(
                source_id=source_id,
                log_source_signature=log_source_signature,
                fields_mapping=fields_mapping,
                raw_log_fields=raw_log_fields,
            )

        if self.skip_load_default_mappings:
            source_mappings[DEFAULT_MAPPING_NAME] = default_mapping

        if self.extend_default_mapping_with_all_fields:
            source_mappings[DEFAULT_MAPPING_NAME].fields_mapping.update(default_mapping.fields_mapping)

        return source_mappings

    @staticmethod
    def prepare_fields_mapping(field_mapping: dict) -> FieldsMapping:
        fields = []
        for generic_field_name, platform_field_name in field_mapping.items():
            fields.append(FieldMapping(generic_field_name=generic_field_name, platform_field_name=platform_field_name))
        return FieldsMapping(fields_mapping=fields)

    @abstractmethod
    def prepare_log_source_signature(self, mapping: dict) -> LogSourceSignature:
        raise NotImplementedError("Abstract method")

    def get_suitable_source_mappings(
        self, field_names: list[str], log_sources: dict[str, list[Union[int, str]]]
    ) -> list[SourceMapping]:
        by_log_sources_and_fields = []
        by_fields = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            if source_mapping.fields_mapping.is_suitable(field_names):
                by_fields.append(source_mapping)

                log_source_signature: LogSourceSignature = source_mapping.log_source_signature
                if log_source_signature and log_source_signature.is_suitable(**log_sources):
                    by_log_sources_and_fields.append(source_mapping)

        return by_log_sources_and_fields or by_fields or [self._source_mappings[DEFAULT_MAPPING_NAME]]

    def get_source_mapping(self, source_id: str) -> Optional[SourceMapping]:
        return self._source_mappings.get(source_id)

    @property
    def default_mapping(self) -> SourceMapping:
        return self._source_mappings[DEFAULT_MAPPING_NAME]

    def check_fields_mapping_existence(self, field_tokens: list[Field], source_mapping: SourceMapping) -> list[str]:
        unmapped = []
        for field in field_tokens:
            generic_field_name = field.get_generic_field_name(source_mapping.source_id)
            mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
            if not mapped_field and field.source_name not in unmapped:
                unmapped.append(field.source_name)

        if self.is_strict_mapping and unmapped:
            raise StrictPlatformException(
                platform_name=self.details.name, fields=unmapped, mapping=source_mapping.source_id
            )

        return unmapped

    @staticmethod
    def map_field(field: Field, source_mapping: SourceMapping) -> list[str]:
        generic_field_name = field.get_generic_field_name(source_mapping.source_id)
        # field can be mapped to corresponding platform field name or list of platform field names
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)

        if isinstance(mapped_field, str):
            mapped_field = [mapped_field]

        return mapped_field if mapped_field else [generic_field_name] if generic_field_name else [field.source_name]


class BaseCommonPlatformMappings(ABC, BasePlatformMappings):
    def prepare_mapping(self) -> dict[str, SourceMapping]:
        source_mappings = {}
        common_field_mapping = self._loader.load_common_mapping(self._platform_dir).get("field_mapping", {})

        for mapping_dict in self._loader.load_platform_mappings(self._platform_dir):
            source_id = mapping_dict["source"]
            log_source_signature = self.prepare_log_source_signature(mapping=mapping_dict)
            fields_mapping = self.prepare_fields_mapping(field_mapping=common_field_mapping)
            source_mappings[source_id] = SourceMapping(
                source_id=source_id, log_source_signature=log_source_signature, fields_mapping=fields_mapping
            )

        return source_mappings
