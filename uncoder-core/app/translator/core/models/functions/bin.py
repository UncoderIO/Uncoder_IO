from dataclasses import dataclass
from typing import Optional

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.custom_types.time import TimeFrameType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Field


@dataclass
class Span:
    value: str = "1"
    type_: str = TimeFrameType.days


@dataclass
class BinFunction(Function):
    name: str = FunctionType.bin
    span: Optional[Span] = None
    field: Optional[Field] = None
    bins: Optional[int] = None

    @property
    def fields(self) -> list[Field]:
        return [self.field] if self.field else []
