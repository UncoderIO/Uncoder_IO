from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, TypeVar

from app.translator.mappings.utils.load_from_files import LoaderFileMappings


DEFAULT_MAPPING_NAME = "default"


class LogSourceSignature(ABC):
    _default_source: dict

    @abstractmethod
    def is_suitable(self, *args, **kwargs) -> bool:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Abstract method")


class FieldMapping:
    def __init__(self, generic_field_name: str, platform_field_name: str):
        self.generic_field_name = generic_field_name
        self.platform_field_name = platform_field_name


class FieldsMapping:

    def __init__(self, fields_mapping: list):
        self.__parser_mapping = self.__build_parser_mapping(fields_mapping)
        self.__render_mapping = self.__build_render_mapping(fields_mapping)

    @staticmethod
    def __build_parser_mapping(fields: List[FieldMapping]) -> Dict[str, FieldMapping]:
        result = {}
        for field in fields:
            if isinstance(field.platform_field_name, list):
                for f in field.platform_field_name:
                    result.update({f: field})
            else:
                result.update({field.platform_field_name: field})
        return result

    @staticmethod
    def __build_render_mapping(fields: List[FieldMapping]) -> Dict[str, FieldMapping]:
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

    def is_suitable(self, field_names: List[str]) -> bool:
        return set(field_names).issubset(set(self.__parser_mapping.keys()))


_LogSourceSignatureType = TypeVar('_LogSourceSignatureType', bound=LogSourceSignature)


class SourceMapping:
    def __init__(self,
                 source_id: str,
                 log_source_signature: _LogSourceSignatureType = None,
                 fields_mapping: FieldsMapping = FieldsMapping([])):
        self.source_id = source_id
        self.log_source_signature = log_source_signature
        self.fields_mapping = fields_mapping


class BasePlatformMappings:

    def __init__(self, platform_dir: str):
        self.__loader = LoaderFileMappings()
        self.__platform_dir = platform_dir
        self._source_mappings = self.prepare_mapping()

    def prepare_mapping(self) -> Dict[str, SourceMapping]:
        source_mappings = {}
        default_mapping = SourceMapping(source_id=DEFAULT_MAPPING_NAME)
        for mapping_dict in self.__loader.load_siem_mappings(self.__platform_dir):
            if (source_id := mapping_dict["source"]) == DEFAULT_MAPPING_NAME:
                default_mapping.log_source_signature = self.prepare_log_source_signature(mapping=mapping_dict)
                continue

            fields_mapping = self.prepare_fields_mapping(field_mapping=mapping_dict.get("field_mapping", {}))
            default_mapping.fields_mapping.update(fields_mapping)
            log_source_signature = self.prepare_log_source_signature(mapping=mapping_dict)
            source_mappings[source_id] = SourceMapping(
                source_id=source_id,
                log_source_signature=log_source_signature,
                fields_mapping=fields_mapping
            )

        source_mappings[DEFAULT_MAPPING_NAME] = default_mapping

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

    @abstractmethod
    def get_suitable_source_mappings(self, *args, **kwargs) -> List[SourceMapping]:
        raise NotImplementedError("Abstract method")

    def get_source_mapping(self, source_id: str) -> Optional[SourceMapping]:
        return self._source_mappings.get(source_id)
