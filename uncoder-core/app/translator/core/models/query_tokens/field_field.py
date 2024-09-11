from app.translator.core.models.query_tokens.field import Alias, BaseFieldsGetter, Field
from app.translator.core.models.query_tokens.identifier import Identifier


class FieldField(BaseFieldsGetter):
    def __init__(
        self,
        source_name_left: str,
        operator: Identifier,
        source_name_right: str,
        is_alias_left: bool = False,
        is_alias_right: bool = False,
    ):
        self.field_left = Field(source_name=source_name_left) if not is_alias_left else None
        self.alias_left = Alias(name=source_name_left) if is_alias_left else None
        self.operator = operator
        self.field_right = Field(source_name=source_name_right) if not is_alias_right else None
        self.alias_right = Alias(name=source_name_right) if is_alias_right else None

    @property
    def fields(self) -> list[Field]:
        fields = []
        if self.field_left:
            fields.append(self.field_left)
        if self.field_right:
            fields.append(self.field_right)

        return fields
