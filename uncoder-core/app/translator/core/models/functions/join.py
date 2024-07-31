from dataclasses import dataclass, field
from typing import Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_container import TokenizedQueryContainer
from app.translator.core.models.query_tokens.field import Alias, BaseFieldsGetter, Field
from app.translator.core.models.query_tokens.field_field import FieldField
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.function_value import FunctionValue
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
    condition: list[Union[FieldField, FieldValue, FunctionValue, Identifier]] = field(default_factory=list)
    preset_log_source_str: str = None

    @property
    def fields(self) -> list[Field]:
        fields = []
        for arg in self.condition:
            if isinstance(arg, BaseFieldsGetter):
                fields.extend(arg.fields)

        return fields
