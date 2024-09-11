from typing import Union

from app.translator.core.custom_types.tokens import STR_SEARCH_OPERATORS
<<<<<<< HEAD
from app.translator.core.models.query_tokens.field import Alias, Field, PredefinedField
=======
from app.translator.core.models.query_tokens.field import Alias, BaseFieldsGetter, Field, PredefinedField
>>>>>>> main
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.value import Value
from app.translator.core.str_value_manager import StrValue


<<<<<<< HEAD
class FieldValue(Value):
=======
class FieldValue(BaseFieldsGetter, Value):
>>>>>>> main
    def __init__(
        self,
        source_name: str,
        operator: Identifier,
        value: Union[bool, int, str, StrValue, list, tuple],
        is_alias: bool = False,
        is_predefined_field: bool = False,
    ):
        super().__init__(value, cast_to_int=operator.token_type not in STR_SEARCH_OPERATORS)
        # mapped by platform fields mapping
        self.field = Field(source_name=source_name) if not (is_alias or is_predefined_field) else None
        # not mapped
        self.alias = Alias(name=source_name) if is_alias else None
        # mapped by platform predefined fields mapping
        self.predefined_field = PredefinedField(name=source_name) if is_predefined_field else None
        self.operator = operator

    def __repr__(self):
        if self.alias:
            return f"{self.alias.name} {self.operator.token_type} {self.values}"

        if self.predefined_field:
            return f"{self.predefined_field.name} {self.operator.token_type} {self.values}"

        return f"{self.field.source_name} {self.operator.token_type} {self.values}"
<<<<<<< HEAD
=======

    @property
    def fields(self) -> list[Field]:
        return [self.field] if self.field else []
>>>>>>> main
