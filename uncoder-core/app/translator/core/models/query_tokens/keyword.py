from typing import Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.value import Value


class Keyword(Value):
    def __init__(self, value: Union[str, list[str]]):
        super().__init__(value)
        self.operator: Identifier = Identifier(token_type=OperatorType.KEYWORD)
        self.name = "keyword"

    def _add_value(self, value: Union[str, list[str]]) -> None:
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str):
            self.values.append(value)

    def __repr__(self):
        return f"{self.name} {self.operator.token_type} {self.values}"
