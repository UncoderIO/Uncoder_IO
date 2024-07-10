from dataclasses import dataclass
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Alias, Field
from app.translator.tools.custom_enum import CustomEnum


class SortOrder(CustomEnum):
    asc = "asc"
    desc = "desc"


@dataclass
class SortArg:
    field: Union[Alias, Field] = None
    function: Function = None
    sort_order: str = SortOrder.asc


@dataclass
class SortLimitFunction(Function):
    name: str = FunctionType.sort_limit
    args: list[SortArg] = None
    limit: str = None
