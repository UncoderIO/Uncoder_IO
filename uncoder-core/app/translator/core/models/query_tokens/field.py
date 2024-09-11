<<<<<<< HEAD
=======
from abc import ABC, abstractmethod
>>>>>>> main
from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, SourceMapping


class Alias:
    def __init__(self, name: str):
        self.name = name


class Field:
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.__generic_names_map = {}

    def get_generic_field_name(self, source_id: str) -> Optional[str]:
        return self.__generic_names_map.get(source_id)

    def add_generic_names_map(self, generic_names_map: dict) -> None:
        self.__generic_names_map = generic_names_map

    def set_generic_names_map(self, source_mappings: list[SourceMapping], default_mapping: SourceMapping) -> None:
        generic_names_map = {
            source_mapping.source_id: source_mapping.fields_mapping.get_generic_field_name(self.source_name)
            or self.source_name
            for source_mapping in source_mappings
        }
        if DEFAULT_MAPPING_NAME not in generic_names_map:
            fields_mapping = default_mapping.fields_mapping
            generic_names_map[DEFAULT_MAPPING_NAME] = (
                fields_mapping.get_generic_field_name(self.source_name) or self.source_name
            )

        self.__generic_names_map = generic_names_map


class PredefinedField:
    def __init__(self, name: str):
        self.name = name
<<<<<<< HEAD
=======


class BaseFieldsGetter(ABC):
    @property
    @abstractmethod
    def fields(self) -> list[Field]:
        raise NotImplementedError("Abstract method")
>>>>>>> main
