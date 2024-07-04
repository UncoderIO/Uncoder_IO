from typing import Optional, Union

from app.translator.core.custom_types.tokens import STR_SEARCH_OPERATORS
from app.translator.core.models.functions.base import Function
from app.translator.core.models.identifier import Identifier
from app.translator.core.str_value_manager import StrValue


class FunctionValue:
    def __init__(self, function: Function, operator: Identifier, value: Union[int, str, StrValue, list, tuple]):
        self.function = function
        self.operator = operator
        self.values = []
        self.__add_value(value)

    @property
    def value(self) -> Union[int, str, StrValue, list[Union[int, str, StrValue]]]:
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    @value.setter
    def value(self, new_value: Union[int, str, StrValue, list[Union[int, str, StrValue]]]) -> None:
        self.values = []
        self.__add_value(new_value)

    def __add_value(self, value: Optional[Union[int, str, StrValue, list, tuple]]) -> None:
        if value and isinstance(value, (list, tuple)):
            for v in value:
                self.__add_value(v)
        elif (
            value
            and isinstance(value, str)
            and value.isnumeric()
            and self.operator.token_type not in STR_SEARCH_OPERATORS
        ):
            self.values.append(int(value))
        elif value is not None and isinstance(value, (int, str)):
            self.values.append(value)
