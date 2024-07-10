from dataclasses import dataclass, field
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_container import TokenizedQueryContainer
from app.translator.core.models.query_tokens.field import Alias, Field
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.tools.custom_enum import CustomEnum


class JoinType(CustomEnum):
    inner = "inner"
    left = "left"
    right = "right"
    cross = "cross"


@dataclass
class JoinFunction(Function):
    name: str = FunctionType.join
    alias: Alias = None
    type_: str = JoinType.inner
    tokenized_query_container: TokenizedQueryContainer = None
    condition: list[Union[Alias, Field, Identifier]] = field(default_factory=list)
    preset_log_source_str: str = None
