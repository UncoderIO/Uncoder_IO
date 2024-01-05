import re
from abc import ABC
from typing import Union

from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.escape_details import EscapeDetails


class EscapeManager(ABC):
    escape_map: dict[str, EscapeDetails] = {}

    def escape(self, value: Union[str, int], value_type: str = ValueType.value) -> Union[str, int]:
        if isinstance(value, int):
            return value
        if escape_details := self.escape_map.get(value_type):
            symbols_pattern = re.compile(escape_details.pattern)
            value = symbols_pattern.sub(escape_details.escape_symbols, value)
        return value

    def remove_escape(self, value: Union[str, int]) -> Union[str, int]:
        if isinstance(value, int):
            return value
        value = value.encode().decode("unicode_escape")
        return value
