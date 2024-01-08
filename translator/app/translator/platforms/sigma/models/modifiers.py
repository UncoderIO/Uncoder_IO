from typing import Union, List

from app.translator.core.models.field import FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType, GroupType


class ModifierManager:

    and_token = Identifier(token_type=LogicalOperatorType.AND)
    or_token = Identifier(token_type=LogicalOperatorType.OR)

    modifier_map = {
        "re": OperatorType.REGEX
    }
    allowed_modifiers = [*modifier_map.keys(), "all", "windash"]

    def __validate_modifiers(self, modifiers: Union[str, list]):
        if isinstance(modifiers, list) and len(modifiers) > 2:
            raise
        elif isinstance(modifiers, list):
            return all(self.__validate_modifiers(modifier) for modifier in modifiers)
        return True

    def map_modifier(self, modifier: str) -> Identifier:
        return Identifier(token_type=self.modifier_map.get(modifier, modifier))

    def modifier_all(self, field_name: str, modifier: str,
                     values: Union[str, List[str]]) -> Union[tuple, list]:
        if (isinstance(values, list) and len(values) == 1) or isinstance(values, str):
            operator = self.map_modifier(modifier=modifier)
            return (FieldValue(source_name=field_name, operator=operator, value=values), )
        else:
            tokens = []
            for value in values:
                tokens.extend(self.modifier_all(field_name=field_name, modifier=modifier, values=value))
                tokens.append(self.and_token)
            return [Identifier(token_type=GroupType.L_PAREN), *tokens[:-1], Identifier(token_type=GroupType.R_PAREN)]

    def __prepare_windash_value(self, value: str):
        if value.startswith(r"/"):
            return [value, value.replace(r"/", "-", 1)]
        elif value.startswith(r"-"):
            return [value, value.replace("-", r"/", 1)]
        return value

    def modifier_windash(self, field_name: str, modifier: Union[str, list],
                         values: Union[str, List[str]]) -> Union[tuple, list]:
        if isinstance(values, list):
            tokens = []
            for value in values:
                tokens.extend(self.modifier_windash(field_name=field_name, modifier=modifier, values=value))
                tokens.append(self.or_token)
            return [Identifier(token_type=GroupType.L_PAREN), *tokens[:-1], Identifier(token_type=GroupType.R_PAREN)]
        operator = self.map_modifier(modifier=modifier)
        return (FieldValue(source_name=field_name, operator=operator, value=self.__prepare_windash_value(value=values)),)

    def apply_multi_modifier(self, field_name: str, modifier: list,
                             values: Union[str, List[str]]) -> Union[tuple, list]:
        if modifier[-1] == "all":
            return self.modifier_all(field_name=field_name, modifier=modifier[0], values=values)
        elif modifier[-1] == "windash":
            return self.modifier_windash(field_name=field_name, modifier=modifier[0], values=values)

    def apply_modifier(self, field_name: str, modifier: list, values: Union[str, List[str]]) -> tuple:
        modifier = modifier[0]
        if modifier == "windash":
            modifier = OperatorType.EQ
            return self.modifier_windash(field_name=field_name, modifier=modifier, values=values)
        operator = self.map_modifier(modifier=modifier)
        return (FieldValue(source_name=field_name, operator=operator, value=values), )

    def create_token(self, field_name: str, modifier: list,
                     value: Union[str, List[str], int]) -> Union[tuple, list]:
        if len(modifier) == 2:
            return self.apply_multi_modifier(field_name=field_name, modifier=modifier, values=value)
        return self.apply_modifier(field_name=field_name, modifier=modifier, values=value)

    def generate(self, field_name: str, modifier: list,
                 value: Union[str, List[str], int]) -> Union[tuple, list]:
        if self.__validate_modifiers(modifiers=modifier):
            return self.create_token(field_name=field_name, modifier=modifier, value=value)
