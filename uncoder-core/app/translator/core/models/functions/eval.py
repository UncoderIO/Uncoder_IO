from dataclasses import dataclass, field
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Alias, Field
from app.translator.core.models.query_tokens.identifier import Identifier


@dataclass
class EvalArg:
    field_: Union[Alias, Field] = None
    expression: list[Union[Field, Function, Identifier, int, float, str]] = field(default_factory=list)


@dataclass
class EvalFunction(Function):
    name: str = FunctionType.eval
    args: list[EvalArg] = None
