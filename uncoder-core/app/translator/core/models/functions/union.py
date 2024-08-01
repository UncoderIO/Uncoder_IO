from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_container import TokenizedQueryContainer
from app.translator.core.models.query_tokens.field import Field


@dataclass
class UnionFunction(Function):
    name: str = FunctionType.union
    tokenized_query_container: TokenizedQueryContainer = None
    preset_log_source_str: str = None

    @property
    def fields(self) -> list[Field]:
        return []
