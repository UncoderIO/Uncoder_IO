from typing import Optional, Union

from app.translator.core.str_value_manager import StrValue


class Value:
    def __init__(self, value: Union[bool, int, str, StrValue, list, tuple], cast_to_int: bool = False):
        self.values = []
        self.__cast_to_int = cast_to_int
        self._add_value(value)

    @property
    def value(self) -> Union[bool, int, str, StrValue, list[Union[int, str, StrValue]]]:
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    @value.setter
    def value(self, new_value: Union[bool, int, str, StrValue, list[Union[int, str, StrValue]]]) -> None:
        self.values = []
        self._add_value(new_value)

    def _add_value(self, value: Optional[Union[bool, int, str, StrValue, list, tuple]]) -> None:
        if value and isinstance(value, (list, tuple)):
            for v in value:
                self._add_value(v)
        elif value and isinstance(value, str) and value.isnumeric() and self.__cast_to_int:
            self.values.append(int(value))
        elif value is not None and isinstance(value, (bool, int, str)):
            self.values.append(value)
