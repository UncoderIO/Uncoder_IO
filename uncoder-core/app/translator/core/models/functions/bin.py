from dataclasses import dataclass
from typing import Optional

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function
from app.translator.tools.custom_enum import CustomEnum


class SpanType(CustomEnum):
    days = "days"
    hours = "hours"
    minutes = "minutes"


@dataclass
class Span:
    value: str = "1"
    type_: str = SpanType.days


@dataclass
class BinFunction(Function):
    name: str = FunctionType.bin
    span: Optional[Span] = None
    field: Optional[Field] = None
    bins: Optional[int] = None
