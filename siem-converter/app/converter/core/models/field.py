from typing import Union, List

from app.converter.core.mapping import SourceMapping
from app.converter.core.models.identifier import Identifier
from app.converter.core.custom_types.tokens import OperatorType


class Field:
    def __init__(self, operator: Identifier, source_name: str, value: Union[int, str, list, tuple]):
        self.operator = operator
        self.values = []
        self.__add_value(value)
        self.source_name = source_name    # input translation field name
        self.generic_names_map = {}

    @property
    def value(self):
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    def __add_value(self, value: Union[int, str, list, tuple]):
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str) and value.isnumeric():
            self.values.append(int(value))
        elif value is not None and isinstance(value, (int, str)):
            self.values.append(value)

    def __add__(self, other):
        self.values.append(other)

    def __repr__(self):
        return f"{self.source_name} {self.operator.token_type} {self.values}"

    def __eq__(self, other):
        if isinstance(other, Field):
            return self._hash == other._hash
        """For OR operator check"""
        if self.source_name == other.source_name and self.operator == other.operator:
            return True
        return False

    def __neq__(self, other):
        """For AND operator check"""
        if self.source_name != other.source_name:
            return True
        return False

    @property
    def _hash(self):
        return hash(str(self))

    def __hash__(self):
        return hash(str(self))


class Keyword:
    def __init__(self, value):
        self.operator: Identifier = Identifier(token_type=OperatorType.KEYWORD)
        self.name = "keyword"
        self.values: [str] = []
        self.__add_value(value=value)

    @property
    def value(self):
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    def __add_value(self, value):
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str):
            self.values.append(value)

    def __add__(self, other):
        if other and isinstance(other, (list, tuple)):
            self.values.extend(other)
        elif other and isinstance(other, str):
            self.values.append(other)
        return self

    def __repr__(self):
        return f"{self.name} {self.operator.token_type} {self.values}"
