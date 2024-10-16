from dataclasses import dataclass, field
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Alias, Field, PredefinedField


@dataclass
class GroupByFunction(Function):
    name: str = FunctionType.stats
    args: list[Function] = field(default_factory=list)
    by_clauses: list[Union[Alias, Field, PredefinedField]] = field(default_factory=list)
    filter_: Function = None

    @property
    def fields(self) -> list[Field]:
        fields = []
        for arg in self.args:
            fields.extend(arg.fields)
        for by_clause in self.by_clauses:
            if isinstance(by_clause, Field):
                fields.append(by_clause)
        if self.filter_:
            fields.extend(self.filter_.fields)

        return fields
