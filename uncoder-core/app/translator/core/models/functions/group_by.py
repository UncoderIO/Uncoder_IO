from dataclasses import Field, dataclass, field
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Alias, PredefinedField


@dataclass
class GroupByFunction(Function):
    name: str = FunctionType.stats
    args: list[Function] = field(default_factory=list)
    by_clauses: list[Union[Alias, Field, PredefinedField]] = field(default_factory=list)
    filter_: Function = None
