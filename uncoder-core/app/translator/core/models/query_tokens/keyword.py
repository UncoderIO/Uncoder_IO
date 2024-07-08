from typing import Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.models.query_tokens.identifier import Identifier


class Keyword:
    def __init__(self, value: Union[str, list[str]]):
        self.operator: Identifier = Identifier(token_type=OperatorType.KEYWORD)
        self.name = "keyword"
        self.values = []
        self.__add_value(value=value)

    @property
    def value(self) -> Union[str, list[str]]:
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    def __add_value(self, value: Union[str, list[str]]) -> None:
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str):
            self.values.append(value)

    def __repr__(self):
        return f"{self.name} {self.operator.token_type} {self.values}"
