from typing import Union

from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.value import Value


class ExtraConditionMixin:
    def generate_extra_conditions(self, source_mapping: SourceMapping) -> list[Union[Value, Identifier]]:
        extra_tokens = []
        for field, value in source_mapping.conditions.items():
            extra_tokens.extend(
                [
                    FieldValue(source_name=field, operator=Identifier(token_type=OperatorType.EQ), value=value),
                    Identifier(token_type=LogicalOperatorType.AND),
                ]
            )
        return extra_tokens
