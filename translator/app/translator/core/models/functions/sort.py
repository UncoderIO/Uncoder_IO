from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function
from app.translator.tools.custom_enum import CustomEnum


class SortOrder(CustomEnum):
    asc = "asc"
    desc = "desc"


@dataclass
class SortArg:
    field: Field = None
    sort_order: str = SortOrder.asc


@dataclass
class SortFunction(Function):
    name: str = FunctionType.sort
    args: list[SortArg] = None
    limit: str = None
